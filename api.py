from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dashboard import (
    fetch_events,
    EVENT_TYPES,
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {event_type[0]: fetch_events(event_type[1]) for event_type in EVENT_TYPES}
