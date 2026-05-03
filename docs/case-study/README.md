# Case study + KG visualization — drafts

Source content for the explanatory artifact aimed at the beadworks (`bw`) team. Two files, both feed two consumers:

- **Claude Design** — visual styling pass; produces handoff bundles
- **Claude Code** — production implementation in The Stoa app (`the-stoa/app/`)

## Files

| file | purpose | feeds |
|---|---|---|
| `case-study.md` | long-form narrative for peer-technical audience; 12 sections covering architecture, disciplines, worked example, hypergraph forward-look, engagement | Claude Design (mini-site layout) → in-app view at `/#/about` (or similar) |
| `kg-spec.md` | structured spec for the information-flow knowledge graph: nodes, edge types, decision points, loops, recursion, visualization modes | Claude Design (interactive prototype) → in-app component at `/#/architecture` (or similar) |

## Workflow

```
1. PRINCIPAL reviews drafts here
2. PRINCIPAL feeds approved drafts into Claude Design
3. Claude Design produces handoff bundles (HTML/CSS prototype + design system tokens)
4. Claude Code implements handoffs as React views/components in the-stoa/app/
5. POLYBIUS uses the production app to give live tours via the Chrome MCP
```

## Status

- `kg-spec.md` — draft 1 (this commit)
- `case-study.md` — draft 1 (this commit)
- Claude Design pass — pending PRINCIPAL review of drafts
- The Stoa app integration — pending Claude Design handoff
- POLYBIUS tour script (`substrate/templates/tour-script.md`) — not yet drafted; comes after the in-app views land so the tour can target real routes
