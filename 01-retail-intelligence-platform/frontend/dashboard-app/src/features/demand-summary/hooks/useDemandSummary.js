import { useCallback, useEffect, useState } from "react";

import { fetchDemandSummary } from "../api/demandSummaryApi.js";


export function useDemandSummary() {
  const [requestId, setRequestId] = useState(0);
  const [state, setState] = useState({
    status: "loading",
    data: null,
    error: null,
  });

  useEffect(() => {
    const controller = new AbortController();
    setState({ status: "loading", data: null, error: null });

    fetchDemandSummary({ signal: controller.signal })
      .then((data) => setState({ status: "success", data, error: null }))
      .catch((error) => {
        if (error.name !== "AbortError") {
          setState({ status: "error", data: null, error });
        }
      });

    return () => controller.abort();
  }, [requestId]);

  const retry = useCallback(() => setRequestId((current) => current + 1), []);

  return { ...state, retry };
}
