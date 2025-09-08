import { useState } from "react";
import { apiRequest } from "./api";

function App() {
  const [form, setForm] = useState({ username: "", email: "", password: "" });
  const [loggedIn, setLoggedIn] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const register = async () => {
    const data = await apiRequest("/users/register/", "POST", form, false);
    console.log(data);
    alert(JSON.stringify(data));
  };

  const login = async () => {
    const data = await apiRequest("/users/login/", "POST", form, false);
    if (data.token) {
      localStorage.setItem("token", data.token);
      setLoggedIn(true);
    }
    console.log(data);
    alert(JSON.stringify(data));
  };

  return (
    <div style={{ padding: 20 }}>
      <h1>Inventory Frontend</h1>

      <h2>{loggedIn ? "✅ Logged In" : "🔒 Not Logged In"}</h2>

      <input
        type="text"
        name="username"
        placeholder="Username"
        onChange={handleChange}
      />
      <br />
      <input
        type="email"
        name="email"
        placeholder="Email"
        onChange={handleChange}
      />
      <br />
      <input
        type="password"
        name="password"
        placeholder="Password"
        onChange={handleChange}
      />
      <br />
      <button onClick={register}>Register</button>
      <button onClick={login}>Login</button>
    </div>
  );
}

export default App;