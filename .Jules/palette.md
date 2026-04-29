## 2025-05-15 - Accessible Workflow Descriptions
**Learning:** Mermaid diagrams in README files are not accessible to screen readers. Providing a structured text-based alternative (like a numbered list) ensures that all users can understand the documented processes.
**Action:** Always include a 'Workflow Description' or equivalent text section immediately following a Mermaid diagram to maintain accessibility standards.

## 2025-05-16 - Graceful CLI Interrupt Handling
**Learning:** CLI tools that do not handle `KeyboardInterrupt` (Ctrl+C) display messy stack traces to the user. Providing a clean exit message improves the "feel" of the tool and makes it appear more professional and stable.
**Action:** Always wrap the entry point of CLI applications in a `try...except KeyboardInterrupt` block to handle user cancellations gracefully.

## 2025-05-20 - CLI Roadmap and System Feedback
**Learning:** In data science CLI tools, users benefit from immediate confirmation of their environment (library versions) and a clear roadmap of the entire analysis pipeline. This builds trust and sets expectations before they even begin.
**Action:** Incorporate a "System Status" and a full "Roadmap" section in the tool's welcome message to orient users and confirm environment readiness.

## 2025-05-25 - Resilient CLI Initialization
**Learning:** CLI tools in environments with many optional dependencies (like data science) should not fail to start just because a library is missing. Providing a high-level status report even when dependencies are incomplete allows users to diagnose environment issues without deciphering stack traces.
**Action:** Use defensive import patterns and dynamic version checking to ensure the CLI's help and status commands always remain accessible.
