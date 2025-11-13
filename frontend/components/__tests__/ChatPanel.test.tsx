import React from "react";
import { fireEvent, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import ChatPanel from "../../components/ChatPanel";
import { renderWithClient } from "./test-utils";

const { mockedSendChat } = vi.hoisted(() => ({
  mockedSendChat: vi.fn().mockResolvedValue({ provider: "stub", answer: "ok" }),
}));

vi.mock("../../lib/api", () => ({
  sendChat: mockedSendChat,
}));

describe("ChatPanel", () => {
  beforeEach(() => {
    mockedSendChat.mockClear();
  });

  it("submits prompt and renders answer", async () => {
    renderWithClient(<ChatPanel />);

    const input = screen.getByLabelText(/prompt/i);
    fireEvent.change(input, { target: { value: "Ping" } });
    fireEvent.submit(input.closest("form")!);

    await waitFor(() => expect(mockedSendChat).toHaveBeenCalled());
    expect(mockedSendChat.mock.calls[0]?.[0]).toBe("Ping");
    expect(await screen.findByText(/ok/)).toBeInTheDocument();
  });
});
