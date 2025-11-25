"""
FastAPI backend for PChords.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .api import chords, midi, scales, progressions
from .core.models import ChordSet, ChordQuality, VoicingType
from .core.theory.notes import NoteName

# Default chord sets
DEFAULT_CHORD_SETS = [
    ChordSet(
        id="beginners_major",
        name="Beginners - Major Triads",
        enabled=True,
        qualities=[ChordQuality.MAJOR],
        roots=[NoteName.C, NoteName.F, NoteName.G],
        voicing_types=[VoicingType.CLOSE],
        difficulty="easy"
    ),
    ChordSet(
        id="jazz_ii_v_i",
        name="Jazz - II-V-I Shells",
        enabled=True,
        qualities=[ChordQuality.MINOR_7, ChordQuality.DOMINANT_7, ChordQuality.MAJOR_7],
        roots=[NoteName.D, NoteName.G, NoteName.C],
        voicing_types=[VoicingType.SHELL_3_7, VoicingType.SHELL_7_3],
        difficulty="medium"
    ),
    ChordSet(
        id="rootless_voicings",
        name="Rootless Voicings (Bill Evans)",
        enabled=False,
        qualities=[ChordQuality.MINOR_9, ChordQuality.DOMINANT_13, ChordQuality.MAJOR_9],
        roots=[NoteName.C, NoteName.F, NoteName.B_FLAT, NoteName.E_FLAT],
        voicing_types=[VoicingType.ROOTLESS_A, VoicingType.ROOTLESS_B],
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
        "http://localhost:3000",
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
app.include_router(scales.router)
app.include_router(progressions.router)

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
