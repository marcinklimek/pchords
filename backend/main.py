"""
FastAPI backend for PChords.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from .api import chords, midi
from .core.models import ChordSet


# Default chord sets
DEFAULT_CHORD_SETS = [
    ChordSet(
        id="beginners",
        name="Beginners - Basic Chords",
        enabled=True,
        qualities=["", "m"],
        scales=["maj"],
        inversions=["root"],
        difficulty="easy"
    ),
    ChordSet(
        id="jazz_ninth",
        name="Jazz - 9th Chords",
        enabled=True,
        qualities=["M9", "m9"],
        scales=["maj", "min"],
        inversions=["from_3rd", "from_7th"],
        difficulty="medium"
    ),
    ChordSet(
        id="jazz_altered",
        name="Jazz - Altered Chords",
        enabled=False,
        qualities=["7#9#5", "7b9b5"],
        scales=["maj", "min"],
        inversions=["from_3rd", "from_7th"],
        difficulty="hard"
    )
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup: Initialize chord generator
    await chords.init_generator(DEFAULT_CHORD_SETS)
    print("✅ PChords backend started")
    print("📊 Initialized with", len(DEFAULT_CHORD_SETS), "chord sets")

    yield

    # Shutdown
    print("🛑 PChords backend shutting down")


# Create FastAPI app
app = FastAPI(
    title="PChords API",
    description="Backend API for PChords - Piano Chord Practice Tool",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative frontend port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chords.router)
app.include_router(midi.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "PChords API",
        "version": "2.0.0",
        "status": "running",
        "docs": "/docs",
        "endpoints": {
            "chords": "/api/chords",
            "midi_websocket": "/ws/midi",
            "midi_status": "/ws/midi/status"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
