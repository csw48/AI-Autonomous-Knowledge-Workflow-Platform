import React from "react";
import { screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import HealthStatus from "../../components/HealthStatus";
import { renderWithClient } from "./test-utils";

const { mockedFetchHealth } = vi.hoisted(() => ({
  mockedFetchHealth: vi.fn().mockResolvedValue({ status: "ok", detail: "env=test" }),
}));

vi.mock("../../lib/api", () => ({
  fetchHealth: mockedFetchHealth,
}));

describe("HealthStatus", () => {
  beforeEach(() => {
    mockedFetchHealth.mockClear();
  });

  it("renders backend health info", async () => {
    renderWithClient(<HealthStatus />);

    await waitFor(() => expect(mockedFetchHealth).toHaveBeenCalled());
    expect(await screen.findByText(/env=test/)).toBeInTheDocument();
  });
});
