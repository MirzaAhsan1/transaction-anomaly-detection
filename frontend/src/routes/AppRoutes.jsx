import { Navigate, Route, Routes } from "react-router-dom";

import DashboardLayout from "../layouts/DashboardLayout";
import DashboardPage from "../pages/Dashboard";
import EmailsPage from "../pages/Emails";
import FraudDetectionPage from "../pages/FraudDetection";
import LoginPage from "../pages/Login";
import NewTransactionPage from "../pages/NewTransaction";
import ProfilePage from "../pages/Profile";
import ReportsPage from "../pages/Reports";
import TransactionDetailsPage from "../pages/TransactionDetails";
import TransactionsPage from "../pages/Transactions";
import UsersPage from "../pages/Users";
import ProtectedRoute from "./ProtectedRoute";
import PublicRoute from "./PublicRoute";
import SignUpPage from "../pages/SignUp";

export default function AppRoutes() {
  return (
    <Routes>
      {/* Public/Auth Routes - Redirect to dashboard if logged in */}
      <Route element={<PublicRoute />}>
        <Route path="login" element={<LoginPage />} />
        <Route path="signin" element={<SignUpPage />} />
        <Route path="signup" element={<SignUpPage />} />
      </Route>

      {/* Protected Routes - Redirect to login if not logged in */}
      <Route element={<ProtectedRoute />}>
        <Route element={<DashboardLayout />}>
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="fraud" element={<FraudDetectionPage />} />
          <Route path="new-transaction" element={<NewTransactionPage />} />
          <Route path="transactions" element={<TransactionsPage />} />
          <Route path="transaction-details" element={<TransactionDetailsPage />} />
          <Route path="reports" element={<ReportsPage />} />
          <Route path="users" element={<UsersPage />} />
          <Route path="emails" element={<EmailsPage />} />
          <Route path="profile" element={<ProfilePage />} />
        </Route>
      </Route>

      {/* Fallback routing */}
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  );
}
