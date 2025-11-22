"""
Lyra Agent - Brain Module

Lyra's internal reasoning engine for structured, inspectable creative processing.
Deterministic, tool-driven pipeline with no RAG, memory, or Congress logic.

Phase 3: Structured reasoning only.

GUARDRAILS:
    - No legal reasoning (Sophia only)
    - No factual judgment (Veritas only)
    - No compute/resource logic (Argus only)
    - No health/social inference (Mercury)
    - No emotional inference
    - No "advice" style output, only structured creative constructs
"""

from typing import Any, Dict, List, Optional

from loguru import logger


class LyraBrain:
    """
    Lyra's internal reasoning engine.
    Deterministic, structured, and tool-driven.
    No RAG, no memory, no Congress logic in Phase 3.

    Pipeline stages:
        1. Interpretation - Analyze input characteristics
        2. Objective Classification - Determine task type
        3. Tool Plan Selection - Choose appropriate tools
        4. Tool Execution - Run tools in sequence
        5. Synthesis - Combine results into structured output

    GUARDRAILS:
        - No legal reasoning (Sophia only)
        - No factual judgment (Veritas only)
        - No compute/resource logic (Argus only)
        - No health/social inference (Mercury)
        - No emotional inference
        - No "advice" style output, only structured creative constructs
    """

    # Supported task types and their tool mappings
    TASK_TOOL_MAPPING = {
        "idea_generation": ["divergence", "convergence"],
        "reframe": ["tonemap", "divergence", "convergence"],
        "narrative_design": ["narratives"],
        "counterfactual_analysis": ["counterfactuals", "convergence"],
        "analogy_exploration": ["analogies"],
        "tone_mapping": ["tonemap"],
        "mixed_creative": ["divergence", "analogies", "narratives", "convergence"],
    }

    def __init__(self, tools: Dict[str, Any]):
        """
        Initialize the brain with available tools.

        Args:
            tools: Dictionary mapping tool names to tool instances
        """
        self.tools = tools
        logger.info("LyraBrain initialized with tools: " + ", ".join(tools.keys()))

    def process(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a creative task through the reasoning pipeline.

        Args:
            task_type: Type of creative task to perform
            prompt: The input prompt to process
            context: Optional context for the task

        Returns:
            Structured result with task_type, prompt, result, and steps
        """
        logger.info(f"Processing task_type={task_type}, prompt_length={len(prompt)}")
        steps = []

        # Stage 1: Interpret input
        interpretation = self._interpret_input(prompt, context)
        steps.append({"stage": "interpretation", "data": interpretation})

        # Stage 2: Classify objective
        objective = self._classify_objective(task_type, prompt, context)
        steps.append({"stage": "objective_classification", "data": objective})

        # Stage 3: Select tool plan
        plan = self._select_tools(objective)
        steps.append({"stage": "tool_plan", "data": plan})

        # Stage 4: Execute tools
        tool_results = self._execute_plan(plan, prompt, context)
        steps.append({"stage": "tool_execution", "data": tool_results})

        # Stage 5: Synthesize output
        synthesis = self._synthesize(objective, tool_results, context)
        steps.append({"stage": "synthesis", "data": synthesis})

        return {
            "task_type": objective.get("task_type", task_type),
            "prompt": prompt,
            "result": synthesis,
            "steps": steps
        }

    # -------------------------
    # INTERNAL PIPELINE STEPS
    # -------------------------

    def _interpret_input(
        self, prompt: str, context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Stage 1: Interpret and analyze the input.

        Analyzes prompt characteristics without making judgments
        or inferences about intent, emotion, or factual claims.

        Args:
            prompt: The input prompt
            context: Optional context

        Returns:
            Interpretation data
        """
        # Count structural elements
        word_count = len(prompt.split()) if prompt else 0
        sentence_indicators = prompt.count('.') + prompt.count('!') + prompt.count('?')

        return {
            "prompt_length": len(prompt),
            "word_count": word_count,
            "sentence_indicators": sentence_indicators,
            "context_present": context is not None,
            "context_keys": list(context.keys()) if context else [],
        }

    def _classify_objective(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Stage 2: Classify the objective based on task type.

        Uses the provided task_type directly - no inference or guessing.

        Args:
            task_type: The specified task type
            prompt: The input prompt
            context: Optional context

        Returns:
            Objective classification data
        """
        is_valid_task = task_type in self.TASK_TOOL_MAPPING

        return {
            "task_type": task_type if is_valid_task else "mixed_creative",
            "task_valid": is_valid_task,
            "available_tasks": list(self.TASK_TOOL_MAPPING.keys()),
        }

    def _select_tools(self, objective: Dict[str, Any]) -> Dict[str, Any]:
        """
        Stage 3: Select the tool execution plan.

        Maps task types to their appropriate tool sequences.

        Args:
            objective: The classified objective

        Returns:
            Tool plan with list of tools to execute
        """
        task = objective["task_type"]
        tools = self.TASK_TOOL_MAPPING.get(task, [])

        return {
            "tools": tools,
            "tool_count": len(tools),
            "execution_order": "sequential",
        }

    def _execute_plan(
        self,
        plan: Dict[str, Any],
        prompt: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Stage 4: Execute the tool plan.

        Runs each tool in sequence, passing outputs between tools
        where appropriate.

        Args:
            plan: The tool plan from _select_tools
            prompt: The original prompt
            context: Optional context

        Returns:
            Results from all executed tools
        """
        results = {}
        last_output = None

        for tool_name in plan["tools"]:
            tool = self.tools.get(tool_name)
            if not tool:
                logger.warning(f"Tool '{tool_name}' not found, skipping")
                continue

            try:
                if tool_name == "divergence":
                    last_output = tool.generate(prompt)
                    results["divergence"] = last_output

                elif tool_name == "convergence":
                    # Convergence requires previous divergent output if available
                    input_data = last_output if isinstance(last_output, list) else []
                    last_output = tool.distill(input_data)
                    results["convergence"] = last_output

                elif tool_name == "analogies":
                    last_output = tool.generate(prompt)
                    results["analogies"] = last_output

                elif tool_name == "narratives":
                    last_output = tool.outline(prompt)
                    results["narrative"] = last_output

                elif tool_name == "counterfactuals":
                    last_output = tool.build(prompt)
                    results["counterfactuals"] = last_output

                elif tool_name == "tonemap":
                    last_output = tool.map(prompt)
                    results["tone"] = last_output

                logger.debug(f"Tool '{tool_name}' executed successfully")

            except Exception as e:
                logger.error(f"Tool '{tool_name}' failed: {e}")
                results[tool_name] = {"error": str(e)}

        return results

    def _synthesize(
        self,
        objective: Dict[str, Any],
        tool_results: Dict[str, Any],
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Stage 5: Synthesize tool results into structured output.

        Combines all tool outputs into a coherent response structure.
        No advice, judgments, or recommendations - only structured data.

        Args:
            objective: The classified objective
            tool_results: Results from tool execution
            context: Optional context

        Returns:
            Synthesized output structure
        """
        task_type = objective.get("task_type", "unknown")

        # Build synthesis based on what tools produced
        synthesis = {
            "summary": f"Synthesized output for {task_type}",
            "primary_insights": list(tool_results.keys()),
        }

        # Include each result type if present
        if "divergence" in tool_results:
            synthesis["options"] = tool_results["divergence"]

        if "convergence" in tool_results:
            synthesis["distilled"] = tool_results["convergence"]

        if "narrative" in tool_results:
            synthesis["narrative_outline"] = tool_results["narrative"]

        if "counterfactuals" in tool_results:
            synthesis["counterfactuals"] = tool_results["counterfactuals"]

        if "analogies" in tool_results:
            synthesis["analogies"] = tool_results["analogies"]

        if "tone" in tool_results:
            synthesis["tone_profile"] = tool_results["tone"]

        return synthesis

    def get_supported_tasks(self) -> List[str]:
        """
        Return list of supported task types.

        Returns:
            List of task type strings
        """
        return list(self.TASK_TOOL_MAPPING.keys())

    def get_task_tools(self, task_type: str) -> List[str]:
        """
        Return tools used for a specific task type.

        Args:
            task_type: The task type to query

        Returns:
            List of tool names
        """
        return self.TASK_TOOL_MAPPING.get(task_type, [])
