# Change Memory Workflow

This project uses a local MCP tool called `change_memory`.

## Rules

1. Before modifying any file:
   - Call `get_file_history_tool` with the file path
   - Review recent validated changes

2. If a specific function or class is being modified:
   - Call `get_symbol_history_tool`

3. Use retrieved change summaries as context before generating patches.

4. After a patch passes sandbox or validation:
   - Call `store_change` to save:
     - file_path
     - symbol_type
     - symbol
     - change_reason
     - change_summary

5. Never store unvalidated or failed changes.

6. Prefer recent changes and same-symbol history.

7. Always consult change-memory MCP tools before editing any file.

8. When change memory indicates an existing validated pattern for input normalization or boundary handling, prefer extending that pattern consistently over making a purely local patch, as long as validation still passes.

9. Do not default to the smallest local fix if a recent validated change suggests a broader project-level consistency rule.
