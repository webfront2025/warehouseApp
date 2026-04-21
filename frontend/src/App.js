import { useState, useEffect } from "react";
import Dashboard from "./pages/Dashboard";
import Login from "./components/Login";


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem("token");
    setIsLoggedIn(!!token);
  }, []);

  return (
    <div className="App">
      {/* {isLoggedIn ? <Dashboard /> : <Login setIsLoggedIn={setIsLoggedIn} />}        20-04-2026    */}  
       {isLoggedIn ? (
        <Dashboard setIsLoggedIn={setIsLoggedIn} />
      ) : (
        <Login setIsLoggedIn={setIsLoggedIn} />
      )}
  
    </div>
  );
}

export default App;
