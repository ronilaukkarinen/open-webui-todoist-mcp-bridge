### 1.1.0: 2025-07-05

- Add Unicode support for international characters (ä, ö, etc.) with `ensure_ascii=False`
- Add model exclusion functionality to skip Todoist data injection for specific models/characters
- Add comprehensive debug logging
- Improve error handling with detailed exception tracking
- Remove hardcoded task filters for maximum flexibility
- Update function to get all current tasks and recent completed tasks (last 7 days)
- Enhance task data structure to include current date for temporal context
- Fix Unicode character encoding issues in task content
- Fix task data injection method to properly work with Open WebUI's inlet system
- Fix MCP endpoint usage to ensure compatibility with Todoist MCP server

### 1.0.0: 2025-07-05

- Initial release of Todoist MCP Bridge
- Add automatic injection of Todoist task data into Open WebUI conversations
- Add integration with Todoist MCP Proxy Server
- Add support for all current tasks, completed tasks, and projects
- Add language-agnostic task management capabilities
- Add basic error handling and API communication
- Bridge between Open WebUI and Todoist via MCP (Model Context Protocol)
- Support all Todoist task operations through MCP proxy
- Enable natural language task management in any language