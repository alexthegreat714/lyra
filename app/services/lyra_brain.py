"""
Lyra Agent - Brain Module

Lyra's internal reasoning engine for structured, inspectable creative processing.
Deterministic, tool-driven pipeline with memory integration.

Phase 4: Added memory retrieval stage.

GUARDRAILS:
    - No legal reasoning (Sophia only)
    - No factual judgment (Veritas only)
    - No compute/resource logic (Argus only)
    - No health/social inference (Mercury)
    - No emotional inference
    - No "advice" style output, only structured creative constructs
"""

import asyncio
from typing import Any, Dict, List, Optional

from loguru import logger


class LyraBrain:
    """
    Lyra's internal reasoning engine.
    Deterministic, structured, and tool-driven with memory support.

    Pipeline stages:
        1. Interpretation - Analyze input characteristics
        2. Objective Classification - Determine task type
        2.5. Memory Retrieval - Fetch relevant context (Phase 4)
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

    # Task type to memory category mapping
    TASK_CATEGORY_MAPPING = {
        "narrative_design": ["narratives", "themes", "motifs"],
        "idea_generation": ["themes", "creative_history", "motifs"],
        "analogy_exploration": ["motifs", "themes", "styles"],
        "reframe": ["themes", "styles", "creative_history"],
        "counterfactual_analysis": ["themes", "narratives"],
        "tone_mapping": ["styles", "themes"],
        "mixed_creative": None,  # Search all categories
    }

    def __init__(self, tools: Dict[str, Any], memory: Any = None):
        """
        Initialize the brain with available tools and optional memory.

        Args:
            tools: Dictionary mapping tool names to tool instances
            memory: Optional memory manager instance (Phase 4)
        """
        self.tools = tools
        self.memory = memory
        logger.info(
            f"LyraBrain initialized with tools: {', '.join(tools.keys())}"
            + (", memory: enabled" if memory else "")
        )

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

        # Stage 2.5: Retrieve relevant memory (Phase 4)
        retrieved = self._retrieve_memory(task_type, prompt, context)
        steps.append({"stage": "memory_retrieval", "data": retrieved})

        # Attach retrieved memory into context for downstream tools
        if context is None:
            context = {}
        context["retrieved_memory"] = retrieved

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

    def _retrieve_memory(
        self,
        task_type: str,
        prompt: str,
        context: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Stage 2.5: Retrieve relevant memory context (Phase 4).

        Queries long-term memory for relevant creative context.

        Args:
            task_type: The task type
            prompt: The input prompt
            context: Optional context

        Returns:
            Memory retrieval results
        """
        if self.memory is None:
            return {"available": False, "items": [], "count": 0}

        # Decide categories based on task_type
        categories = self.TASK_CATEGORY_MAPPING.get(task_type)

        try:
            # Run async retrieval - handle both sync and async contexts
            results = self._run_memory_retrieval(prompt, task_type, categories)

            return {
                "available": True,
                "items": results,
                "count": len(results),
                "categories_searched": categories or "all",
            }
        except Exception as e:
            logger.warning(f"Memory retrieval failed: {e}")
            return {"available": True, "items": [], "count": 0, "error": str(e)}

    def _run_memory_retrieval(
        self,
        prompt: str,
        task_type: str,
        categories: Optional[List[str]]
    ) -> List[Dict[str, Any]]:
        """
        Run memory retrieval, handling async context.

        Args:
            prompt: Query prompt
            task_type: Task type
            categories: Categories to search

        Returns:
            List of retrieved items
        """
        try:
            # Try to get running event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're in an async context, can't use run_until_complete
                # Use sync fallback from query module
                from app.rag.query import query_relevant_sync
                return query_relevant_sync(prompt, categories, top_k=5)
            else:
                # Run async function
                return loop.run_until_complete(
                    self.memory.retrieve_context(
                        prompt=prompt,
                        task_type=task_type,
                        categories=categories,
                        top_k=5
                    )
                )
        except RuntimeError:
            # No event loop exists, create one
            return asyncio.run(
                self.memory.retrieve_context(
                    prompt=prompt,
                    task_type=task_type,
                    categories=categories,
                    top_k=5
                )
            )

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
            context: Optional context (now includes retrieved_memory)

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
            context: Optional context (includes retrieved_memory)

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

        # Phase 4: Include memory context summary if available
        if context and "retrieved_memory" in context:
            memory_data = context["retrieved_memory"]
            if memory_data.get("count", 0) > 0:
                synthesis["memory_context"] = {
                    "items_found": memory_data["count"],
                    "categories": memory_data.get("categories_searched", "all"),
                }

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
