// Theme context — reactive light/dark state for The Stoa.
//
// Architecture (per agents/design/acb-001/design.md §2.1):
// - <ThemeProvider> owns React state for `dark`.
// - useTheme() returns { dark, toggle, setDark }.
// - On mount, initial state is read from <html data-theme="...">. The inline
//   bootstrap script in index.html has already set this attribute synchronously
//   before React mounts, so the lazy initializer always sees the correct value
//   (no FOUC, no flash).
// - Effect syncs `data-theme` on <html> and writes to localStorage on every change.
// - localStorage write is wrapped in try/catch (private browsing / quota safety).

import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";

type ThemeCtx = {
  dark: boolean;
  toggle: () => void;
  setDark: (d: boolean) => void;
};

const Ctx = createContext<ThemeCtx | null>(null);

export function ThemeProvider({ children }: { children: ReactNode }) {
  const [dark, setDarkState] = useState(
    () => document.documentElement.dataset.theme === "dark"
  );

  useEffect(() => {
    document.documentElement.dataset.theme = dark ? "dark" : "light";
    try {
      localStorage.setItem("acb-theme", dark ? "dark" : "light");
    } catch {
      // localStorage disabled / quota exceeded — silently noop. Choice still
      // applies for the current session via React state.
    }
  }, [dark]);

  const value: ThemeCtx = {
    dark,
    setDark: setDarkState,
    toggle: () => setDarkState((d) => !d),
  };
  return <Ctx.Provider value={value}>{children}</Ctx.Provider>;
}

export function useTheme(): ThemeCtx {
  const v = useContext(Ctx);
  if (!v) throw new Error("useTheme called outside ThemeProvider");
  return v;
}
