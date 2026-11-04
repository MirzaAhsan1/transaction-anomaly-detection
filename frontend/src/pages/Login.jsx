import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useSigninMutation } from "../api/authApi";
import useAuthStore from "../store/authStore";

export default function LoginPage() {
  const navigate = useNavigate();
  const setCredentials = useAuthStore((state) => state.setCredentials);

  const [email, setEmail] = useState("analyst@txnai.local");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");

  const [signin, { isLoading }] = useSigninMutation();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    try {
      const response = await signin({ email, password }).unwrap();

      setCredentials({
        accessToken: response.access_token,
        user: response.user,
      });

      navigate("/dashboard");
    } catch (err) {
      console.error("Login failed:", err);
      if (err?.data?.detail) {
        // backend may return validation details as an array of objects.
        // React cannot render objects directly.
        const detail = err.data.detail;
        if (Array.isArray(detail)) {
          const firstMsg = detail[0]?.msg;
          setError(firstMsg || "Login failed");
        } else if (typeof detail === "string") {
          setError(detail);
        } else {
          setError(detail?.msg || "Login failed");
        }
      } else {
        setError("Invalid email or password");
      }
    }
  };

  return (
    <div className="auth-container h-screen flex items-center justify-center w-full">
      <section className="auth-card w-full max-w-md">
        <div className="panel-header">
          <div>
            <h2>Login</h2>
            <p className="subtle-text">Access the fraud analysis workspace</p>
          </div>
        </div>

        <form onSubmit={handleLogin}>
          <label className="field">
            <span>Email</span>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
              required
            />
          </label>

          <label className="field">
            <span>Password</span>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
              required
            />
          </label>

          <div className="inline-row">
            <label>
              <input type="checkbox" defaultChecked /> Remember me
            </label>
            <a href="#">Forgot password?</a>
          </div>

          {error && <p style={{ color: "red", marginTop: "10px", marginBottom: "10px" }}>{error}</p>}

          <button type="submit" disabled={isLoading} className="primary-button mt-4">
            {isLoading ? "Signing in..." : "Sign in to dashboard"}
          </button>

          <p className="mt-4 text-center">
            Don't have an account? <Link to="/signup">Sign up</Link>
          </p>
        </form>
      </section>
    </div>
  );
}
