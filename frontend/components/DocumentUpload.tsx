"use client";

import React, { FormEvent, useState } from "react";
import { useMutation } from "@tanstack/react-query";

import { uploadDocument } from "../lib/api";

export default function DocumentUpload() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [title, setTitle] = useState("");
  const [status, setStatus] = useState<string | null>(null);

  const mutation = useMutation({
    mutationFn: ({ file, title }: { file: File; title?: string }) => uploadDocument(file, title),
    onSuccess: (data) => {
      setStatus(`Uploaded ${data.title} (chunks: ${data.chunk_count})`);
      setSelectedFile(null);
      setTitle("");
    },
    onError: (error: Error) => {
      setStatus(error.message);
    },
  });

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!selectedFile) {
      setStatus("Please pick a file first.");
      return;
    }

    await mutation.mutateAsync({ file: selectedFile, title: title || undefined });
  };

  return (
    <section className="card" aria-live="polite">
      <p className="card__eyebrow">Documents</p>
      <h2 style={{ marginTop: "0.25rem" }}>Upload</h2>
      <p style={{ color: "#9ea5b5", marginTop: "0.5rem" }}>
        Upload a document (text, PDF, DOCX or image) to index it for later RAG processing. Chunking and optional OCR
        happen on the server.
      </p>
      <form onSubmit={handleSubmit} style={{ display: "grid", gap: "0.75rem", marginTop: "1rem" }}>
        <label style={{ display: "grid", gap: "0.35rem", color: "#9ea5b5" }}>
          <span>Document file (text, PDF, DOCX, image)</span>
          <input
            type="file"
            aria-label="Document file"
            accept=".txt,.pdf,.docx,image/*"
            onChange={(event) => {
              const file = event.target.files?.[0];
              setSelectedFile(file ?? null);
            }}
            style={{ color: "inherit" }}
          />
        </label>
        <input
          type="text"
          placeholder="Optional title override"
          value={title}
          onChange={(event) => setTitle(event.target.value)}
          style={{
            padding: "0.65rem 0.9rem",
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
            border: "none",
            borderRadius: "0.75rem",
            padding: "0.75rem 1.25rem",
            background: mutation.isPending ? "#303849" : "#4ade80",
            color: "#051607",
            fontWeight: 600,
          }}
        >
          {mutation.isPending ? "Uploading…" : "Upload"}
        </button>
      </form>
      {status && (
        <p style={{ marginTop: "0.75rem", color: mutation.isError ? "#f87171" : "#34d399" }}>{status}</p>
      )}
    </section>
  );
}
