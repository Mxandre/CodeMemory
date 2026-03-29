# CodeMemory
CodeMemory - Give your code agent a persistent project memory

## ⭐ Why this design?
Modern code agents like **OpenAI Codex** or **Claude Code** are powerful -- but they are **stateless**.
They:
- Forget previous bug fixes
- Re-learn the same patterns repeatedly
- Ofen apply local patches instead of respecting project-wide design patterns

## 💢 Problem
When fixing bugs, agents usually:
- Only look at current files
- Ignore historical fixes
- Produce locally correct but globally inconsistent patches
- Sometimes bugs arise that cannot be detected without verification
  
## 💡 Solution
This project introduces a **local change memory layer**:
*A persisstent databse of **validated code changes**, accessible via MCP.*
With this, agents can :
- Recall the logic it modified before
- Learn the project's coding style whilst modifying the code
- Maintain consistency across the codebase
- Generate more logical and project-specific changes

## ⚖ Project Stucture
```text
CodeMemory/
├── README.md          # project documentation
├── LICENSE            # open-source license
├── mcp_server.py            # MCP server entry et MCP tool definitions
├── db.py          # SQLite logic
├── schema.sql           # DB schema
├── .debug_ai/
    └── =change_memory.db    # example of persistent memory
├── AGENTS.md       # example of agent instruction file
```
## 🗝 Provided MCP Tools
| Tool | Description |
|------|-------------|
| init_change_memory | Initialize local memory database|
| store_change | Store a validated change | 
| get_file_history_tool | Retrieve file-level history |
| get_symbol_history_tool | Retrieve function/class-level history|

##🔮 Workflow
```text
Bug occurs
   ↓
Agent retrieves history (MCP)
   ↓
Agent generates patch (guided by past patterns)
   ↓
Sandbox validation
   ↓
Store validated change
```

## 🧠 What gets stored?
Each validated change includes:
- file_path
- symbol
- change_reason
- change_summary
- timestamp

## 🔌 Integration with Codex
This project works with OpenAI Codex or Claude code via MCP.

## 🧪 Experiment

We compared bug fixing with and without change memory.

Result:
- Agents with memory reused existing patterns
- Agents without memory applied local patches

## 📈 Key Insight
> Code agents do not just need context——they need **history**

This project demonstrates that:
- Memory changes reasoning strategy, not just output
- Agents become more consistent, not just correct

