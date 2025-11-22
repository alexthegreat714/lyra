# Lyra Agent

Lyra is a creative strategist and conceptual reframing agent designed to assist with innovative thinking, idea generation, and creative problem-solving within a multi-agent system.

## Current Phase: Phase 3 - Reasoning Engine

This implementation includes the foundation from Phases 1-2 plus the LyraBrain structured reasoning engine.

### LyraBrain - Structured Reasoning

LyraBrain is Lyra's internal reasoning engine that provides deterministic, inspectable creative processing through a 5-stage pipeline:

1. **Interpretation** - Analyze input characteristics
2. **Objective Classification** - Determine task type
3. **Tool Plan Selection** - Choose appropriate tools
4. **Tool Execution** - Run tools in sequence
5. **Synthesis** - Combine results into structured output

### Available Creative Task Types

| Task Type | Tools Used | Description |
|-----------|------------|-------------|
| `idea_generation` | divergence → convergence | Generate and distill divergent ideas |
| `reframe` | tonemap → divergence → convergence | Analyze tone and reframe concepts |
| `narrative_design` | narratives | Create narrative scaffolds |
| `counterfactual_analysis` | counterfactuals → convergence | Explore what-if scenarios |
| `analogy_exploration` | analogies | Generate cross-domain analogies |
| `tone_mapping` | tonemap | Map conceptual tones |
| `mixed_creative` | divergence → analogies → narratives → convergence | Full creative pipeline |

### Available Tools

| Tool | Description |
|------|-------------|
| `divergence` | Generate 5-7 divergent conceptual angles from a prompt |
| `convergence` | Distill multiple options into a core insight |
| `analogies` | Produce 3-5 analogies from different domains |
| `narratives` | Generate narrative scaffolds with structure and beats |
| `counterfactuals` | Build structured what-if scenario analyses |
| `tonemap` | Map conceptual tones (not emotional inference) |

### Phase 3 Notes

Phase 3 adds structured reasoning, NOT memory or RAG.

**Guardrails:**
- No legal reasoning (Sophia only)
- No factual judgment (Veritas only)
- No compute/resource logic (Argus only)
- No health/social inference (Mercury)
- No emotional inference
- No "advice" style output, only structured creative constructs

## Project Structure

```
lyra/
  app/
    main.py              # Entry point
    config.py            # Configuration and settings
    server.py            # FastAPI application factory
    routes/
      __init__.py
      core.py            # Core API endpoints
    models/
      __init__.py
      schema.py          # Pydantic request/response models
    services/
      __init__.py
      lyra_agent.py      # Lyra agent class with tool/brain integration
      lyra_brain.py      # LyraBrain reasoning engine
    tools/
      __init__.py
      divergence.py      # Divergent angle generation
      convergence.py     # Option distillation
      analogies.py       # Cross-domain analogies
      narratives.py      # Narrative scaffolding
      counterfactuals.py # What-if scenario analysis
      tone_map.py        # Conceptual tone mapping
    memory/
      short_term/        # Short-term memory storage (placeholder)
      long_term/         # Long-term memory storage (placeholder)
    rag/
      __init__.py
      ingest.py          # Document ingestion (placeholder)
      embed.py           # Text embedding (placeholder)
      query.py           # Knowledge retrieval (placeholder)
    logs/
  tests/
    conftest.py
    test_routes.py
    test_health.py
    test_tools.py        # Tool-specific tests
    test_brain.py        # Brain/reasoning tests
  README.md
  requirements.txt
```

## Installation

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Create a `.env` file for configuration:
   ```bash
   LYRA_HOST=0.0.0.0
   LYRA_PORT=8000
   LYRA_DEBUG=false
   ```

## Running the Server

Start the Lyra agent server:

```bash
# From the project root directory
python -m app.main
```

Or using uvicorn directly:

```bash
uvicorn app.server:app --host 0.0.0.0 --port 8000
```

The server will be available at `http://localhost:8000`.

## API Endpoints

### GET /status
Get the current status of the Lyra agent.

**Response:**
```json
{
  "agent": "Lyra",
  "version": "0.1",
  "state": "online"
}
```

### POST /creative_brain (Phase 3)
Execute a creative task through the reasoning brain.

**Request:**
```json
{
  "task_type": "idea_generation",
  "prompt": "sustainable innovation strategies",
  "context": {"optional": "context data"}
}
```

