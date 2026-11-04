// @authApi.js
import { AUTH_ENDPOINTS } from "../constants/endpoints"; // Assuming endpoints.js is in the same directory
import { baseApi } from "./baseApi"; // Assuming baseApi.js is in the same directory

export const authApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    // Signin endpoint (from previous task)
    signin: builder.mutation({
      query: (credentials) => ({
        url: AUTH_ENDPOINTS.LOGIN,
        method: "POST",
        body: credentials,
      }),
    }),

    // Signup endpoint
    signUp: builder.mutation({
      query: (userData) => ({
        url: AUTH_ENDPOINTS.SIGNUP, // Use the SIGNUP endpoint constant
        method: "POST",
        body: userData, // Send user data in the request body
      }),
    }),
  }),
});

// Export hooks for usage in functional components
export const { useSigninMutation, useSignUpMutation } = authApi; // Added useSignUpMutation