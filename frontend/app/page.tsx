import ChatPanel from "../components/ChatPanel";
import HealthStatus from "../components/HealthStatus";

export default function HomePage() {
  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}>
      <header>
        <p style={{ margin: 0, color: "#8d95a5" }}>AI Autonomous Knowledge & Workflow Platform</p>
        <h1 style={{ marginTop: "0.25rem" }}>Ops dashboard</h1>
        <p style={{ color: "#9ea5b5", maxWidth: "640px" }}>
          Monitor backend health, sanity-check the LLM stub, and get confidence that the platform is live.
        </p>
      </header>
      <HealthStatus />
      <ChatPanel />
    </div>
  );
}
