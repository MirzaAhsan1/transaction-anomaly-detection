import { create } from "zustand";

const useTransactionStore = create((set) => ({
  search: "",

  riskLevel: "ALL",

  setSearch: (search) =>
    set({
      search,
    }),

  setRiskLevel: (riskLevel) =>
    set({
      riskLevel,
    }),

  resetFilters: () =>
    set({
      search: "",
      riskLevel: "ALL",
    }),
}));

export default useTransactionStore;