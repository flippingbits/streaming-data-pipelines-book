from datetime import datetime, timedelta
import random

from fastapi import FastAPI
from faker import Faker

Faker.seed(42)

app = FastAPI()
fake = Faker()

devices = ["Chrome", "Edge", "Firefox"]
pages = ["/", "/cart", "/contact", "/privacy-policy", "/products"]
timestamp_format = "%Y-%m-%dT%H:%M:%S.%f"


def generate_fake_visit(since):
    now = datetime.now()
    since_ts = now

    if since is not None:
        # parse query parameter to datetime
        since_ts = datetime.strptime(since, timestamp_format)
        fake.date_between(start_date=since_ts, end_date=now)
        # determine timedelta
        delta = now - since_ts
        # convert timedelta to seconds
        delta_seconds = (delta.days * 24 * 60 * 60) + delta.seconds
        # generate random timestamp between since and now
        since_ts = since_ts + timedelta(seconds=random.randrange(delta_seconds))

    return {
        "device": random.choice(devices),
        "domain": "excellenttoys.org",
        "ip": fake.ipv4(),
        "page": random.choice(pages),
        "timestamp": since_ts.strftime(timestamp_format),
    }


# Usage of this fake API:
# Call `/visitors` to get visitor data with the timestamp set to the current time
# Call `/visitors=since?timestamp`, where timestamp is in the format `%Y-%m-%dT%H:%M:%S.%f`, to get visitors that occurred since the provided timestamp
@app.get("/visitors")
async def visitors(since: str = None, count: int = 25):
    visitors = []
    for _ in range(count):
        visitors.append(generate_fake_visit(since))
    return visitors
