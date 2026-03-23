import React, { useState } from 'react';
import "./Register.css";
import Header from '../Header/Header';

const Register = () => {
  const [userName, setUserName] = useState("");
  const [password, setPassword] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [open, setOpen] = useState(true);

  let register_url = window.location.origin + "/djangoapp/registration";

  const register = async (e) => {
    e.preventDefault();
    const res = await fetch(register_url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        userName,
        password,
        firstName,
        lastName,
        email,
      }),
    });
    const json = await res.json();
    if (json.status === "Authenticated") {
      sessionStorage.setItem("username", json.userName);
      setOpen(false);
    } else if (json.error === "Already Registered") {
      alert("User already registered. Please log in.");
    } else {
      alert("Registration failed. Please try again.");
    }
  };

  if (!open) {
    window.location.href = "/";
  }

  return (
    <div>
      <Header />
      <div className="register_container">
        <h1 className="header">Register</h1>
        <form onSubmit={register}>
          <div className="inputs">
            <div className="input">
              <img src={require("../assets/person.png")} className="img_icon" alt="Username" />
              <input
                type="text"
                placeholder="Username"
                className="input_field"
                onChange={(e) => setUserName(e.target.value)}
                required
              />
            </div>
            <div className="input">
              <img src={require("../assets/person.png")} className="img_icon" alt="First Name" />
              <input
                type="text"
                placeholder="First Name"
                className="input_field"
                onChange={(e) => setFirstName(e.target.value)}
                required
              />
            </div>
            <div className="input">
              <img src={require("../assets/person.png")} className="img_icon" alt="Last Name" />
              <input
                type="text"
                placeholder="Last Name"
                className="input_field"
                onChange={(e) => setLastName(e.target.value)}
                required
              />
            </div>
            <div className="input">
              <img src={require("../assets/email.png")} className="img_icon" alt="Email" />
              <input
                type="email"
                placeholder="Email"
                className="input_field"
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="input">
              <img src={require("../assets/password.png")} className="img_icon" alt="Password" />
              <input
                type="password"
                placeholder="Password"
                className="input_field"
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>
          <div className="submit_panel">
            <input type="submit" className="submit" value="Register" />
          </div>
        </form>
      </div>
    </div>
  );
};

export default Register;
