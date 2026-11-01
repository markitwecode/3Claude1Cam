# Codex with the Claude production environment

The current runbook is `CLAUDE.md`. The substantive role instructions remain in `.claude/agents/`; `.codex/agents/` contains only adapters for Codex tools and job handling. No Codex-only benchmark-derived teaching guidance is active. Previous instructions and the completed Lecture 6 experiment are preserved as historical artifacts, not inputs to new builds.

The current scene-model candidate is **GPT-6 Astra, medium reasoning**. The previous scene model was GPT-6.1 Sol at medium. The shared `vk build` default remains unchanged for the existing Claude workflow; Codex directors pass the model explicitly:

```sh
VK_JOB_GB=12 VK_GPU_SLOTS=1 VK_MANIM_SLOTS=6 engine/vk -C <new-project> build <scene> --model gpt-6-astra --effort medium --instructions /path/to/3Claude1Cam/.claude/agents/scene-builder.md
```

The model ID and medium reasoning setting are supported by [official OpenAI model documentation](https://developers.openai.com/api/docs/models/gpt-6-astra). Availability is checked separately; documentation alone does not establish scene quality.

Follow Claude's source ingestion, planning, writing, continuity, voice QA, director, scene review and final-render process. Match the engine, assets, instructions, normal review limits and resource caps across comparison arms. Read root `AGENTS.md` for platform mapping and RAM limits. Existing projects are read-only comparison artifacts; create new test folders. Do not import old benchmark findings or target scene implementations into workers' prompts.

For a builder-only experiment, freeze identical scripts, briefs, audio and timing manifests before running both models. That isolates scene building, not end-to-end authoring. An end-to-end comparison requires independent authoring from the same sources and is a different experiment. Lecture 6 is already a development example and cannot establish unseen generalization.

Freeze task inputs, role hashes and settings before generation; freeze outputs after the ordinary production reviews. Run a blind comparison only then. No comparison-driven repairs to the scored output. Preserve later development versions separately if improvements are requested. `.codex/parity-environment.json` records the current authoritative instruction hashes and candidate model setting.

Shared engineering fixes, such as recognizing concise implemented scenes rather than using an 80-line threshold, apply to both environments. The reduced Mac resource budget also applies to both. Platform tool names necessarily differ; substantive task instructions do not.
