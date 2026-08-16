import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen


API_KEY = os.environ.get("YOUTUBE_API_KEY")

if not API_KEY:
    raise RuntimeError("YOUTUBE_API_KEY is not set")


VIDEO_IDS = [
    # 橘ひなの
    "NzpocDBMiEA",
    "Gg_as9k-Rig",
    "WiahstHgunk",
    "2dgGZhwlvpw",
    "Mcz2GZn7YZU",
    "OM3D6xux8Cw",

    # 紡木こかげ
    "8pmrz9kLd-A",
    "7AOmFoD_GyM",

    # 神成きゅぴ
    "5lS9lMfvyNs",
    "1J-ZaMboApg",
    "01cCr-e2yU4",
    "w9mSN4cybt4",
    "hCE-qHr-0bE",
    "SnJQ8IS80TQ",

    # 胡桃のあ
    "VAYkLafTCcQ",

    # 過去データで start_actual=None だった要確認動画
    "-BU_AyNM7I8",
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