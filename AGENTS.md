# Codex video studio — Claude-matched environment

The authoritative production process is CLAUDE.md and the authoritative role bodies are .claude/agents/*.md. Preserve those files and all existing project outputs. .codex/agents/*.md are platform adapters, not separate creative or quality instructions.

The main session is the producer. Delegate planning, chapter writing and direction as documented in CLAUDE.md, with paths and decisions rather than source dumps. Assigned workers perform only their assigned role. Translate Claude tool names to available Codex tools. Keep state in project files; inspect vk status and STATUS.md before resuming. Queue collaboration work within the available slots and use at most two active chapter directors.

## Current model test
Scene builders and fix workers use GPT-6 Astra at medium reasoning, explicitly via `vk build --model gpt-6-astra --effort medium --instructions <absolute studio>/.claude/agents/scene-builder.md`. The shared vk build default is unchanged so the existing Claude workflow is preserved. Planning/writing/direction use the session model unless explicitly assigned otherwise; record it where observable, never infer a historical session model from current CLI config.

Use the same engine, assets, reference material, task instructions and normal review/fix limits as Claude. Remove Codex-only benchmark-derived guidance from active roles. Do not read the previous Codex comparison findings to guide a new build. Use fresh project folders; existing Claude and Codex projects are read-only comparison artifacts. In a builder-only test, identical frozen scripts, briefs, voice audio and timing manifests may be supplied to both arms: that tests the builder, not end-to-end authoring. Do not copy target scene implementations or give workers comparison-driven repair notes.

Freeze the protocol, role-file hashes, task inputs and model settings before generation. Run the ordinary production checks equally in both arms. Freeze completed outputs before the blind comparison. Comparison results are measurement only: no post-score fixes to the scored version. Any later development version must be separate and reported as tuned. Lecture 6 has already informed development and is not an unseen generalization test.

## Shared Mac limits
Apply the same resource caps to every comparison arm: `VK_JOB_GB=12 VK_GPU_SLOTS=1 VK_MANIM_SLOTS=6`. At most three builders per director, six total; keep engine memory locks active. One voice job at a time, and no voice alongside lecture transcription. Check memory pressure and swap before heavy batches, holding new heavy work at warning pressure. Never terminate other apps or remove existing artifacts for headroom.

Read docs/LESSONS.md before engine changes. Shared engineering fixes (including status detection for concise scenes) apply to both environments; they do not supply extra teaching guidance. Keep normal source, audio, visual and final reviews as Claude documents them. Confirm review claims against actual frames/source material.
