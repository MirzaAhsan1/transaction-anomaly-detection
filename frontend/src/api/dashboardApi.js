import { DASHBOARD_ENDPOINTS } from "../constants/endpoints";
import { baseApi } from "./baseApi";

export const dashboardApi = baseApi.injectEndpoints({
  endpoints: (builder) => ({
    getDashboardStats: builder.query({
      query: () => DASHBOARD_ENDPOINTS.STATS,
      providesTags: ["Analytics"],
    }),
    getRecentTransactions: builder.query({
      query: () => DASHBOARD_ENDPOINTS.RECENT_TRANSACTIONS,
      providesTags: ["Transaction"],
    }),
    getFraudTrend: builder.query({
      query: () => DASHBOARD_ENDPOINTS.FRAUD_TREND,
      providesTags: ["Analytics"],
    }),
    getPaymentMethods: builder.query({
      query: () => DASHBOARD_ENDPOINTS.PAYMENT_METHODS,
      providesTags: ["Analytics"],
    }),
    getDeviceDistribution: builder.query({
      query: () => DASHBOARD_ENDPOINTS.DEVICE_DISTRIBUTION,
      providesTags: ["Analytics"],
    }),
    getCountryDistribution: builder.query({
      query: () => DASHBOARD_ENDPOINTS.COUNTRY_DISTRIBUTION,
      providesTags: ["Analytics"],
    }),
  }),
});

export const {
  useGetDashboardStatsQuery,
  useGetRecentTransactionsQuery,
  useGetFraudTrendQuery,
  useGetPaymentMethodsQuery,
  useGetDeviceDistributionQuery,
  useGetCountryDistributionQuery,
} = dashboardApi;
