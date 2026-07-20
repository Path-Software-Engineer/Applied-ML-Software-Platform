import { useCallback, useEffect, useState } from "react";

import { fetchModelComparison } from "../api/modelComparisonApi.js";


export function useModelComparison() {
  const [requestId, setRequestId] = useState(0);
  const [state, setState] = useState({
    status: "loading",
    data: null,
    error: null,
  });

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading", data: null, error: null });

    fetchModelComparison({ signal: controller.signal })
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
