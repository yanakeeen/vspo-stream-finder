import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen


BASE_URL = "https://holodex.net/api/v2"

API_KEY = os.environ.get("HOLODEX_API_KEY")

if not API_KEY:
    raise RuntimeError("HOLODEX_API_KEY is not set")


TEST_VIDEOS = {
    "valorant": "9nxGMT51JK4",
    "minecraft": "pQYpSlZSsY0",
    "apex": "YkySMsypko8",
    "lol": "JVM4DPrDcP4",
}


def get_json(path: str, params: dict | None = None):
    url = f"{BASE_URL}{path}"

    if params:
        url += "?" + urlencode(params)

    request = Request(
        url,
        headers={
            "X-APIKEY": API_KEY,
            "User-Agent": "vspo-stream-finder-poc/0.1",
        },
    )

    with urlopen(request, timeout=20) as response:
        return json.load(response)


def simplify(video: dict) -> dict:
    channel = video.get("channel") or {}

    video_id = video.get("id")

    return {
        "id": video_id,
        "youtube_url": (
            f"https://www.youtube.com/watch?v={video_id}"
            if video_id
            else None
        ),
        "title": video.get("title"),
        "channel_id": video.get("channel_id") or channel.get("id"),
        "channel_name": channel.get("name"),
        "published_at": video.get("published_at"),
        "start_scheduled": video.get("start_scheduled"),
        "start_actual": video.get("start_actual"),
        "end_actual": video.get("end_actual"),
        "duration": video.get("duration"),
        "topic_id": video.get("topic_id"),
        "type": video.get("type"),
        "status": video.get("status"),
    }


print("=== Known game samples ===")

for game, video_id in TEST_VIDEOS.items():
    video = get_json(f"/videos/{video_id}")

    print(f"\n--- expected game: {game} ---")
    print(
        json.dumps(
            simplify(video),
            ensure_ascii=False,
            indent=2,
        )
    )


print("\n=== VSpo JP channels ===")

channels = get_json(
    "/channels",
    {
        "org": "VSpo",
        "lang": "ja",
        "limit": 50,
    },
)

print(f"channel count returned: {len(channels)}")

for channel in channels:
    print(
        channel.get("id"),
        channel.get("name"),
        channel.get("english_name"),
    )


print("\n=== Latest VSpo past videos ===")

recent = get_json(
    "/videos",
    {
        "org": "VSpo",
        "type": "stream",
        "status": "past",
        "sort": "available_at",
        "order": "desc",
        "limit": 50,
    },
)

missing_topic = sum(
    1 for video in recent
    if not video.get("topic_id")
)

print(f"videos returned: {len(recent)}")
print(f"topic missing: {missing_topic}")

for video in recent[:10]:
    print(
        json.dumps(
            simplify(video),
            ensure_ascii=False,
            indent=2,
        )
    )


print("\n=== Oldest VSpo videos available ===")

oldest = get_json(
    "/videos",
    {
        "org": "VSpo",
        "type": "stream",
        "status": "past",
        "sort": "available_at",
        "order": "asc",
        "limit": 10,
    },
)

for video in oldest:
    print(
        json.dumps(
            simplify(video),
            ensure_ascii=False,
            indent=2,
        )
    )