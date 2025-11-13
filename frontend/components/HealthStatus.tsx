"use client";

import React, { useEffect, useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchHealth } from "../lib/api";

export default function HealthStatus() {
  const [lastRefetch, setLastRefetch] = useState<Date | null>(null);
  const { data, isLoading, isError, refetch, isRefetching } = useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
    refetchInterval: 30_000,
  });

  useEffect(() => {
    if (data && !lastRefetch) {
      setLastRefetch(new Date());
    }
  }, [data, lastRefetch]);

  const handleRefresh = async () => {
    await refetch();
    const stamp = new Date();
    setLastRefetch(stamp);
    // eslint-disable-next-line no-console
    console.info("[health] manual refresh completed at", stamp.toISOString());
  };

  const statusTone = data?.status === "ok" ? "#34d399" : data?.status === "warn" ? "#fbbf24" : "#f87171";

  return (
    <section className="card" aria-live="polite">
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <p className="card__eyebrow">Backend status</p>
          <div className="card__title-row">
            <h2>Health</h2>
            {data && !isError && (
              <span className="status-pill" style={{ color: statusTone, background: `${statusTone}22` }}>
                <span className="status-dot" />
                {data.status.toUpperCase()}
              </span>
            )}
          </div>
        </div>
        <button
          onClick={handleRefresh}
          style={{
            padding: "0.5rem 1.1rem",
            borderRadius: "0.75rem",
            border: "none",
            background: isRefetching ? "#303849" : "#2563eb",
            color: "#fff",
            fontWeight: 600,
            minWidth: "120px",
          }}
          disabled={isRefetching}
        >
          {isRefetching ? "Refreshing…" : "Refresh"}
        </button>
      </header>
      <div style={{ marginTop: "1rem" }}>
        {(isLoading || isRefetching) && <p>Checking...</p>}
        {isError && <p style={{ color: "#f87171" }}>Unable to reach backend.</p>}
        {data && !isError && (
          <ul style={{ listStyle: "none", padding: 0, margin: 0, display: "grid", gap: "0.4rem" }}>
            <li>
              <strong>Status:</strong> {data.status}
            </li>
            <li>
              <strong>Detail:</strong> {data.detail}
            </li>
            {lastRefetch && (
              <li className="timestamp">
                Last manual refresh:{" "}
                <time dateTime={lastRefetch.toISOString()}>{lastRefetch.toLocaleTimeString()}</time>
              </li>
            )}
          </ul>
        )}
      </div>
    </section>
  );
}
