import { TRANSACTION_ENDPOINTS } from "../constants/endpoints";
import { baseApi } from "./baseApi";

export const transactionApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    createTransaction: builder.mutation({
      query: (transactionData) => ({
        url: TRANSACTION_ENDPOINTS.CREATE,
        method: "POST",
        body: transactionData,
      }),
      invalidatesTags: ["Transaction", "Analytics"],
    }),
    getTransactions: builder.query({
      query: () => TRANSACTION_ENDPOINTS.GET_ALL,
      providesTags: ["Transaction"],
    }),
  }),
});

export const { useCreateTransactionMutation, useGetTransactionsQuery } = transactionApi;
