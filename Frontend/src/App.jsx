import ReactDOM from "react-dom/client";
import AudioRecorder from "./Components/AudioButton/AudioBtn";

const App = () => {
    return(
        <div><AudioRecorder/></div>
    )
}

const container = document.getElementById("root");
const root = ReactDOM.createRoot(container);

root.render(<App />);
