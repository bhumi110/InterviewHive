import { useNavigate } from "react-router-dom";


function Home() {

    const navigate = useNavigate();

    return (
        <div>

            <h1>
                AI Interview Room
            </h1>

            <p>
                Practice realistic technical interviews
                tailored to your resume.
            </p>

            <button
                onClick={() => navigate("/setup")}
            >
                Start Interview
            </button>

        </div>
    );
}


export default Home;