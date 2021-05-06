from fastapi import FastAPI
from dashboard import (
    fetch_events,
    EVENT_TYPES,
)

app = FastAPI()


@app.get("/")
async def root():
    return {event_type[0]: fetch_events(event_type[1]) for event_type in EVENT_TYPES}
