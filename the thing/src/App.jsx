import viteLogo from "./assets/audience.png";
import "./App.css";
import { useState } from "react";

function pcmEncode(input) {
  const output = new Uint8Array(input.length * 2);

  for (let i = 0; i < input.length; i++) {
    const index = i * 2;
    const sample = Math.max(-1, Math.min(1, input[i])) * 32767;
    output[index] = sample & 0xff;
    output[index + 1] = (sample >> 8) & 0xff;
  }

  return output;
}

let scriptProcessor;
let streamVar;
let pcmData = [];
let ws = new WebSocket("ws://localhost:5000");

async function audioRecord() {
  streamVar = await navigator.mediaDevices.getUserMedia({ audio: true });
  const audioContext = new AudioContext();
  const mediaStreamSource = audioContext.createMediaStreamSource(streamVar);
  scriptProcessor = audioContext.createScriptProcessor(4096, 1, 1);
  mediaStreamSource.connect(scriptProcessor);
  scriptProcessor.connect(audioContext.destination);

  scriptProcessor.onaudioprocess = function (event) {
    const inputBuffer = event.inputBuffer.getChannelData(0);
    pcmData.push(...inputBuffer);
  };

  setInterval(() => {
    const intData = new Int16Array(pcmData.length);
    for (let i = 0; i < pcmData.length; i++) {
      const sample = Math.max(-1, Math.min(1, pcmData[i]));
      intData[i] = sample < 0 ? sample * 0x8000 : sample * 0x7fff;
    }
    ws.send(intData);
    pcmData = [];
  }, 500);
}

function App() {
  const [getTxt, setGetTxt] = useState("");

  ws.onmessage = (eV) => {
    setGetTxt(eV.data);
  };

  return (
    <div className="App">
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
      </div>
      <h1>StudyBuddy.AI</h1>
      <div className="card">
        <button onClick={() => audioRecord()}>Start Recording</button>
        <button
          onClick={() => {
            scriptProcessor.disconnect();
            streamVar.getTracks().forEach((track) => track.stop());
            ws.send("Done");
          }}
        >
          Stop Recording
        </button>
      </div>
      <button>{getTxt == "" ? "Generating" : getTxt}</button>
    </div>
  );
}

export default App;
