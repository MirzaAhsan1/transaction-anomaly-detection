import { create } from "zustand";

// 1. On app initialization, read the token from localStorage
const storedToken = localStorage.getItem("accessToken");
const storedUser = JSON.parse(localStorage.getItem("user") || "null");

const useAuthStore = create((set) => ({
  accessToken: storedToken,
  user: storedUser,
  isAuthenticated: !!storedToken,

  setCredentials: ({ accessToken, user }) => {
    // Persist JWT access token to localStorage
    localStorage.setItem("accessToken", accessToken);
    if (user) {
      localStorage.setItem("user", JSON.stringify(user));
    }
    set({
      accessToken,
      user,
      isAuthenticated: true,
    });
  },

  logout: () => {
    // Clear token from both localStorage and the store
    localStorage.removeItem("accessToken");
    localStorage.removeItem("user");
    set({
      accessToken: null,
      user: null,
      isAuthenticated: false,
    });
  },
}));

export default useAuthStore;