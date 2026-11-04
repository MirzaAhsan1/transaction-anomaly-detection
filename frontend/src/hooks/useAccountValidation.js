import { useEffect, useState } from "react";
import { useLazyValidateAccountQuery } from "../api/accountsApi";

/**
 * Reusable hook for debounced account number validation.
 *
 * @param {string} accountNumber - The account number to validate.
 * @param {number} [debounceMs=800] - Debounce delay in milliseconds.
 * @returns {{ status: 'idle'|'loading'|'found'|'not_found'|'error', data: object|null }}
 *
 * Usage:
 *   const sender = useAccountValidation(formData.sender_account_number);
 *   const receiver = useAccountValidation(formData.receiver_account_number);
 *
 *   sender.status === 'found'    → ✔ Account Found
 *   sender.status === 'not_found'→ ❌ Account Not Found
 *   sender.status === 'loading'  → Checking...
 *   sender.status === 'idle'     → (no input yet)
 */
export function useAccountValidation(accountNumber, debounceMs = 800) {
  const [triggerValidate] = useLazyValidateAccountQuery();
  const [state, setState] = useState({ status: "idle", data: null });

  useEffect(() => {
    const trimmed = typeof accountNumber === "string" ? accountNumber.trim() : "";

    // Reset to idle when the field is cleared
    if (!trimmed) {
      setState({ status: "idle", data: null });
      return;
    }

    setState({ status: "loading", data: null });

    const timer = setTimeout(async () => {
      try {
        // RTK Query lazy trigger — goes through the same auth pipeline as all other API calls
        const result = await triggerValidate(trimmed).unwrap();

        if (result.exists) {
          setState({ status: "found", data: result });
        } else {
          setState({ status: "not_found", data: null });
        }
      } catch {
        setState({ status: "error", data: null });
      }
    }, debounceMs);

    return () => clearTimeout(timer);
  }, [accountNumber, debounceMs, triggerValidate]);

  return state;
}
