"use client";

import React, { FormEvent, useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { searchDocuments } from "../lib/api";

export default function SearchPanel() {
  const [query, setQuery] = useState("");
  const mutation = useMutation({
    mutationFn: searchDocuments,
  });

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!query.trim()) return;
    await mutation.mutateAsync({ query });
  };

  return (
    <section className="card">
      <p className="card__eyebrow">Search</p>
      <h2 style={{ marginTop: "0.25rem" }}>Find chunks</h2>
      <p style={{ color: "#9ea5b5" }}>Simple substring search over stored chunks (placeholder for full RAG).</p>
      <form onSubmit={handleSubmit} style={{ display: "flex", gap: "0.5rem", marginTop: "1rem" }}>
        <input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="Enter keywords"
          style={{
            flex: 1,
            padding: "0.6rem 1rem",
            borderRadius: "0.75rem",
            border: "1px solid #2c3140",
            background: "#11141b",
            color: "inherit",
          }}
        />
        <button
          type="submit"
          disabled={mutation.isPending}
          style={{
            padding: "0.6rem 1.2rem",
            borderRadius: "0.75rem",
            border: "none",
            background: mutation.isPending ? "#303849" : "#38bdf8",
            color: "#032136",
            fontWeight: 600,
          }}
        >
          {mutation.isPending ? "Searching..." : "Search"}
        </button>
      </form>
      {mutation.data && (
        <ul style={{ marginTop: "1rem", listStyle: "none", padding: 0 }}>
          {mutation.data.length === 0 && <li>No matches yet.</li>}
          {mutation.data.map((match) => (
            <li key={`${match.document_id}-${match.chunk_index}`} style={{ marginBottom: "0.5rem" }}>
              <small style={{ color: "#8d95a5" }}>Doc {match.document_id} • Chunk {match.chunk_index}</small>
              <p style={{ margin: 0 }}>{match.content}</p>
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}
