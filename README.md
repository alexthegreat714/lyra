# Lyra Agent

Lyra is a creative strategist and conceptual reframing agent designed to assist with innovative thinking, idea generation, and creative problem-solving within a multi-agent system.

## Current Phase: Phase 4 - RAG + Memory Integration

This implementation includes Phases 1-3 plus long-term memory with RAG capabilities.

### Phase 4 Features

- **File-backed Long-term Memory**: JSON storage under `memory/long_term/`
- **Text Embeddings**: HTTP client for embedding service (Ollama-compatible)
- **Semantic Search**: Cosine similarity-based retrieval
- **Memory Categories**: themes, narratives, styles, user_preferences, creative_history, motifs
- **Memory-aware Brain**: LyraBrain now retrieves relevant context during reasoning

### LyraBrain - Structured Reasoning (Phase 3+4)

LyraBrain is Lyra's internal reasoning engine with a 6-stage pipeline:

1. **Interpretation** - Analyze input characteristics
2. **Objective Classification** - Determine task type
3. **Memory Retrieval** - Fetch relevant context (Phase 4)
4. **Tool Plan Selection** - Choose appropriate tools
5. **Tool Execution** - Run tools in sequence
6. **Synthesis** - Combine results into structured output

### Memory Categories

| Category | Description |
|----------|-------------|
| `themes` | Core themes and concepts explored |
| `narratives` | Narrative structures and story elements |
| `styles` | Creative styles and approaches |
| `user_preferences` | User-specific preferences and patterns |
| `creative_history` | History of creative outputs |
| `motifs` | Recurring motifs and patterns |

### Available Creative Task Types

| Task Type | Tools Used | Memory Categories |
|-----------|------------|-------------------|
| `idea_generation` | divergence → convergence | themes, creative_history, motifs |
| `reframe` | tonemap → divergence → convergence | themes, styles, creative_history |
| `narrative_design` | narratives | narratives, themes, motifs |
| `counterfactual_analysis` | counterfactuals → convergence | themes, narratives |
| `analogy_exploration` | analogies | motifs, themes, styles |
| `tone_mapping` | tonemap | styles, themes |
| `mixed_creative` | divergence → analogies → narratives → convergence | all categories |

### Available Tools

| Tool | Description |
|------|-------------|
| `divergence` | Generate 5-7 divergent conceptual angles from a prompt |
| `convergence` | Distill multiple options into a core insight |
| `analogies` | Produce 3-5 analogies from different domains |
| `narratives` | Generate narrative scaffolds with structure and beats |
| `counterfactuals` | Build structured what-if scenario analyses |
| `tonemap` | Map conceptual tones (not emotional inference) |

### Guardrails

- No legal reasoning (Sophia only)
- No factual judgment (Veritas only)
- No compute/resource logic (Argus only)
- No health/social inference (Mercury)
- No emotional inference
- No "advice" style output, only structured creative constructs
- Memory is for creative context only - no cross-agent data

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
      memory.py          # Memory API endpoints (Phase 4)
    models/
      __init__.py
      schema.py          # Pydantic request/response models
    services/
      __init__.py
      lyra_agent.py      # Lyra agent class with tool/brain/memory integration
      lyra_brain.py      # LyraBrain reasoning engine with memory retrieval
      memory_manager.py  # Memory manager service (Phase 4)
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
      long_term/         # Long-term memory storage (Phase 4)
        themes/
        narratives/
        styles/
        user_preferences/
        creative_history/
        motifs/
    rag/
      __init__.py
      ingest.py          # Document ingestion (Phase 4)
      embed.py           # Text embedding (Phase 4)
      query.py           # Knowledge retrieval (Phase 4)
    logs/
  tests/
    conftest.py
    test_routes.py
    test_health.py
    test_tools.py        # Tool-specific tests
    test_brain.py        # Brain/reasoning tests
    test_memory.py       # Memory/RAG tests (Phase 4)
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

   # Phase 4: Embedding configuration
   LYRA_EMBEDDING_MODEL=nomic-embed-text
   LYRA_EMBEDDING_ENDPOINT=http://localhost:11434/api/embeddings
   LYRA_EMBEDDING_TIMEOUT=30.0
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

