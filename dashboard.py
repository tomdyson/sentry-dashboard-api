import os
import json
import arrow
import requests
from dotenv import load_dotenv

load_dotenv()

EXCLUDE_OLDER_THAN = int(os.environ.get("EXCLUDE_OLDER_THAN", 3600 * 1))  # one hour
SENTRY_API_KEY = os.environ.get("SENTRY_API_KEY")
EVENT_TYPES = [
    ("form submissions", os.environ.get("FORM_SUBMISSION_ID")),
    ("completed transactions", os.environ.get("TRANSACTION_COMPLETED_ID")),
    ("attribute errors", os.environ.get("ATTRIBUTE_ERROR_ID")),
]


def delta_as_hours_etc(delta):
    hours, remainder = divmod(delta.seconds, 3600)  # Get Hour
    minutes, seconds = divmod(remainder, 60)
    return (hours, minutes, seconds)


def fetch_events(issue_id):
    url = f"https://sentry.io/api/0/issues/{issue_id}/events/"
    headers = {"Authorization": f"Bearer {SENTRY_API_KEY}"}
    resp = requests.get(url, headers=headers)
    events = resp.json()
    reduced_events = {"issue_id": issue_id, "events": []}
    now = arrow.utcnow()
    for event in events:
        timestamp = arrow.get(event["dateCreated"])
        if timestamp > now.shift(seconds=-1 * EXCLUDE_OLDER_THAN):
            reduced_events["events"].append(
                {
                    "timestamp": timestamp.format(),
                    "humanised_time": timestamp.humanize(),
                    "event_id": event["eventID"],
                }
            )
            # print(f"{hours}hrs, {minutes}mins, {seconds}secs - {event['eventID']}")
    return reduced_events


def event_report(events, event_name):
    print(f"# {event_name} in the last {int(EXCLUDE_OLDER_THAN / 3600)} hour(s)")
    for event in events["events"]:
        print(f"{event['timestamp']} - {event['humanised_time']} - {event['event_id']}")


def run_reports():
    for event_type in EVENT_TYPES:
        event_report(fetch_events(event_type[1]), event_type[0])


if __name__ == "__main__":
    run_reports()
