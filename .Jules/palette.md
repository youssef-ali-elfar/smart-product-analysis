## 2025-05-15 - Accessible Workflow Descriptions
**Learning:** Mermaid diagrams in README files are not accessible to screen readers. Providing a structured text-based alternative (like a numbered list) ensures that all users can understand the documented processes.
**Action:** Always include a 'Workflow Description' or equivalent text section immediately following a Mermaid diagram to maintain accessibility standards.

## 2025-05-16 - Graceful CLI Interrupt Handling
**Learning:** CLI tools that do not handle `KeyboardInterrupt` (Ctrl+C) display messy stack traces to the user. Providing a clean exit message improves the "feel" of the tool and makes it appear more professional and stable.
**Action:** Always wrap the entry point of CLI applications in a `try...except KeyboardInterrupt` block to handle user cancellations gracefully.
