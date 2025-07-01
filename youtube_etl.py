from googleapiclient.discovery import build
from dotenv import load_dotenv
import pandas as pd
import os

# Load API key from .env or GitHub secret
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# YouTube API client
youtube = build("youtube", "v3", developerKey=API_KEY)

def get_video_stats(video_ids):
    request = youtube.videos().list(
        part="snippet,statistics",
        id=",".join(video_ids)
    )
    response = request.execute()

    data = []
    for item in response["items"]:
        stats = item["statistics"]
        snippet = item["snippet"]
        data.append({
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "published_at": snippet["publishedAt"],
            "views": stats.get("viewCount"),
            "likes": stats.get("likeCount"),
            "comments": stats.get("commentCount"),
            "video_id": item["id"]
        })

    return pd.DataFrame(data)

def main():
    video_ids = ["dQw4w9WgXcQ", "3JZ_D3ELwOQ"]
    df = get_video_stats(video_ids)
    df.to_csv("youtube_stats.csv", index=False)
    print("ETL completed. File saved.")

if __name__ == "__main__":
    main()
