"use client";

import React, { FormEvent, useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { ChatResponse, RagChatResponse, sendChat, sendRagChat } from "../lib/api";

export default function ChatPanel() {
  const [prompt, setPrompt] = useState("Hello, what can you do?");
  const [useRag, setUseRag] = useState(false);
  const [history, setHistory] = useState<(ChatResponse | RagChatResponse)[]>([]);

  const mutation = useMutation({
    mutationFn: async (payload: { prompt: string; useRag: boolean }) => {
      if (payload.useRag) {
        return sendRagChat(payload.prompt);
      }
      return sendChat(payload.prompt);
    },
    onSuccess: (data) => {
      setHistory((prev) => [data, ...prev]);
    },
  });

  const onSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!prompt.trim()) return;
    await mutation.mutateAsync({ prompt, useRag });
  };

  return (
    <section className="card">
      <header>
        <p style={{ margin: 0, color: "#8d95a5" }}>LLM stub / RAG</p>
        <h2 style={{ margin: "0 0 1rem" }}>Chat</h2>
      </header>
      <form onSubmit={onSubmit} style={{ display: "flex", flexDirection: "column", gap: "0.75rem" }}>
        <input
          aria-label="Prompt"
          value={prompt}
          onChange={(event) => setPrompt(event.target.value)}
          style={{
            padding: "0.75rem 1rem",
            borderRadius: "0.75rem",
            border: "1px solid #2c3140",
            background: "#11141b",
            color: "inherit",
          }}
        />
        <div style={{ display: "flex", alignItems: "center", gap: "0.75rem" }}>
          <label style={{ display: "flex", alignItems: "center", gap: "0.35rem", color: "#9ea5b5" }}>
            <input
              type="checkbox"
              checked={useRag}
              onChange={(event) => setUseRag(event.target.checked)}
            />
            <span>Use RAG over uploaded documents</span>
          </label>
          <button
            type="submit"
            disabled={mutation.isPending}
            style={{
              marginLeft: "auto",
              padding: "0.75rem 1.25rem",
              borderRadius: "0.75rem",
              border: "none",
              background: mutation.isPending ? "#4b5563" : "#16a34a",
              color: "#fff",
              minWidth: "120px",
            }}
          >
            {mutation.isPending ? "Sending" : useRag ? "Ask (RAG)" : "Ask"}
          </button>
        </div>
      </form>

      <div style={{ marginTop: "1.5rem" }}>
        {history.length === 0 && <p>No messages yet.</p>}
        {history.map((item, index) => (
          <article key={`${item.answer}-${index}`} style={{ marginBottom: "1rem" }}>
            <p style={{ margin: 0, color: "#8d95a5" }}>Provider: {item.provider}</p>
            <p style={{ margin: "0.25rem 0" }}>{item.answer}</p>
            {"contexts" in item && item.contexts.length > 0 && (
              <ul style={{ margin: "0.5rem 0 0", paddingLeft: "1rem", color: "#9ea5b5", fontSize: "0.85rem" }}>
                {item.contexts.slice(0, 3).map((ctx, ctxIndex) => (
                  <li key={`${ctx.document_id}-${ctx.chunk_index}-${ctxIndex}`}>
                    [{ctx.chunk_index}] {ctx.content}
                  </li>
                ))}
              </ul>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
