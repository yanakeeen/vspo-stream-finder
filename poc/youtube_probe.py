import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen


API_KEY = os.environ.get("YOUTUBE_API_KEY")

if not API_KEY:
    raise RuntimeError("YOUTUBE_API_KEY is not set")


VIDEO_IDS = [
    "9nxGMT51JK4",
    "pQYpSlZSsY0",
    "YkySMsypko8",
    "JVM4DPrDcP4",
]


params = {
    "part": ",".join(
        [
            "snippet",
            "contentDetails",
            "liveStreamingDetails",
            "topicDetails",
            "status",
        ]
    ),
    "id": ",".join(VIDEO_IDS),
    "key": API_KEY,
}

url = (
    "https://www.googleapis.com/youtube/v3/videos?"
    + urlencode(params)
)

with urlopen(url, timeout=20) as response:
    data = json.load(response)


for video in data.get("items", []):
    snippet = video.get("snippet", {})
    content = video.get("contentDetails", {})
    live = video.get("liveStreamingDetails")

    result = {
        "id": video.get("id"),
        "title": snippet.get("title"),
        "channel_id": snippet.get("channelId"),
        "channel_title": snippet.get("channelTitle"),
        "published_at": snippet.get("publishedAt"),
        "category_id": snippet.get("categoryId"),
        "live_broadcast_content": snippet.get(
            "liveBroadcastContent"
        ),
        "duration": content.get("duration"),
        "live_streaming_details": live,
        "topic_categories": (
            video.get("topicDetails", {})
            .get("topicCategories")
        ),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))