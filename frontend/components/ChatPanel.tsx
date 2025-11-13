"use client";

import React, { FormEvent, useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { ChatResponse, sendChat } from "../lib/api";

export default function ChatPanel() {
  const [prompt, setPrompt] = useState("Hello, what can you do?");
  const [history, setHistory] = useState<ChatResponse[]>([]);

  const mutation = useMutation({
    mutationFn: sendChat,
    onSuccess: (data) => {
      setHistory((prev) => [data, ...prev]);
    },
  });

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!prompt.trim()) return;
    await mutation.mutateAsync(prompt);
  };

  return (
    <section className="card">
      <header>
        <p style={{ margin: 0, color: "#8d95a5" }}>LLM stub</p>
        <h2 style={{ margin: "0 0 1rem" }}>Chat</h2>
      </header>
      <form onSubmit={onSubmit} style={{ display: "flex", gap: "0.5rem" }}>
        <input
          aria-label="Prompt"
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          style={{
            flex: 1,
            padding: "0.75rem 1rem",
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
            padding: "0.75rem 1.25rem",
            borderRadius: "0.75rem",
            border: "none",
            background: mutation.isPending ? "#4b5563" : "#16a34a",
            color: "#fff",
            minWidth: "120px",
          }}
        >
          {mutation.isPending ? "Sending" : "Ask"}
        </button>
      </form>

      <div style={{ marginTop: "1.5rem" }}>
        {history.length === 0 && <p>No messages yet.</p>}
        {history.map((item, index) => (
          <article key={`${item.answer}-${index}`} style={{ marginBottom: "1rem" }}>
            <p style={{ margin: 0, color: "#8d95a5" }}>Provider: {item.provider}</p>
            <p style={{ margin: 0 }}>{item.answer}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
