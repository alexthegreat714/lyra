# Lyra Agent

Lyra is a creative strategist and conceptual reframing agent designed to assist with innovative thinking, idea generation, and creative problem-solving within a multi-agent system.

## Current Phase: Phase 2 - Creative Tools

This implementation includes the foundation from Phase 1 plus Lyra's creative toolset.

### Available Tools

| Tool | Description |
|------|-------------|
| `divergence` | Generate 5-7 divergent conceptual angles from a prompt |
| `convergence` | Distill multiple options into a core insight |
| `analogies` | Produce 3-5 analogies from different domains |
| `narratives` | Generate narrative scaffolds with structure and beats |
| `counterfactuals` | Build structured what-if scenario analyses |
| `tonemap` | Map conceptual tones (not emotional inference) |

### Phase 2 Restrictions

This phase includes pure creative logic functions only:
- No RAG querying
- No memory writing
- No legal checks or bias flags
- No congress contributions
- No Sky event logic
- No persona or tone behavior
- No creativity "pipeline"
- No emotional modeling

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
      lyra_agent.py      # Lyra agent class with tool integration
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

### POST /run_task
Execute a task through the Lyra agent.

**Basic Request:**
```json
{
  "task": "string",
  "payload": {}
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

**Response:**
```json
{
  "status": "received",
  "task_id": "uuid",
  "result": {
    "result": [
      {"angle": "Inversion", "description": "..."},
      {"angle": "Scale Shift", "description": "..."}
    ]
  }
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

#### Analogies Tool
```json
{
  "task": "use_tool",
  "payload": {
    "tool": "analogies",
    "args": {"concept": "organizational change"}
  }
}
```

#### Narratives Tool
```json
{
  "task": "use_tool",
  "payload": {
    "tool": "narratives",
    "args": {
      "theme": "digital transformation",
      "constraints": {"structure": "hero_journey"}
    }
  }
}
```

#### Counterfactuals Tool
```json
{
  "task": "use_tool",
  "payload": {
    "tool": "counterfactuals",
    "args": {"scenario": "Company adopts AI-first strategy"}
  }
}
```

#### Tone Mapper Tool
```json
{
  "task": "use_tool",
  "payload": {
    "tool": "tonemap",
    "args": {"prompt": "Strategic technical implementation"}
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
pytest tests/test_tools.py

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

### Phase 3 - Memory and Context
- Short-term memory implementation
- Long-term memory storage
- Context management

### Phase 4 - RAG Integration
- Document ingestion pipeline
- Text embedding system
- Knowledge retrieval and querying

### Phase 5 - Congress Interface
- Multi-agent collaboration
- Event-driven communication
- Coordination with Sky orchestrator

## License

Copyright 2024. All rights reserved.