**Response:**
```json
{
  "task_type": "idea_generation",
  "prompt": "sustainable innovation strategies",
  "result": {
    "summary": "Synthesized output for idea_generation",
    "primary_insights": ["divergence", "convergence"],
    "options": [...],
    "distilled": {...}
  },
  "steps": [
    {"stage": "interpretation", "data": {...}},
    {"stage": "objective_classification", "data": {...}},
    {"stage": "tool_plan", "data": {...}},
    {"stage": "tool_execution", "data": {...}},
    {"stage": "synthesis", "data": {...}}
  ]
}
```

### POST /run_task
Execute a task through the Lyra agent.

**Creative Brain via run_task:**
```json
{
  "task": "creative_brain",
  "payload": {
    "task_type": "narrative_design",
    "prompt": "digital transformation journey"
  }
}
```

**Tool Invocation Request:**
```json
{
  "task": "use_tool",
  "payload": {
    "tool": "divergence",
    "args": {"prompt": "sustainable urban development"}
  }
}
```

### Creative Brain Examples

#### Idea Generation
```json
{
  "task_type": "idea_generation",
  "prompt": "remote work productivity"
}
```

#### Narrative Design
```json
{
  "task_type": "narrative_design",
  "prompt": "digital transformation",
  "context": {"structure": "hero_journey"}
}
```

#### Counterfactual Analysis
```json
{
  "task_type": "counterfactual_analysis",
  "prompt": "Company adopts AI-first strategy"
}
```

#### Analogy Exploration
```json
{
  "task_type": "analogy_exploration",
  "prompt": "organizational change management"
}
```

#### Tone Mapping
```json
{
  "task_type": "tone_mapping",
  "prompt": "strategic technical implementation"
}
```

#### Mixed Creative (Full Pipeline)
```json
{
  "task_type": "mixed_creative",
  "prompt": "future of sustainable cities"
}
```

### Tool Invocation Examples

#### Divergence Tool
```json
{
  "task": "use_tool",
  "payload": {
    "tool": "divergence",
    "args": {"prompt": "remote work productivity"}
  }
}
```

#### Convergence Tool
```json
{
  "task": "use_tool",
  "payload": {
    "tool": "convergence",
    "args": {
      "options": [
        {"angle": "A", "description": "First perspective"},
        {"angle": "B", "description": "Second perspective"}
      ]
    }
  }
}
```

### POST /event
Receive events from Sky/Congress.

**Request:**
```json
{
  "event_type": "string",
  "payload": {}
}
```

**Response:**
```json
{
  "acknowledged": true
}
```

### POST /shutdown
Initiate graceful shutdown.

**Response:**
```json
{
  "status": "shutdown_initiated",
  "message": "Lyra agent shutdown initiated"
}
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_brain.py

# Run brain tests only
pytest tests/test_brain.py -v

# Run tool tests only
pytest tests/test_tools.py -v
```

## Tool Details

### Divergence Tool
Generates 5-7 divergent conceptual angles using different lenses:
- Inversion, Scale Shift, Temporal, Cross-Domain
- Constraint Removal, Stakeholder Shift, Abstraction
- Materialization, Synthesis, Decomposition

### Convergence Tool
Distills multiple options into:
- Core idea
- Supporting points
- Rationale

### Analogies Tool
Produces analogies from domains including:
- Biology, Architecture, Music, Physics
- Economics, Ecology, Cooking, Navigation
- Gardening, Games

### Narratives Tool
Generates scaffolds with:
- Premise, Conflicts, Structural beats
- Resolution patterns
- Supports: three_act, hero_journey, five_act, circular

### Counterfactuals Tool
Builds what-if analyses across dimensions:
- Temporal, Magnitude, Actor, Method
- Context, Constraint, Information, Motivation

### Tone Mapper
Maps conceptual tones (NOT emotional inference):
- abstract, grounded, technical
- whimsical, strategic, narrative

## Expected Future Phases

### Phase 4 - RAG Integration
- Document ingestion pipeline
- Text embedding system
- Knowledge retrieval and querying

### Phase 5 - Memory and Context
- Short-term memory implementation
- Long-term memory storage
- Context management

### Phase 6 - Congress Interface
- Multi-agent collaboration
- Event-driven communication
- Coordination with Sky orchestrator

## License

Copyright 2024. All rights reserved.
