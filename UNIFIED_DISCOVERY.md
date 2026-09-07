# Unified Discovery Layer

This MVP turns multiple conversations into a graph and identifies candidate relationships for deeper reasoning.

```text
Chats
  ↓
Concept extraction
  ↓
Pairwise relation graph
  ↓
Complementarity ranking
  ↓
Hypothesis generation
  ↓
Contradiction signals
  ↓
Evidence / model-based validation (next stage)
  ↓
Execution through Nexus
```

## Connection to the existing ecosystem

- **MART / Meta-Attention:** confidence and self-critique layer.
- **Graph projects:** persistent concept/relation memory.
- **ReasonSynth / Prometheus-style work:** hypothesis and reasoning experiments.
- **Nexus Executor:** action/execution layer.
- **DiscoveryOS concept:** orchestration of the complete loop.

## Current test status

The deterministic core was executed locally with **3/3 tests passing**. The tests establish that related conversations rank above an unrelated control, that graph relations become hypotheses, and that the contradiction baseline is explicit rather than presented as semantic truth.

## Important limitation

This is a baseline, not proof that the unified theory is correct. Lexical Jaccard overlap can miss semantic relationships and can also create false positives. The next scientific test should compare this baseline against embeddings and an LLM/NLI judge on a human-labeled dataset, reporting precision@k, recall@k, calibration, and contradiction-detection accuracy.
