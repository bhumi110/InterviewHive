import { BrowserRouter, Routes, Route } from "react-router-dom";

import "./index.css";
import "./pixi/pixi.css";

import Home from "./pages/Home";
import Setup from "./pages/Setup";
import Interview from "./pages/Interview";
import Report from "./pages/Report";


function App() {

    return (
        <BrowserRouter>

            <Routes>

                <Route
                    path="/"
                    element={<Home />}
                />

                <Route
                    path="/setup"
                    element={<Setup />}
                />

                <Route
                    path="/interview"
                    element={<Interview />}
                />

                <Route
                    path="/report"
                    element={<Report />}
                />

            </Routes>

        </BrowserRouter>
    );
}


export default App;