## 2025-05-14 - Friendly CLI Environment Checks
**Learning:** CLI applications often crash with cryptic `ModuleNotFoundError` when dependencies are missing. A more accessible and delightful UX is to catch these errors and provide clear, actionable instructions on how to resolve them. This prevents user frustration and lowers the barrier to entry for new users.
**Action:** Always wrap top-level imports of external libraries in a try-except block in the main entry point, and provide a helpful message suggesting the correct installation command.
