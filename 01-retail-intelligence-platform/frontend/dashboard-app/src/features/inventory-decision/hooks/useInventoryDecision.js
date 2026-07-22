import { useCallback, useEffect, useState } from "react";

import { fetchInventoryDecision } from "../api/inventoryDecisionApi.js";


export function useInventoryDecision() {
  const [requestId, setRequestId] = useState(0);
  const [state, setState] = useState({ status: "loading", data: null, error: null });

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading", data: null, error: null });
    fetchInventoryDecision({ signal: controller.signal })
      .then((data) => setState({ status: "connected", data, error: null }))
      .catch((error) => {
        if (error.name !== "AbortError") {
          setState({ status: "unavailable", data: null, error });
        }
      });
    return () => controller.abort();
  }, [requestId]);

  const retry = useCallback(() => setRequestId((current) => current + 1), []);
  return { ...state, retry };
}
