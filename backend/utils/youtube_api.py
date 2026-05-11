import yt_dlp
import random

def get_songs_by_emotion(emotion, language):

    mood_map = {
        "calm":      "chill relaxing songs",
        "sad":       "sad emotional songs",
        "love":      "romantic love songs",
        "joy":       "happy upbeat songs",
        "angry":     "rap energy songs",
        "motivated": "motivational workout songs",
        "anxious":   "soothing anxiety relief songs"
    }

    keyword  = mood_map.get(emotion, f"{emotion} songs")
    variations = ["latest", "new", "trending", "top", "viral", "best", "popular"]
    random_word = random.choice(variations)
    query = f"{random_word} {language} {keyword}"

    print(f"🔍 QUERY: {query}")

    # ✅ BETTER OPTIONS TO BYPASS RENDER RESTRICTIONS
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': True,   # ✅ faster — no full extraction
        'no_warnings': True,
        'ignoreerrors': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
        }
    }

    songs = []
    previous_ids = set()

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(
                f"ytsearch15:{query}",
                download=False
            )

        entries = results.get("entries", []) if results else []
        print(f"📦 RAW RESULTS: {len(entries)}")

        random.shuffle(entries)

        for video in entries:
            if not video:
                continue

            vid   = video.get("id")
            title = video.get("title")

            if not vid or not title:
                continue

            if vid in previous_ids:
                continue

            # ✅ with extract_flat, duration may be None — skip that check
            duration = video.get("duration") or 0

            # only filter if duration is available
            if duration and (duration > 600 or duration < 60):
                continue

            previous_ids.add(vid)

            thumbnail = video.get("thumbnail")
            if not thumbnail:
                thumbnail = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"

            songs.append({
                "name":      title,
                "artist":    video.get("uploader") or video.get("channel") or "Unknown Artist",
                "thumbnail": thumbnail,
                "videoId":   vid,
                "duration":  duration
            })

            if len(songs) >= 10:
                break

    except Exception as e:
        print(f"❌ yt-dlp ERROR: {e}")

    # ✅ FALLBACK
    if not songs:
        print("⚠️ EMPTY → FALLBACK")
        fallback_queries = [
            f"trending {language} songs",
            f"popular {language} music",
            f"best {language} songs 2024"
        ]

        for fallback_query in fallback_queries:
            if songs:
                break

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    results = ydl.extract_info(
                        f"ytsearch15:{fallback_query}",
                        download=False
                    )

                entries = results.get("entries", []) if results else []
                random.shuffle(entries)

                for video in entries:
                    if not video:
                        continue

                    vid   = video.get("id")
                    title = video.get("title")

                    if not vid or not title:
                        continue

                    thumbnail = video.get("thumbnail")
                    if not thumbnail:
                        thumbnail = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"

                    songs.append({
                        "name":      title,
                        "artist":    video.get("uploader") or video.get("channel") or "Unknown",
                        "thumbnail": thumbnail,
                        "videoId":   vid,
                        "duration":  video.get("duration") or 0
                    })

                    if len(songs) >= 10:
                        break

            except Exception as e:
                print(f"❌ FALLBACK ERROR: {e}")

    print(f"✅ FINAL SONG COUNT: {len(songs)}")
    return songs[:10]
