"""
Lyra Agent Service

Core agent class for the Lyra creative strategist agent.

GUARDRAILS:
    - No legal reasoning (Sophia only)
    - No factual judgment (Veritas only)
    - No compute/resource logic (Argus only)
    - No health/social inference (Mercury)
    - No emotional inference
    - No "advice" style output, only structured creative constructs
"""

from typing import Any, Dict, Optional

from loguru import logger

from app.tools.divergence import DivergenceTool
from app.tools.convergence import ConvergenceTool
from app.tools.analogies import AnalogyTool
from app.tools.narratives import NarrativeTool
from app.tools.counterfactuals import CounterfactualTool
from app.tools.tone_map import ToneMapper
from app.services.lyra_brain import LyraBrain
from app.services.memory_manager import LyraMemoryManager


class LyraAgent:
    """
    Lyra Agent - Creative strategist and conceptual reframing agent.

    Phase 4: RAG + Memory integration.
    Available tools:
        - divergence: Generate divergent conceptual angles
        - convergence: Distill options into core insights
        - analogies: Create cross-domain analogies
        - narratives: Build narrative scaffolds
        - counterfactuals: Construct what-if scenarios
        - tonemap: Map conceptual tones

    Creative task types:
        - idea_generation
        - reframe
        - narrative_design
        - counterfactual_analysis
        - analogy_exploration
        - tone_mapping
        - mixed_creative

    Memory categories:
        - themes, narratives, styles
        - user_preferences, creative_history, motifs

    Future phases will implement:
        - Congress interface for multi-agent collaboration

    GUARDRAILS:
        - No legal reasoning (Sophia only)
        - No factual judgment (Veritas only)
        - No compute/resource logic (Argus only)
        - No health/social inference (Mercury)
        - No emotional inference
        - No "advice" style output, only structured creative constructs
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
        Initialize the Lyra agent with all creative tools, brain, and memory.

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

        # Phase 4: Initialize memory manager
        self.memory = LyraMemoryManager()

        # Phase 4: Initialize the reasoning brain with tool access and memory
        self.brain = LyraBrain(
            tools={
                "divergence": self.divergence,
                "convergence": self.convergence,
                "analogies": self.analogies,
                "narratives": self.narratives,
                "counterfactuals": self.counterfactuals,
                "tonemap": self.tonemap,
            },
            memory=self.memory,
        )

        logger.info(
            f"LyraAgent initialized (v{settings.VERSION}) "
            f"with creative tools, brain, and memory"
        )

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

        # Phase 2: Handle direct tool invocation
        if task == "use_tool":
            tool_name = payload.get("tool")
            tool_args = payload.get("args", {})
            return self.use_tool(tool_name, tool_args)

        # Phase 3: Handle creative brain task
        if task == "creative_brain":
            return self.run_creative_task(
                task_type=payload.get("task_type", "mixed_creative"),
                prompt=payload.get("prompt", ""),
                context=payload.get("context"),
            )

        # Default: return task info
        return {
            "note": "Lyra Phase 4 - use task='creative_brain' or 'use_tool'",
            "task_received": task,
            "payload_keys": list(payload.keys()) if payload else [],
            "available_tools": list(self.TOOL_REGISTRY.keys()),
            "available_task_types": self.brain.get_supported_tasks(),
            "memory_categories": self.memory.get_valid_categories(),
        }

    def run_creative_task(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute a creative task through the reasoning brain.

        Args:
            task_type: Type of creative task to perform
            prompt: The input prompt to process
            context: Optional context for the task

        Returns:
            Structured result from the brain's reasoning pipeline
        """
        logger.info(f"Running creative task: {task_type}")
        return self.brain.process(task_type, prompt, context)

    def use_tool(self, tool_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Invoke a specific creative tool directly.

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
            "task_types_available": self.brain.get_supported_tasks(),
            "memory_stats": self.memory.get_stats(),
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

    def get_available_task_types(self) -> Dict[str, str]:
        """
        Get information about available creative task types.

        Returns:
            Dict mapping task types to descriptions
        """
        return {
            "idea_generation": "Generate and distill divergent ideas",
            "reframe": "Analyze tone and reframe concepts",
            "narrative_design": "Create narrative scaffolds and structures",
            "counterfactual_analysis": "Explore what-if scenarios",
            "analogy_exploration": "Generate cross-domain analogies",
            "tone_mapping": "Map conceptual tones",
            "mixed_creative": "Full creative pipeline with multiple tools",
        }
