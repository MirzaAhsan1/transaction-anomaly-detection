// ==========================
// Authentication
// ==========================

export const AUTH_ENDPOINTS = {
  LOGIN: "/auth/login",
  SIGNUP: "/auth/signup", 
};

// ==========================
// Accounts
// ==========================

export const ACCOUNTS_ENDPOINTS = {
  VALIDATE: (accountNumber) => `/accounts/validate/${accountNumber}`,
};

// ==========================
// Transactions
// ==========================

export const TRANSACTION_ENDPOINTS = {
  CREATE: "/transactions/",
  GET_ALL: "/transactions/",
};


// ==========================
// Dashboard
// ==========================

export const DASHBOARD_ENDPOINTS = {
  STATS: "/dashboard/stats",
  RECENT_TRANSACTIONS: "/dashboard/recent-transactions",
  FRAUD_TREND: "/dashboard/fraud-trend",
  PAYMENT_METHODS: "/dashboard/payment-methods",
  DEVICE_DISTRIBUTION: "/dashboard/device-distribution",
  COUNTRY_DISTRIBUTION: "/dashboard/country-distribution",
};