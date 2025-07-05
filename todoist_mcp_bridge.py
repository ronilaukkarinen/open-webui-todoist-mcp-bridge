"""
title: Todoist MCP Bridge
author: Roni Laukkarinen
description: Bridge to Todoist MCP Proxy Server for reliable task management.
repository_url: https://github.com/ronilaukkarinen/open-webui-todoist-mcp-bridge
version: 1.1.0
required_open_webui_version: >= 0.5.0
"""

import json
import requests
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class Filter:
    class Valves(BaseModel):
        MCP_PROXY_URL: str = Field(
            default="http://localhost:8001",
            description="URL of the Todoist MCP Proxy Server"
        )
        excluded_models: str = Field(
            default="",
            description="Comma-separated list of model names to exclude from Todoist data injection. Use lowercase with hyphens (e.g., 'english-refiner,translator,obfuscator')"
        )

    def __init__(self):
        self.valves = self.Valves()

    def _should_exclude_model(self, body: dict, excluded_models: str) -> bool:
        """
        Check if the current model should be excluded from Todoist data injection.
        Supports multiple model identifier fields for robust filtering.
        """
        if not excluded_models:
            return False

        # Parse excluded models list
        excluded_models_list = [model.strip().strip('"\'') for model in excluded_models.split(",")]

        # Check multiple possible model identifier fields
        current_model = body.get("model", "")
        model_id = body.get("model_id", "")

        # Check for OpenWebUI model/character names in nested structures
        model_name = ""
        model_title = ""

        # Look for model info in nested chat structure
        if "chat" in body and isinstance(body["chat"], dict):
            if "models" in body["chat"] and isinstance(body["chat"]["models"], list):
                for model_info in body["chat"]["models"]:
                    if isinstance(model_info, dict):
                        if "name" in model_info:
                            model_name = model_info.get("name", "")
                        if "title" in model_info:
                            model_title = model_info.get("title", "")

        # Also check direct model info
        if "model_info" in body and isinstance(body["model_info"], dict):
            model_name = body["model_info"].get("name", model_name)
            model_title = body["model_info"].get("title", model_title)

        # Check all possible model identifiers against exclusion list
        models_to_check = [current_model, model_id, model_name, model_title]
        for model_identifier in models_to_check:
            if model_identifier and model_identifier in excluded_models_list:
                return True
        return False

    def inlet(self, body: dict, __user__ = None) -> dict:
        """
        Inject Todoist task data into every conversation so AI can access it naturally.
        Similar to how the memory function works - adds task context to the first user message.
        """
        print(f"TODOIST BRIDGE: inlet() called!")
        print(f"TODOIST BRIDGE: body keys: {list(body.keys())}")
        print(f"TODOIST BRIDGE: messages count: {len(body.get('messages', []))}")

        # Check if current model should be excluded
        if self.valves.excluded_models:
            if self._should_exclude_model(body, self.valves.excluded_models):
                print("TODOIST BRIDGE: Skipping Todoist data injection for excluded model")
                return body

        if "messages" in body and body["messages"]:
            try:
                print(f"TODOIST BRIDGE: Getting task data...")
                # Get comprehensive task data
                task_data = self.get_all_task_data()
                print(f"TODOIST BRIDGE: Got task data, length: {len(task_data)}")

                # Create task context similar to memory function
                task_context = f"""<TODOIST_CONTEXT>
You have access to the user's Todoist task data. Here's their current information:

{task_data}

IMPORTANT INSTRUCTIONS:
- Only reference task information when relevant to the current conversation
- Do not list or enumerate tasks unless specifically asked
- Use the information naturally to provide better, more personalized responses
- You can help with task management in any language the user prefers
- If task information is not relevant to the current topic, ignore it completely

</TODOIST_CONTEXT>

"""

                # Add task context to the first user message
                for i, message in enumerate(body["messages"]):
                    if message.get("role") == "user":
                        original_content = message.get("content", "")
                        # Only inject if not already present
                        if not original_content.startswith("<TODOIST_CONTEXT>"):
                            message["content"] = task_context + original_content
                            print(f"TODOIST BRIDGE: Injected Todoist task data into conversation")
                        else:
                            print(f"TODOIST BRIDGE: Todoist context already present, skipping injection")
                        break

            except Exception as e:
                print(f"TODOIST BRIDGE: Error injecting Todoist context: {e}")
                import traceback
                traceback.print_exc()

        return body

    def call_mcp(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Call MCP Proxy endpoint"""
        url = f"{self.valves.MCP_PROXY_URL}/{endpoint}"

        try:
            # All MCP Proxy endpoints expect POST requests
            if data is None:
                data = {}
            response = requests.post(url, json=data)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"MCP request failed: {str(e)}"}

    def get_all_task_data(self) -> str:
        """
        Get comprehensive task data from Todoist.
        Returns all current tasks, recent completed tasks, and projects.
        No hardcoded filters - completely flexible for AI to interpret.

        Returns:
            JSON string with all task data
        """
        try:
            # Get all current tasks
            all_tasks = self.call_mcp("get-tasks")

            # Get recent completed tasks
            from datetime import date, timedelta
            today = date.today()
            week_ago = today - timedelta(days=7)

            completed_recent = self.call_mcp("get-tasks-completed-by-completion-date", {
                "since": f"{week_ago.isoformat()}T00:00:00Z",
                "until": f"{today.isoformat()}T23:59:59Z"
            })

            # Get all projects
            projects = self.call_mcp("get-projects")

            result = {
                "all_tasks": all_tasks,
                "recent_completed_tasks": completed_recent,
                "projects": projects,
                "current_date": today.isoformat()
            }

            return json.dumps(result, indent=2, ensure_ascii=False)

        except Exception as e:
            return json.dumps({"error": f"Failed to get task data: {str(e)}"}, ensure_ascii=False)

    def get_productivity_stats(self) -> str:
        """
        Get comprehensive productivity statistics and insights.

        Returns:
            JSON string with productivity metrics and performance data
        """
        try:
            result = self.call_mcp("get-productivity-stats")
            return json.dumps(result, indent=2, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": f"Failed to get productivity stats: {str(e)}"}, ensure_ascii=False)

    def add_task(self, content: str, description: str = "", due_string: str = "", priority: int = 1) -> str:
        """
        Add a new task to Todoist.

        Args:
            content: Task content (required)
            description: Task description
            due_string: Natural language due date (e.g., "tomorrow at 2pm")
            priority: Priority level (1=normal, 2=high, 3=very high, 4=urgent)

        Returns:
            JSON string with task information or error message
        """
        if not content:
            return json.dumps({"error": "Task content is required"}, ensure_ascii=False)

        data = {"content": content}
        if description:
            data["description"] = description
        if due_string:
            data["due_string"] = due_string
        if priority > 1:
            data["priority"] = priority

        result = self.call_mcp("add-task", data)
        return json.dumps(result, indent=2, ensure_ascii=False)

    def quick_add_task(self, text: str) -> str:
        """
        Add a task using natural language processing.
        Perfect for converting conversational requests into tasks.

        Args:
            text: Task text with natural language (e.g., "Buy milk tomorrow at 2pm #grocery")

        Returns:
            JSON string with task information or error message
        """
        if not text:
            return json.dumps({"error": "Task text is required"})

        result = self.call_mcp("quick-add-task", {"text": text})
        return json.dumps(result, indent=2, ensure_ascii=False)

    def complete_task(self, task_id: str) -> str:
        """
        Mark a task as completed.

        Args:
            task_id: Task ID to complete

        Returns:
            JSON string with success confirmation or error message
        """
        if not task_id:
            return json.dumps({"error": "Task ID is required"})

        result = self.call_mcp("close-task", {"task_id": task_id})
        return json.dumps(result, indent=2, ensure_ascii=False)

    def get_tasks(self, filter_string: str = "", project_id: str = "") -> str:
        """
        Get tasks from Todoist with optional filtering.

        Args:
            filter_string: Filter tasks using Todoist's filter syntax (e.g., "today", "p1", "overdue")
            project_id: Get tasks from specific project

        Returns:
            JSON string with tasks or error message
        """
        data = {}
        if filter_string:
            data["filter"] = filter_string
        if project_id:
            data["project_id"] = project_id

        if data:
            result = self.call_mcp("get-tasks-by-filter", data)
        else:
            result = self.call_mcp("get-tasks")

        return json.dumps(result, indent=2, ensure_ascii=False)

    def get_projects(self) -> str:
        """
        Get all projects from Todoist.

        Returns:
            JSON string with projects or error message
        """
        result = self.call_mcp("get-projects")
        return json.dumps(result, indent=2, ensure_ascii=False)

    def update_task(self, task_id: str, content: str = "", description: str = "", due_string: str = "", priority: int = 0) -> str:
        """
        Update an existing task.

        Args:
            task_id: Task ID to update (required)
            content: New task content
            description: New task description
            due_string: New natural language due date
            priority: New priority level (1-4)

        Returns:
            JSON string with updated task information or error message
        """
        if not task_id:
            return json.dumps({"error": "Task ID is required"})

        data = {"task_id": task_id}
        if content:
            data["content"] = content
        if description:
            data["description"] = description
        if due_string:
            data["due_string"] = due_string
        if priority > 0:
            data["priority"] = priority

        result = self.call_mcp("update-task", data)
        return json.dumps(result, indent=2, ensure_ascii=False)
