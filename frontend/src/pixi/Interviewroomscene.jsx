import { useEffect, useRef, useState } from "react";
import { Application, Graphics, Container } from "pixi.js";

/**
 * InterviewRoomScene
 * -------------------
 * The one "signature" piece rendered with PixiJS: a pixel-art AI interviewer
 * avatar (plus a smaller candidate figure) sitting at a desk, idling gently,
 * with a comic-style thought bubble that appears above whichever "agent"
 * is currently working:
 *   - phase "thinking"  -> bubble over the interviewer (it's evaluating)
 *   - phase "listening" -> bubble over the candidate (they're typing)
 *
 * Everything else in the app (forms, buttons, text) stays as real DOM/CSS —
 * PixiJS is used only where it earns its keep: an ambient, animated,
 * game-like visual, not form controls.
 *
 * Props:
 *   phase: "idle" | "listening" | "thinking" | "done"
 *   height: canvas height in px (width fills the parent)
 */

function InterviewRoomScene({ phase = "idle", height = 150 }) {
    const hostRef = useRef(null);
    const appRef = useRef(null);
    const stateRef = useRef({ phase });
    const [failed, setFailed] = useState(false);
    const [errorMessage, setErrorMessage] = useState("");

    // keep latest phase available inside the ticker closure
    useEffect(() => {
        stateRef.current.phase = phase;
    }, [phase]);

    useEffect(() => {
        let destroyed = false;
        const host = hostRef.current;
        if (!host) return;

        // Pixi v7 has a completely different API (sync `new Application({...})`,
        // `app.view` instead of `app.canvas`, old-style Graphics drawing).
        // Catch that early with an actionable message rather than a cryptic
        // TypeError from deep inside setup().
        if (typeof Application.prototype.init !== "function") {
            console.error(
                "InterviewRoomScene requires pixi.js v8+ (found an older API — " +
                    "`Application.prototype.init` is missing). Run: npm install pixi.js@latest"
            );
            setErrorMessage(
                "installed pixi.js looks like v7 — run: npm install pixi.js@latest"
            );
            setFailed(true);
            return;
        }

        const app = new Application();

        async function initWithFallback(opts) {
            // Some setups have a flaky WebGPU adapter that makes init() reject;
            // force WebGL first, then fall back to Pixi's own auto-detection.
            try {
                await app.init({ ...opts, preference: "webgl" });
            } catch (webglErr) {
                console.warn(
                    "Pixi init with preference:'webgl' failed, retrying with defaults:",
                    webglErr
                );
                await app.init(opts);
            }
        }

        async function setup() {
            // Measure the host BEFORE init so we never hand Pixi a 0x0 canvas
            // (which is what happens if init runs before layout settles).
            const rect = host.getBoundingClientRect();
            const startW = Math.max(Math.round(rect.width), 320);
            const startH = Math.max(Math.round(rect.height), height);

            await initWithFallback({
                width: startW,
                height: startH,
                background: 0x6e7c5a,
                antialias: false,
                resolution: Math.min(window.devicePixelRatio || 1, 2),
                autoDensity: true,
                roundPixels: true,
            });

            if (destroyed) {
                app.destroy(true, { children: true });
                return;
            }

            app.canvas.style.display = "block";
            app.canvas.style.width = "100%";
            app.canvas.style.height = "100%";
            host.appendChild(app.canvas);
            appRef.current = app;

            // now that we're attached, let Pixi track the host's size live
            app.resizeTo = host;

            const W = () => app.renderer.width / app.renderer.resolution;
            const H = () => app.renderer.height / app.renderer.resolution;

            const root = new Container();
            app.stage.addChild(root);

            // ---- floor ----
            const floor = new Graphics();
            root.addChild(floor);

            // ---- desks ----
            const deskLeft = buildDesk(0.75);
            const deskRight = buildDesk(1.3);
            root.addChild(deskLeft, deskRight);

            // ---- people (interviewer is the "agent", bigger + centered) ----
            const candidate = buildPerson(0xd9a441, 0x2b2b23, 0.85);
            const interviewer = buildPerson(0x5f7fb8, 0x2b2b23, 1.5);
            root.addChild(candidate, interviewer);

            // ---- thought bubbles ----
            const candidateBubble = buildThoughtBubble(0.7);
            const interviewerBubble = buildThoughtBubble(1.1);
            root.addChild(candidateBubble, interviewerBubble);

            // ---- status lamp ----
            const lamp = new Graphics();
            root.addChild(lamp);

            let deskY = 0;
            let candidateBaseY = 0;
            let interviewerBaseY = 0;

            function layout() {
                const w = W();
                const h = H();

                drawFloor(floor, w, h);

                deskY = h * 0.66;
                deskLeft.position.set(w * 0.2, deskY);
                deskRight.position.set(w * 0.72, deskY);

                candidateBaseY = deskY - 30;
                interviewerBaseY = deskY - 46;

                candidate.position.set(w * 0.2, candidateBaseY);
                interviewer.position.set(w * 0.72, interviewerBaseY);
                interviewer.scale.x = -Math.abs(interviewer.scale.x);

                candidateBubble.position.set(w * 0.2 + 26, candidateBaseY - 58);
                interviewerBubble.position.set(w * 0.72 - 30, interviewerBaseY - 78);

                lamp.position.set(w - 22, 20);
            }

            layout();
            app.renderer.on("resize", layout);

            let t = 0;
            app.ticker.add(() => {
                t += app.ticker.deltaTime * 0.06;
                const ph = stateRef.current.phase;

                // idle bob for both figures
                candidate.position.y = candidateBaseY + Math.sin(t) * 2;
                interviewer.position.y = interviewerBaseY + Math.sin(t + 1.4) * 2;

                // thought bubbles: interviewer thinks, candidate "thinks" while typing
                const showInterviewer = ph === "thinking";
                const showCandidate = ph === "listening";

                interviewerBubble.visible = showInterviewer;
                candidateBubble.visible = showCandidate;

                if (showInterviewer) {
                    interviewerBubble.y = interviewerBaseY - 78 + Math.sin(t * 1.6) * 2;
                    animateBubbleDots(interviewerBubble, t);
                }
                if (showCandidate) {
                    candidateBubble.y = candidateBaseY - 58 + Math.sin(t * 1.6) * 2;
                    animateBubbleDots(candidateBubble, t);
                }

                // status lamp: solid, pulsing while an agent is working
                const color =
                    ph === "thinking"
                        ? 0x5fb8b0
                        : ph === "listening"
                        ? 0xe3a23c
                        : ph === "done"
                        ? 0x7cc576
                        : 0x8a8a78;
                const pulsing = ph === "listening" || ph === "thinking";
                const alpha = pulsing ? 0.55 + Math.sin(t * 4) * 0.45 : 1;
                lamp.clear();
                lamp.circle(0, 0, 7).fill({ color, alpha: Math.max(alpha, 0.15) });
                lamp.circle(0, 0, 7).stroke({ width: 2, color: 0x000000 });
            });
        }

        setup().catch((err) => {
            // Fail visibly instead of leaving a blank box, and surface the
            // real error text so you don't have to dig through devtools.
            console.error("InterviewRoomScene failed to initialize:", err);
            setErrorMessage(err?.message || String(err));
            setFailed(true);
        });

        return () => {
            destroyed = true;
            if (appRef.current) {
                appRef.current.destroy(true, { children: true });
                appRef.current = null;
            }
            if (host) host.innerHTML = "";
        };
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []);

    return (
        <div
            ref={hostRef}
            style={{
                width: "100%",
                height,
                border: "3px solid var(--ink)",
                borderTop: "none",
                overflow: "hidden",
                lineHeight: 0,
                background: "var(--olive)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
            }}
        >
            {failed && (
                <span
                    style={{
                        fontFamily: "var(--font-mono)",
                        fontSize: 11,
                        color: "var(--paper)",
                        padding: "0 12px",
                        textAlign: "center",
                        lineHeight: 1.5,
                    }}
                >
                    scene failed to load{errorMessage ? `: ${errorMessage}` : ""}
                </span>
            )}
        </div>
    );
}

function animateBubbleDots(bubble, t) {
    // Use children.find rather than getChildByLabel — that helper was added
    // in a later Pixi v8 minor version and may not exist on every install.
    const dots = bubble.children.find((ch) => ch.label === "dots");
    if (!dots) return;
    dots.children.forEach((d, i) => {
        d.position.y = Math.sin(t * 5 + i * 1.4) * 2;
    });
}

function drawFloor(g, w, h) {
    g.clear();
    g.rect(0, 0, w, h).fill({ color: 0x6e7c5a });
    const tile = 20;
    for (let x = 0; x < w; x += tile) {
        g.moveTo(x, 0).lineTo(x, h).stroke({ width: 1, color: 0x5c6a49, alpha: 0.6 });
    }
    for (let y = 0; y < h; y += tile) {
        g.moveTo(0, y).lineTo(w, y).stroke({ width: 1, color: 0x5c6a49, alpha: 0.6 });
    }
}

function buildDesk(scale = 1) {
    const g = new Graphics();
    g.rect(-30, 0, 60, 8).fill({ color: 0x8a5a34 });
    g.rect(-30, 8, 60, 4).fill({ color: 0x6b4526 });
    // monitor
    g.rect(-10, -18, 20, 16).fill({ color: 0x22271d });
    g.rect(-7, -15, 14, 10).fill({ color: 0x2f6f4a });
    g.scale.set(scale);
    return g;
}

/**
 * A simple blocky pixel-avatar: hair, head, body, and a couple of
 * face pixels so it reads as a character rather than a silhouette.
 */
function buildPerson(shirtColor, hairColor, scale = 1) {
    const c = new Container();
    const g = new Graphics();

    // body
    g.rect(-9, 0, 18, 16).fill({ color: shirtColor });
    g.rect(-9, 0, 18, 3).fill({ color: 0x000000, alpha: 0.15 }); // collar shade

    // head
    g.rect(-7, -14, 14, 14).fill({ color: 0xe7c9a1 });

    // hair
    g.rect(-7, -14, 14, 5).fill({ color: hairColor });

    // face pixels (eyes)
    g.rect(-4, -6, 2, 2).fill({ color: 0x2b2b23 });
    g.rect(2, -6, 2, 2).fill({ color: 0x2b2b23 });

    c.addChild(g);
    c.scale.set(scale);
    c.label = "person";
    return c;
}

/**
 * Pixel-cloud "thinking" bubble: a stack of offset squares forming a
 * rounded silhouette, two small trailing circles leading down toward the
 * character's head, and three animated dots inside.
 */
function buildThoughtBubble(scale = 1) {
    const c = new Container();

    const cloud = new Graphics();
    // stacked squares approximate a pixel "cloud" shape
    cloud.rect(-22, -14, 44, 22).fill({ color: 0xf5f1df });
    cloud.rect(-16, -20, 32, 8).fill({ color: 0xf5f1df });
    cloud.rect(-22, -14, 44, 22).stroke({ width: 2, color: 0x000000 });
    cloud.rect(-16, -20, 32, 8).stroke({ width: 2, color: 0x000000 });
    cloud.label = "cloud";
    c.addChild(cloud);

    // trailing circles down to the character's head
    const trail1 = new Graphics();
    trail1.circle(-4, 14, 4).fill({ color: 0xf5f1df }).stroke({ width: 2, color: 0x000000 });
    const trail2 = new Graphics();
    trail2.circle(-10, 22, 2.5).fill({ color: 0xf5f1df }).stroke({ width: 1.5, color: 0x000000 });
    c.addChild(trail1, trail2);

    // three animated dots inside the cloud
    const dots = new Container();
    dots.label = "dots";
    for (let i = 0; i < 3; i++) {
        const d = new Graphics();
        d.rect(0, 0, 4, 4).fill({ color: 0x2b2b23 });
        d.position.set(i * 9 - 9, -4);
        dots.addChild(d);
    }
    c.addChild(dots);

    c.scale.set(scale);
    c.visible = false;
    return c;
}

export default InterviewRoomScene;