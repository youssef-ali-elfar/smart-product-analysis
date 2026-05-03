## 2025-05-15 - Accessible Workflow Descriptions
**Learning:** Mermaid diagrams in README files are not accessible to screen readers. Providing a structured text-based alternative (like a numbered list) ensures that all users can understand the documented processes.
**Action:** Always include a 'Workflow Description' or equivalent text section immediately following a Mermaid diagram to maintain accessibility standards.

## 2025-05-16 - Graceful CLI Interrupt Handling
**Learning:** CLI tools that do not handle `KeyboardInterrupt` (Ctrl+C) display messy stack traces to the user. Providing a clean exit message improves the "feel" of the tool and makes it appear more professional and stable.
**Action:** Always wrap the entry point of CLI applications in a `try...except KeyboardInterrupt` block to handle user cancellations gracefully.

## 2025-05-20 - CLI Roadmap and System Feedback
**Learning:** In data science CLI tools, users benefit from immediate confirmation of their environment (library versions) and a clear roadmap of the entire analysis pipeline. This builds trust and sets expectations before they even begin.
**Action:** Incorporate a "System Status" and a full "Roadmap" section in the tool's welcome message to orient users and confirm environment readiness.

## 2026-05-03 - CLI Scannability and Defensive Status
**Learning:** In terminal-based tools, vertical alignment of information (e.g., aligning colons in a status list) significantly improves scannability and professional feel. Furthermore, providing defensive "Not Found" statuses for expected dependencies (with color cues) prevents crashes and helps users troubleshoot environment issues immediately.
**Action:** Use a standardized label padding (15 chars) for all key-value pairs in CLI reports and implement `try...except` version checking for all external dependencies to ensure status reporting remains functional even in broken environments.
