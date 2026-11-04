import { ACCOUNTS_ENDPOINTS } from "../constants/endpoints";
import { baseApi } from "./baseApi";

export const accountsApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    validateAccount: builder.query({
      query: (accountNumber) => ({
        url: ACCOUNTS_ENDPOINTS.VALIDATE(accountNumber),
        method: "GET",
      }),
    }),
  }),
});

export const { useValidateAccountQuery, useLazyValidateAccountQuery } = accountsApi;

