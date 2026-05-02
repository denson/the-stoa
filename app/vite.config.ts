/// <reference types="vitest/config" />
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "node",
    include: [
      "src/**/__tests__/**/*.test.ts",
      "scripts/**/__tests__/**/*.test.ts",
    ],
  },
});
