# Lyra Agent

Lyra is a creative strategist and conceptual reframing agent designed to assist with innovative thinking, idea generation, and creative problem-solving within a multi-agent system.

## Phase 1 - Foundation

This is the Phase 1 implementation of the Lyra agent, which includes:

- Project scaffolding and directory structure
- FastAPI server with basic endpoints
- Configuration system
- Placeholder services and models
- Basic test suite

### Phase 1 Restrictions

- No creative logic implementation
- No tool integrations
- No RAG (Retrieval-Augmented Generation) functionality
- No reasoning patterns
- No congress interface for multi-agent collaboration

These features will be implemented in subsequent phases.

## Project Structure

```
lyra/
  app/
    main.py           # Entry point
    config.py         # Configuration and settings
    server.py         # FastAPI application factory
    routes/
      __init__.py
      core.py         # Core API endpoints
    models/
      __init__.py
      schema.py       # Pydantic request/response models
    services/
      __init__.py
      lyra_agent.py   # Base Lyra agent class
    memory/
      short_term/     # Short-term memory storage
      long_term/      # Long-term memory storage
    rag/
      __init__.py
      ingest.py       # Document ingestion (placeholder)
      embed.py        # Text embedding (placeholder)
      query.py        # Knowledge retrieval (placeholder)
    logs/
  tests/
    conftest.py
    test_routes.py
    test_health.py
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

**Request:**
```json
{
  "task": "string",
  "payload": {}
}
```

**Response:**
```json
{
  "status": "received",
  "task_id": "uuid",
  "result": {}
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
pytest tests/test_health.py
```

## Expected Future Phases

### Phase 2 - Tools and Reasoning
- Tool integrations for creative tasks
- Basic reasoning patterns
- Enhanced task processing

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
