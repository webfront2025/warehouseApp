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
      {isLoggedIn ? <Dashboard /> : <Login />}
    </div>
  );
}

export default App;
