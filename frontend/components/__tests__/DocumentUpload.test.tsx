import React from "react";
import { fireEvent, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import DocumentUpload from "../../components/DocumentUpload";
import { renderWithClient } from "./test-utils";

const { mockUpload } = vi.hoisted(() => ({
  mockUpload: vi.fn().mockResolvedValue({ id: "1", title: "notes.txt", chunk_count: 2 }),
}));

vi.mock("../../lib/api", () => ({
  uploadDocument: mockUpload,
}));

describe("DocumentUpload", () => {
  beforeEach(() => {
    mockUpload.mockClear();
  });

  it("uploads selected file", async () => {
    renderWithClient(<DocumentUpload />);

    const fileInput = screen.getByLabelText(/file/i);
    const file = new File(["hello"], "notes.txt", { type: "text/plain" });
    fireEvent.change(fileInput, { target: { files: [file] } });

    fireEvent.click(screen.getByRole("button", { name: /upload/i }));

    await waitFor(() => expect(mockUpload).toHaveBeenCalled());
    expect(await screen.findByText(/uploaded notes.txt/i)).toBeInTheDocument();
  });
});
