/**
 * PixelWindow
 * A bordered panel with a dark titlebar (mac-style dots + label + meta),
 * matching the "COMMAND CENTER" panel language from the reference UI.
 *
 * Usage:
 *   <PixelWindow title="RESUME_UPLOAD" meta="step 1 / 2">
 *     ...content
 *   </PixelWindow>
 */
function PixelWindow({ title, meta, tight = false, children, className = "" }) {
    return (
        <section className={`pw ${className}`}>
            <header className="pw__titlebar">
                <span className="pw__dots">
                    <span />
                    <span />
                    <span />
                </span>
                <span className="pw__title">{title}</span>
                {meta && <span className="pw__meta">{meta}</span>}
            </header>

            <div className={`pw__body ${tight ? "pw__body--tight" : ""}`}>
                {children}
            </div>
        </section>
    );
}

export default PixelWindow;