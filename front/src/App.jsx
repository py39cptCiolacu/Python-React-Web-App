import { useEffect, useState } from "react";

import "./App.css";
import Home from "./pages/Home";

function App() {
  const [ready, setReady] = useState(false);

  const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

  const checkReady = async () => {
    if (window.pywebview && window.pywebview.api) {
      setReady(true);
      return;
    }
    await sleep(10);
    checkReady();
  };

  useEffect(() => {
    checkReady();
  }, []);

  return !ready ? (
    <div className="h-screen w-full flex justify-center items-center">
      <div
        className="inline-block h-8 w-8 animate-spin rounded-full border-4 border-solid border-blue-400 border-current border-r-transparent align-[-0.125em] motion-reduce:animate-[spin_1.5s_linear_infinite]"
        role="status"
      >
        <span className="!absolute !-m-px !h-px !w-px !overflow-hidden !whitespace-nowrap !border-0 !p-0 ![clip:rect(0,0,0,0)]">
          Loading...
        </span>
      </div>
    </div>
  ) : (
    <Home />
  );
}

export default App;