### POST /creative_brain
Execute a creative task through the reasoning brain (with memory retrieval).

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
    "distilled": {...},
    "memory_context": {
      "items_found": 3,
      "categories": ["themes", "creative_history", "motifs"]
    }
  },
  "steps": [
    {"stage": "interpretation", "data": {...}},
    {"stage": "objective_classification", "data": {...}},
    {"stage": "memory_retrieval", "data": {...}},
    {"stage": "tool_plan", "data": {...}},
    {"stage": "tool_execution", "data": {...}},
    {"stage": "synthesis", "data": {...}}
  ]
}
```

### POST /memory/ingest (Phase 4)
Ingest creative snippets into long-term memory.

**Request:**
```json
{
  "items": [
    {
      "text": "The hero's journey begins in darkness",
      "category": "narratives",
      "metadata": {"source": "workshop"}
    },
    {
      "text": "Transformation through adversity",
      "category": "themes",
      "metadata": {}
    }
  ]
}
```

**Response:**
```json
{
  "ingested_count": 2,
  "results": [
    {
      "id": "uuid-1",
      "category": "narratives",
      "status": "ingested",
      "timestamp": "2024-01-01T00:00:00Z"
    },
    {
      "id": "uuid-2",
      "category": "themes",
      "status": "ingested",
      "timestamp": "2024-01-01T00:00:00Z"
    }
  ]
}
```

### POST /memory/preview (Phase 4)
Query and preview items from long-term memory.

**Semantic Search:**
```json
{
  "query": "hero journey narrative",
  "top_k": 5
}
```

**Category Filter:**
```json
{
  "category": "themes",
  "top_k": 10
}
```

**Response:**
```json
{
  "items": [
    {
      "id": "uuid-1",
      "text": "The hero's journey begins in darkness",
      "category": "narratives",
      "similarity": 0.87,
      "metadata": {"source": "workshop"}
    }
  ],
  "count": 1,
  "query": "hero journey narrative",
  "category": null
}
```

### GET /memory/stats (Phase 4)
Get memory statistics.

**Response:**
```json
{
  "categories": {
    "themes": 5,
    "narratives": 3,
    "styles": 2,
    "motifs": 1
  },
  "total_items": 11,
  "valid_categories": ["themes", "narratives", "styles", "user_preferences", "creative_history", "motifs"]
}
```

### GET /memory/categories (Phase 4)
List valid memory categories with descriptions.

**Response:**
```json
{
  "categories": ["themes", "narratives", "styles", "user_preferences", "creative_history", "motifs"],
  "descriptions": {
    "themes": "Core themes and concepts explored",
    "narratives": "Narrative structures and story elements",
    "styles": "Creative styles and approaches",
    "user_preferences": "User-specific preferences and patterns",
    "creative_history": "History of creative outputs",
    "motifs": "Recurring motifs and patterns"
  }
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
pytest tests/test_memory.py

# Run memory tests only
pytest tests/test_memory.py -v

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

## Embedding Service

Phase 4 uses an HTTP embedding service (Ollama-compatible by default).

**Default Configuration:**
- Model: `nomic-embed-text`
- Endpoint: `http://localhost:11434/api/embeddings`
- Timeout: 30 seconds

**Fallback:**
When the embedding service is unavailable, a deterministic hash-based pseudo-embedding is used to prevent system crashes.

## Expected Future Phases

### Phase 5 - Congress Integration
- Voting mechanisms
- Contribution tracking
- Bill analysis interface

### Phase 6 - Sky Protocol
- Message passing framework
- Event-driven communication
- Coordination with Sky orchestrator

### Phase 7 - History Logging
- Creative history logger
- Export functionality
- Audit trail

## License

Copyright 2024. All rights reserved.
