

// @SignUp.jsx
import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useSignUpMutation } from "../api/authApi"; // Adjust the import path as needed


function SignUpPage() {
  const navigate = useNavigate();
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [email, setEmail] = useState("");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // RTK Query hook for sign-up
  const [signup, { isLoading }] = useSignUpMutation();

  const handleSignUp = async (e) => {
    e.preventDefault();
    setError(""); // Clear previous errors

    try {
      // Call the signup mutation with user data
      const response = await signup({
        first_name: firstName,
        last_name: lastName,
        email: email,
        username: username,
        password: password,
      }).unwrap(); // .unwrap() handles promise resolution/rejection

      // Handle successful sign-up
      console.log("Sign up successful:", response);
      // Assuming a successful signup redirects to the login page or a confirmation page
      navigate("/login"); // Redirect to login page after successful signup

    } catch (err) {
      // Handle sign-up errors
      console.error("Sign up failed:", err);

      // Display specific error message from backend if available
      if (err?.data?.detail) {
        // backend may return validation details as an array of objects.
        // React cannot render objects directly.
        const detail = err.data.detail;
        if (Array.isArray(detail)) {
          const firstMsg = detail[0]?.msg;
          setError(firstMsg || "Sign up failed");
        } else if (typeof detail === "string") {
          setError(detail);
        } else {
          setError(detail?.msg || "Sign up failed");
        }
      } else {
        setError("An unexpected error occurred. Please try again.");
      }
    }
  };

  return (
    <div className="auth-container h-screen flex items-center justify-center w-full">
      <section className="auth-card w-full">
        <div className="panel-header">
          <div>
            <h2>Create account</h2>
            <p className="subtle-text">Register a new fraud analyst profile</p>
          </div>
        </div>
        <form onSubmit={handleSignUp}>
          <div className="field">
            <label htmlFor="firstName">First Name:</label>
            <input
              type="text"
              id="firstName"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div className="field">
            <label htmlFor="lastName">Last Name:</label>
            <input
              type="text"
              id="lastName"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div className="field">
            <label htmlFor="email">Email:</label>
            <input
              type="email"
              id="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div className="field">
            <label htmlFor="username">Username:</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div className="field">
            <label htmlFor="password">Password:</label>
            <input
              type="password"
              id="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>

          {/* Display error message if any */}
          {error && <p style={{ color: "red" }}>{error}</p>}

          <button type="submit" disabled={isLoading} className="primary-button">
            {isLoading ? "Signing up..." : "Sign up"}
          </button>
          <p className="mt-4 text-center">
            Already have an account? <Link to="/login">Sign in</Link>
          </p>
        </form>
      </section>
    </div>
  );
}

export default SignUpPage;