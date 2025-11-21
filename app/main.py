"""
Lyra Agent Entry Point

Run the Lyra agent server.
"""

import uvicorn

from app.config import get_settings


def main():
    """Run the Lyra agent server."""
    settings = get_settings()

    uvicorn.run(
        "app.server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
