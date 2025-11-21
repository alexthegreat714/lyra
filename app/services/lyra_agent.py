"""
Lyra Agent Service

Core agent class for the Lyra creative strategist agent.
"""

from typing import Any, Dict, Optional

from loguru import logger

from app.tools.divergence import DivergenceTool
from app.tools.convergence import ConvergenceTool
from app.tools.analogies import AnalogyTool
from app.tools.narratives import NarrativeTool
from app.tools.counterfactuals import CounterfactualTool
from app.tools.tone_map import ToneMapper


class LyraAgent:
    """
    Lyra Agent - Creative strategist and conceptual reframing agent.

    Phase 2: Tool integrations for creative exploration.
    Available tools:
        - divergence: Generate divergent conceptual angles
        - convergence: Distill options into core insights
        - analogies: Create cross-domain analogies
        - narratives: Build narrative scaffolds
        - counterfactuals: Construct what-if scenarios
        - tonemap: Map conceptual tones

    Future phases will implement:
        - RAG-based knowledge retrieval
        - Reasoning patterns
        - Congress interface for multi-agent collaboration
    """

    # Map of tool names to their methods
    TOOL_REGISTRY = {
        "divergence": "divergence",
        "convergence": "convergence",
        "analogies": "analogies",
        "narratives": "narratives",
        "counterfactuals": "counterfactuals",
        "tonemap": "tonemap",
    }

    def __init__(self, settings):
        """
        Initialize the Lyra agent with all creative tools.

        Args:
            settings: Application settings instance
        """
        self.settings = settings

        # Initialize creative tools
        self.divergence = DivergenceTool()
        self.convergence = ConvergenceTool()
        self.analogies = AnalogyTool()
        self.narratives = NarrativeTool()
        self.counterfactuals = CounterfactualTool()
        self.tonemap = ToneMapper()

        logger.info(f"LyraAgent initialized (v{settings.VERSION}) with creative tools")

    def run_task(self, task: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a task.

        Args:
            task: The type of task to execute
            payload: Task-specific payload data

        Returns:
            Dict containing task execution result
        """
        logger.info(f"Running task: {task}")

        # Handle tool invocation task
        if task == "use_tool":
            tool_name = payload.get("tool")
            tool_args = payload.get("args", {})
            return self.use_tool(tool_name, tool_args)

        # Default: return task info
        return {
            "note": "Lyra Phase 2 - use task='use_tool' for tool access",
            "task_received": task,
            "payload_keys": list(payload.keys()) if payload else [],
            "available_tools": list(self.TOOL_REGISTRY.keys()),
        }

    def use_tool(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a specific creative tool.

        Args:
            tool_name: Name of the tool to use
            payload: Arguments for the tool

        Returns:
            Dict containing tool result
        """
        logger.info(f"Using tool: {tool_name}")

        if tool_name not in self.TOOL_REGISTRY:
            return {
                "error": f"Unknown tool: {tool_name}",
                "available_tools": list(self.TOOL_REGISTRY.keys()),
            }

        try:
            result = self._invoke_tool(tool_name, payload)
            return {"result": result}
        except Exception as e:
            logger.error(f"Tool invocation failed: {e}")
            return {"error": str(e)}

    def _invoke_tool(self, tool_name: str, payload: Dict[str, Any]) -> Any:
        """
        Internal method to invoke tool logic.

        Args:
            tool_name: Name of the tool
            payload: Tool arguments

        Returns:
            Tool result
        """
        if tool_name == "divergence":
            prompt = payload.get("prompt", "")
            return self.divergence.generate(prompt)

        elif tool_name == "convergence":
            options = payload.get("options", [])
            return self.convergence.distill(options)

        elif tool_name == "analogies":
            concept = payload.get("concept", "")
            return self.analogies.generate(concept)

        elif tool_name == "narratives":
            theme = payload.get("theme", "")
            constraints = payload.get("constraints", {})
            return self.narratives.outline(theme, constraints)

        elif tool_name == "counterfactuals":
            scenario = payload.get("scenario", "")
            return self.counterfactuals.build(scenario)

        elif tool_name == "tonemap":
            prompt = payload.get("prompt", "")
            return self.tonemap.map(prompt)

        else:
            raise ValueError(f"Tool '{tool_name}' not implemented")

    def handle_event(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle an incoming event.

        Args:
            event_type: Type of event
            payload: Event-specific payload data

        Returns:
            Dict indicating event was handled
        """
        logger.info(f"Handling event: {event_type}")
        return {"handled": True, "event_type": event_type}

    def get_status(self) -> Dict[str, Any]:
        """
        Get the current status of the agent.

        Returns:
            Dict containing agent status information
        """
        return {
            "agent": self.settings.AGENT_NAME,
            "version": self.settings.VERSION,
            "ok": True,
            "tools_available": list(self.TOOL_REGISTRY.keys()),
        }

    def get_available_tools(self) -> Dict[str, str]:
        """
        Get information about available tools.

        Returns:
            Dict mapping tool names to descriptions
        """
        return {
            "divergence": "Generate 5-7 divergent conceptual angles from a prompt",
            "convergence": "Distill multiple options into a core insight",
            "analogies": "Produce 3-5 analogies from different domains",
            "narratives": "Generate narrative scaffolds with structure and beats",
            "counterfactuals": "Build structured what-if scenario analyses",
            "tonemap": "Map conceptual tones (not emotional inference)",
        }
