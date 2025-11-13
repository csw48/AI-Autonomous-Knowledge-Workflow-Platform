"use client";

import React from "react";
import { useQuery } from "@tanstack/react-query";
import { fetchHealth } from "../lib/api";

export default function HealthStatus() {
  const { data, isLoading, isError, refetch } = useQuery({
    queryKey: ["health"],
    queryFn: fetchHealth,
    refetchInterval: 30_000,
  });

  return (
    <section className="card" aria-live="polite">
      <header style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <div>
          <p style={{ margin: 0, color: "#8d95a5" }}>Backend status</p>
          <h2 style={{ margin: 0 }}>Health</h2>
        </div>
        <button
          onClick={() => refetch()}
          style={{
            padding: "0.4rem 0.9rem",
            borderRadius: "999px",
            border: "none",
            background: "#3b82f6",
            color: "#fff",
          }}
        >
          Refresh
        </button>
      </header>
      <div style={{ marginTop: "1rem" }}>
        {isLoading && <p>Checking...</p>}
        {isError && <p style={{ color: "#f87171" }}>Unable to reach backend.</p>}
        {data && (
          <ul style={{ listStyle: "none", padding: 0 }}>
            <li>
              <strong>Status:</strong> {data.status}
            </li>
            <li>
              <strong>Detail:</strong> {data.detail}
            </li>
          </ul>
        )}
      </div>
    </section>
  );
}
