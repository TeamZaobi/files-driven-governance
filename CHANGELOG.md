# Changelog

All notable changes to `files-driven` are recorded here.

## v0.2.4 - 2026-03-24

### Added

- Added `references/document-lifecycle-and-compaction.md` to formalize lifecycle states, compaction triggers, and archive strategy for bloated docs.
- Added `docs/DOCUMENT_BLOAT_INQUIRY_ROUND_1.md` to record a first explicit inquiry-reflection-convergence round on document bloat governance.
- Added `docs/RELEASE_NOTES_v0.2.4.md` for the document-bloat patch release notes.

### Changed

- Extended `SKILL.md` to recognize documentation sprawl as a diagnosis dimension and to activate lifecycle/compaction strategy when retrieval cost rises.
- Extended `references/output-contract.md` with a conditional `文档生命周期与压缩策略` section.
- Extended `references/classic-governance-flows.md` and `references/scenario-playbooks.md` with `growth_signal -> lifecycle_review -> compact_or_archive`.
- Updated `README.md`, `docs/MANUAL.md`, and `docs/REPO_METADATA.md` for `v0.2.4`.

## v0.2.3 - 2026-03-24

### Added

- Added `docs/RELEASE_NOTES_v0.2.3.md` for the precision-first patch release notes.

### Changed

- Changed `SKILL.md` to output a precision-first governance blueprint using `core required + conditional sections` instead of always emitting the full governance contract.
- Changed `references/output-contract.md` to separate core sections from conditional sections and add activation hints for advanced sections.
- Updated `README.md`, `docs/MANUAL.md`, `docs/REPO_METADATA.md`, and `agents/openai.yaml` for `v0.2.3` and the precision-first positioning.

## v0.2.2 - 2026-03-24

### Added

- Added `references/understanding-confidence-and-clarification.md` to formalize confidence-gated clarification before locking a governance diagnosis.
- Added `docs/RELEASE_NOTES_v0.2.2.md` for the patch release notes.

### Changed

- Extended `SKILL.md` to treat `OpenClaw` as a first-class multi-tool entrypoint in adapter guidance.
- Extended `SKILL.md`, `references/output-contract.md`, and `references/core-doctrine.md` to require understanding-confidence checks and targeted clarification questions when project basics remain ambiguous.
- Extended `references/tool-adapter-matrix.md`, `references/official-retrieval-orders.md`, and `references/cross-layer-sharing-contract.md` to cover `OpenClaw` as an explicit adapter or launcher surface.
- Updated `README.md`, `docs/MANUAL.md`, `docs/REPO_METADATA.md`, and `agents/openai.yaml` for `v0.2.2`.

## v0.2.1 - 2026-03-24

### Added

- Added `references/family-locator-contract.md` to define canonical locators, current-version anchors, and fallback rules for `policy_or_rules`、`object`、`workflow`、`skill`、`agent`.
- Added `references/official-retrieval-orders.md` to formalize cross-tool read order for the five core families.
- Added `references/tool-adapter-matrix.md` to separate tool adapters from canonical family sources.
- Added `docs/RELEASE_NOTES_v0.2.1.md` for the patch release notes.

### Changed

- Extended `SKILL.md`, `README.md`, `docs/MANUAL.md`, `references/output-contract.md`, and `references/core-doctrine.md` to make family retrieval readiness and tool-adapter design explicit.

## v0.2.0 - 2026-03-24

### Added

- Added `references/classic-governance-flows.md` to formalize the reusable flow library distilled from AIJournal and HQMDClaw.
- Added `references/adversarial-convergence-loop.md` to make hostile inquiry, defense, and convergence a first-class mechanism.
- Added `docs/RELEASE_NOTES_v0.2.0.md` for GitHub-facing release notes.

### Changed

- Upgraded `SKILL.md` from structure-only guidance to structure plus flow-library selection.
- Upgraded the output contract to require `推荐经典流程库`.
- Expanded scenario playbooks to recommend default and conditional flow sets by start state.
- Expanded shared-patterns guidance with reusable classic flows and a clearer development arc from HQMDClaw to AIJournal.
- Updated `README.md`, `docs/MANUAL.md`, `docs/REPO_METADATA.md`, and `agents/openai.yaml` for the new positioning and release language.

### Notes

- `files-driven` now explicitly treats `discussion -> decision_package -> task_or_decision`, `mechanism_review`, `adversarial_inquiry -> defense -> convergence`, and `proposal -> validation -> rollout -> activation_or_rollback` as selectable governance flows rather than incidental habits.

## v0.1.0 - 2026-03-24

### Added

- Initial public release of the `files-driven` project structure governance skill.
- Core doctrine, strategy matrix, cross-layer sharing contract, output contract, scenario playbooks, and multi-tool team practices.
- GitHub packaging, repository manual, contribution docs, and metadata templates.
