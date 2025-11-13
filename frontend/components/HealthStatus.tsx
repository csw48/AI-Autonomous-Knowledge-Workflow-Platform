"use client";

import React, { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchHealth } from "../lib/api";

export default function HealthStatus() {
  const [lastRefetch, setLastRefetch] = useState<Date | null>(null);
  const { data, isLoading, isError, refetch, isRefetching } = useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
    refetchInterval: 30_000,
  });

  const handleRefresh = async () => {
    await refetch();
    const stamp = new Date();
    setLastRefetch(stamp);
    // Provide explicit signal in dev tools for easy debugging
    // eslint-disable-next-line no-console
    console.info("[health] manual refresh completed at", stamp.toISOString());
  };

  return (
    <section className="card" aria-live="polite">
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <p style={{ margin: 0, color: "#8d95a5" }}>Backend status</p>
          <h2 style={{ margin: 0 }}>Health</h2>
        </div>
        <button
          onClick={handleRefresh}
          style={{
            padding: "0.4rem 0.9rem",
            borderRadius: "999px",
            border: "none",
            background: "#3b82f6",
            color: "#fff",
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
          <ul style={{ listStyle: "none", padding: 0 }}>
            <li>
              <strong>Status:</strong> {data.status}
            </li>
            <li>
              <strong>Detail:</strong> {data.detail}
            </li>
            {lastRefetch && (
              <li style={{ color: "#8d95a5" }}>
                Last manual refresh: {lastRefetch.toLocaleTimeString()}
              </li>
            )}
          </ul>
        )}
      </div>
    </section>
  );
}
