import type { Metadata } from "next";
import "./globals.css";
import Providers from "../components/Providers";
import { ReactNode } from "react";

export const metadata: Metadata = {
  title: "AI Workflow Platform",
  description: "Monitor backend health and chat with the agent",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body>
        <Providers>
          <main>{children}</main>
        </Providers>
      </body>
    </html>
  );
}
