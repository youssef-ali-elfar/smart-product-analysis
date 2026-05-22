## 2025-05-15 - Accessible Workflow Descriptions
**Learning:** Mermaid diagrams in README files are not accessible to screen readers. Providing a structured text-based alternative (like a numbered list) ensures that all users can understand the documented processes.
**Action:** Always include a 'Workflow Description' or equivalent text section immediately following a Mermaid diagram to maintain accessibility standards.

## 2025-05-16 - Graceful CLI Interrupt Handling
**Learning:** CLI tools that do not handle `KeyboardInterrupt` (Ctrl+C) display messy stack traces to the user. Providing a clean exit message improves the "feel" of the tool and makes it appear more professional and stable.
**Action:** Always wrap the entry point of CLI applications in a `try...except KeyboardInterrupt` block to handle user cancellations gracefully.

## 2025-05-20 - CLI Roadmap and System Feedback
**Learning:** In data science CLI tools, users benefit from immediate confirmation of their environment (library versions) and a clear roadmap of the entire analysis pipeline. This builds trust and sets expectations before they even begin.
**Action:** Incorporate a "System Status" and a full "Roadmap" section in the tool's welcome message to orient users and confirm environment readiness.

## 2026-05-13 - Context-Aware CLI Onboarding
**Learning:** For multi-stage data analysis pipelines, checking for physical project structure (like a `data/` directory) is just as important as checking for dependencies. Users benefit from dynamic "Tips" that guide them specifically to the next setup step based on what's missing (dependencies first, then data).
**Action:** Implement proactive directory existence checks and use them to drive context-specific onboarding tips in CLI entry points.

## 2026-05-15 - Granular CLI Status Feedback
**Learning:** Binary "Found/Not Found" checks for directories can be misleading. A "Found" status on an empty data directory can lead to confusing downstream errors. Providing granular feedback (e.g., file counts) and warning states (YELLOW) for empty but existing directories significantly improves the onboarding experience.
**Action:** Use a three-tier status (Success/Warning/Error) for directory checks and include item counts to provide users with immediate, actionable context.

## 2026-05-18 - Dynamic Roadmap Progress
**Learning:** Transforming a static roadmap into a dynamic progress indicator using status tags (e.g., [DONE], [NEXT], [PEND]) provides users with immediate visual feedback on their current state in a multi-stage pipeline. This reduces cognitive load and clearly highlights the "next best action."
**Action:** Use a data-driven approach (e.g., a list of stages) and conditional logic to render roadmap statuses dynamically based on the application's environment state.

## 2026-05-20 - Multi-Metric CLI Status Feedback
**Learning:** Providing combined metrics (e.g., file count AND total size) for data directories gives users a much clearer picture of their environment readiness than a single count. Combining this with specific missing-dependency counts (e.g., "3 libraries missing") creates a highly actionable onboarding experience.
**Action:** When reporting on collections (files, dependencies), always provide both the count and a relevant secondary metric (like size or specific names) and ensure perfect grammatical pluralization.

## 2026-05-22 - Environment Context and Data Freshness
**Learning:** In Python-based data tools, explicitly displaying the environment type (Virtual Env vs Global) serves as a critical diagnostic that helps users avoid common dependency pitfalls. Additionally, providing "data freshness" (relative age of files) offers an implicit "liveness" indicator, building user confidence that they are working with the most recent datasets.
**Action:** Incorporate environment detection and file freshness (using relative time) into CLI status reports to provide deeper operational context.
