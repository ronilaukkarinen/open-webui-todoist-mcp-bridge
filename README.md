# Open WebUI Todoist MCP Bridge

![Open WebUI](https://img.shields.io/badge/Open%20WebUI-222222?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyBmaWxsPSIjZmZmZmZmIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiIGhlaWdodD0iMWVtIiBzdHlsZT0iZmxleDpub25lO2xpbmUtaGVpZ2h0OjEiIHZpZXdCb3g9IjAgMCAyNCAyNCIgd2lkdGg9IjFlbSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48cGF0aCBjbGlwLXJ1bGU9ImV2ZW5vZGQiIGQ9Ik0xNy42OTcgMTJjMCA0Ljk3LTMuOTYyIDktOC44NDkgOUMzLjk2MiAyMSAwIDE2Ljk3IDAgMTJzMy45NjItOSA4Ljg0OC05YzQuODg3IDAgOC44NDkgNC4wMyA4Ljg0OSA5em0tMy42MzYgMGMwIDIuOTI4LTIuMzM0IDUuMzAxLTUuMjEzIDUuMzAxLTIuODc4IDAtNS4yMTItMi4zNzMtNS4yMTItNS4zMDFTNS45NyA2LjY5OSA4Ljg0OCA2LjY5OWMyLjg4IDAgNS4yMTMgMi4zNzMgNS4yMTMgNS4zMDF6Ij48L3BhdGg+PHBhdGggZD0iTTI0IDNoLTMuMzk0djE4SDI0VjN6Ij48L3BhdGg+PC9zdmc+Cg==)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Version](https://img.shields.io/badge/version-1.1.0-blue?style=for-the-badge)

A powerful Open WebUI Function that bridges your Todoist tasks with AI conversations through Model Context Protocol (MCP). This function automatically injects your current tasks, completed tasks, and projects into conversations, enabling natural task management in any language.

![Screenshot from 2025-07-05 21-18-19](https://github.com/user-attachments/assets/2dc4043d-2241-481a-9cb2-9fad3c63fbd4)

## 🌟 Features

- **Automatic Task Context**: Your Todoist data is automatically available to the AI in every conversation
- **Language Agnostic**: Works in any language without hardcoded keywords or triggers
- **Comprehensive Data**: Access to all current tasks, recent completed tasks, and projects
- **Model Exclusion**: Configure which AI models/characters should exclude Todoist data
- **Unicode Support**: Properly handles international characters (ä, ö, etc.)
- **Flexible Integration**: Uses MCP Proxy Server for reliable API access

## Prerequisites

- [Open WebUI](https://github.com/open-webui/open-webui)
- [MCP Proxy Server for Open WebUI](https://docs.openwebui.com/openapi-servers/mcp/)
- [Official Doist/todoist-mcp](https://github.com/Doist/todoist-mcp)

First, you need [the official Todoist MCP server](https://github.com/Doist/todoist-mcp) running:

```bash
# Install the Todoist MCP server
git clone https://github.com/Doist/todoist-mcp
cd ~/todoist-mcp
npm install
npm run build

# Set up your Todoist API token
export TODOIST_API_TOKEN="your_token_here"
```

Install and run the MCP Proxy Server:

```bash
# Install in your Open WebUI virtual environment
cd ~/open-webui
source venv/bin/activate
pip install mcpo

# Start the proxy server
mcpo --host 0.0.0.0 --port 8001 todoist-mcp
```

Set up as a systemd service for automatic startup:

```bash
# Create service file
sudo nano /etc/systemd/system/todoist-mcp-proxy.service
```

```ini
[Unit]
Description=Todoist MCP Proxy Server
After=network.target

[Service]
Type=simple
User=rolle
Group=rolle
WorkingDirectory=/home/rolle/open-webui
Environment=PATH=/home/rolle/open-webui/venv/bin
Environment=TODOIST_API_TOKEN=your_token_here
ExecStart=/home/rolle/open-webui/venv/bin/mcpo --host 0.0.0.0 --port 8001 todoist-mcp
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable todoist-mcp-proxy.service
sudo systemctl start todoist-mcp-proxy.service
```

## 🚀 Installation

1. Download `todoist_mcp_bridge.py` from this repository
2. In Open WebUI, go to **Settings** → **Functions**
3. Click **Import Function** and upload the file
4. **Enable the function globally** in the Functions settings
5. Configure the MCP Proxy URL (default: `http://localhost:8001`)

## ⚙️ Configuration

### Function Settings (Valves)

- **MCP_PROXY_URL**: URL of your Todoist MCP Proxy Server (default: `http://localhost:8001`)
- **excluded_models**: Comma-separated list of model names to exclude from Todoist data injection

### Example Configuration

```
MCP_PROXY_URL: http://localhost:8001
excluded_models: english-refiner,translator,summarizer
```

## 💬 Usage Examples

Once installed and configured, the AI will automatically have access to your Todoist data. You can ask questions naturally in any language:

**English:**
- "What should I work on today?"
- "How productive have I been this week?"
- "Do I have any urgent tasks?"

**Finnish:**
- "Mitä tehtäviä minulla on tänään?"
- "Kuinka tuottelias olen ollut?"
- "Onko minulla kiireellisiä tehtäviä?"

**Spanish:**
- "¿Qué tareas tengo para hoy?"
- "¿Cómo ha sido mi productividad?"

The AI will naturally reference your task data when relevant and can help you:
- Review current tasks
- Check completed tasks
- Understand your productivity patterns
- Get project overviews
- Plan your work

## 🔧 How It Works

1. **Data Injection**: The function automatically injects your Todoist data into every conversation as context
2. **MCP Communication**: Uses the MCP Proxy Server to communicate with the Todoist MCP server
3. **Smart Context**: Provides all current tasks, recent completed tasks (last 7 days), and projects
4. **Unicode Handling**: Properly encodes international characters for display
5. **Model Filtering**: Excludes specified models from receiving Todoist context

## 📊 Data Provided

The AI receives:
- **All Current Tasks**: Complete list of your active Todoist tasks
- **Recent Completed Tasks**: Tasks completed in the last 7 days
- **Projects**: All your Todoist projects for context
- **Current Date**: For temporal context

## 🐛 Troubleshooting

### Function Not Working
- Ensure the function is **enabled globally** in Open WebUI
- Check that the MCP Proxy Server is running on the configured port
- Verify your Todoist API token is valid

### No Task Data Appearing
- Check Open WebUI logs for "TODOIST BRIDGE:" debug messages
- Verify the MCP Proxy URL is correct
- Test the proxy server directly: `curl http://localhost:8001/docs`

### Unicode Character Issues
- This version (1.1.0+) includes Unicode fixes for international characters
- Upgrade to the latest version if seeing encoded characters
