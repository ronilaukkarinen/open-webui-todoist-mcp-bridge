# Changelog

All notable changes to the Open WebUI Todoist MCP Bridge will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-01-05

### Added
- Unicode support for international characters (ä, ö, etc.) with `ensure_ascii=False`
- Model exclusion functionality to skip Todoist data injection for specific models/characters
- Comprehensive debug logging with "TODOIST BRIDGE:" prefixes for troubleshooting
- Improved error handling with detailed exception tracking

### Changed
- Removed hardcoded task filters for maximum flexibility
- Updated function to get all current tasks and recent completed tasks (last 7 days)
- Enhanced task data structure to include current date for temporal context
- Improved documentation with detailed setup instructions

### Fixed
- Fixed Unicode character encoding issues in task content
- Fixed task data injection method to properly work with Open WebUI's inlet system
- Fixed MCP endpoint usage to ensure compatibility with Todoist MCP server

## [1.0.0] - 2025-01-05

### Added
- Initial release of Todoist MCP Bridge
- Automatic injection of Todoist task data into Open WebUI conversations
- Integration with Todoist MCP Proxy Server
- Support for all current tasks, completed tasks, and projects
- Language-agnostic task management capabilities
- Basic error handling and API communication

### Features
- Bridge between Open WebUI and Todoist via MCP (Model Context Protocol)
- Automatic task context injection using inlet method
- Support for all Todoist task operations through MCP proxy
- Natural language task management in any language