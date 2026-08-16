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
        "lang=", channel.get("lang"),
        "org=", channel.get("org"),
        "type=", channel.get("type"),
        "inactive=", channel.get("inactive"),
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

print("\n=== Holodex live info comparison ===")

LIVE_INFO_TEST_VIDEOS = {
    "normal_short": "lyYDIRmro94",
    "normal_clip": "Vh7XBUEFfWA",
    "live_lol": "XKR7iMRpU8k",
    "live_biohazard": "HQ0sT_4vX6k",
    "live_valorant": "_e2tqI5j0ds",
}


def print_video(label: str, video: dict | None):
    print(f"\n[{label}]")

    if not video:
        print("NO DATA")
        return

    print(
        json.dumps(
            simplify(video),
            ensure_ascii=False,
            indent=2,
        )
    )


for label, video_id in LIVE_INFO_TEST_VIDEOS.items():
    print(f"\n--- {label}: {video_id} ---")

    default_result = get_json(
        "/videos",
        {
            "id": video_id,
            "limit": 1,
        },
    )

    live_info_result = get_json(
        "/videos",
        {
            "id": video_id,
            "include": "live_info",
            "limit": 1,
        },
    )

    detail_result = get_json(
        f"/videos/{video_id}"
    )

    print_video(
        "GET /videos",
        default_result[0] if default_result else None,
    )

    print_video(
        "GET /videos?include=live_info",
        live_info_result[0] if live_info_result else None,
    )

    print_video(
        "GET /videos/{videoId}",
        detail_result,
    )

print("\n=== Channel sample analysis ===")

SAMPLE_CHANNELS = {
    "橘ひなの": "UCvUc0m317LWTTPZoBQV479A",
    "紡木こかげ": "UC-WX1CXssCtCtc2TNIRnJzg",
    "神成きゅぴ": "UCMp55EbT_ZlqiMS3lCj01BQ",
    "胡桃のあ": "UCIcAj6WkJ8vZ7DeJVgmeqKw",
}


for name, channel_id in SAMPLE_CHANNELS.items():
    videos = get_json(
        "/videos",
        {
            "channel_id": channel_id,
            "type": "stream",
            "status": "past",
            "include": "live_info",
            "sort": "available_at",
            "order": "desc",
            "limit": 50,
        },
    )

    actual_streams = [
        video
        for video in videos
        if video.get("start_actual") is not None
    ]

    missing_topic = [
        video
        for video in actual_streams
        if not video.get("topic_id")
    ]

    no_start = [
        video
        for video in videos
        if video.get("start_actual") is None
    ]

    print("start_actual missing:")

    for video in no_start:
        print(
            f"  {video.get('id')} | "
            f"{video.get('topic_id')} | "
            f"{video.get('duration')}s | "
            f"{video.get('title')}"
        )

    topics = {}

    for video in actual_streams:
        topic = video.get("topic_id") or "<missing>"
        topics[topic] = topics.get(topic, 0) + 1

    print(f"\n--- {name} ---")
    print(f"uploads returned: {len(videos)}")
    print(f"livestream archives: {len(actual_streams)}")
    print(f"livestream topic missing: {len(missing_topic)}")
    print("topics:")

    for topic, count in sorted(
        topics.items(),
        key=lambda item: (-item[1], item[0]),
    ):
        print(f"  {topic}: {count}")

    if missing_topic:
        print("missing topic titles:")

        for video in missing_topic:
            print(
                f"  {video.get('id')} "
                f"{video.get('title')}"
            )

    print("latest livestream samples:")

    for video in actual_streams[:10]:
        print(
            f"  {video.get('id')} | "
            f"{video.get('topic_id')} | "
            f"{video.get('title')}"
        )

print("\n=== Oldest channel videos ===")

for name, channel_id in SAMPLE_CHANNELS.items():
    oldest = get_json(
        "/videos",
        {
            "channel_id": channel_id,
            "type": "stream",
            "status": "past",
            "include": "live_info",
            "sort": "available_at",
            "order": "asc",
            "limit": 5,
        },
    )

    print(f"\n--- {name} ---")

    for video in oldest:
        print(
            f"{video.get('id')} | "
            f"available={video.get('available_at')} | "
            f"start={video.get('start_actual')} | "
            f"topic={video.get('topic_id')} | "
            f"{video.get('title')}"
        )

print("\n=== Pagination test ===")

PAGINATION_CHANNEL = {
    "name": "橘ひなの",
    "channel_id": "UCvUc0m317LWTTPZoBQV479A",
}


def get_video_page(channel_id: str, offset: int):
    return get_json(
        "/videos",
        {
            "channel_id": channel_id,
            "type": "stream",
            "status": "past",
            "include": "live_info",
            "sort": "available_at",
            "order": "desc",
            "limit": 50,
            "offset": offset,
            "paginated": "1",
        },
    )


page1 = get_video_page(
    PAGINATION_CHANNEL["channel_id"],
    offset=0,
)

page2 = get_video_page(
    PAGINATION_CHANNEL["channel_id"],
    offset=50,
)

items1 = page1["items"]
items2 = page2["items"]

ids1 = {video["id"] for video in items1}
ids2 = {video["id"] for video in items2}

overlap = ids1 & ids2

print(f"channel: {PAGINATION_CHANNEL['name']}")
print(f"total: {page1['total']}")
print(f"page1 count: {len(items1)}")
print(f"page2 count: {len(items2)}")
print(f"overlap: {len(overlap)}")

if items1:
    print(
        "page1 range:",
        items1[0].get("available_at"),
        "->",
        items1[-1].get("available_at"),
    )

if items2:
    print(
        "page2 range:",
        items2[0].get("available_at"),
        "->",
        items2[-1].get("available_at"),
    )

print("\npage1 last:")
if items1:
    print(
        items1[-1]["id"],
        items1[-1].get("available_at"),
        items1[-1].get("title"),
    )

print("\npage2 first:")
if items2:
    print(
        items2[0]["id"],
        items2[0].get("available_at"),
        items2[0].get("title"),
    )