import yt_dlp
import random

def get_songs_by_emotion(emotion, language):

    # ✅ EXPANDED MOOD MAP (includes new emotions)
    mood_map = {
        "calm":      "chill relaxing songs",
        "sad":       "sad emotional songs",
        "love":      "romantic love songs",
        "joy":       "happy upbeat songs",
        "angry":     "rap energy songs",
        "motivated": "motivational workout songs",
        "anxious":   "soothing anxiety relief songs"
    }

    keyword = mood_map.get(emotion, f"{emotion} songs")

    # ✅ RANDOM VARIATION TO AVOID SAME RESULTS
    variations = ["latest", "new", "trending", "top", "viral", "best", "popular"]
    random_word = random.choice(variations)

    query = f"{random_word} {language} {keyword}"
    print(f"🔍 QUERY: {query}")

    # ✅ LOCAL previous_ids (not global — resets each call, avoids stale data)
    previous_ids = set()

    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'extract_flat': False,
    }

    songs = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(
                f"ytsearch20:{query}",
                download=False
            )

        entries = results.get("entries", [])
        print(f"📦 RAW RESULTS: {len(entries)}")

        # ✅ SHUFFLE FOR VARIETY
        random.shuffle(entries)

        for video in entries:

            if not video:
                continue

            vid      = video.get("id")
            title    = video.get("title")
            duration = video.get("duration") or 0

            if not vid or not title:
                continue

            # ✅ SKIP DUPLICATES
            if vid in previous_ids:
                continue

            # ✅ SKIP LIVESTREAMS & VERY LONG VIDEOS (over 10 mins)
            if duration == 0 or duration > 600:
                print(f"⏩ Skipping long/live video: {title} ({duration}s)")
                continue

            # ✅ SKIP SHORT VIDEOS (under 1 min — usually ads/clips)
            if duration < 60:
                print(f"⏩ Skipping short video: {title} ({duration}s)")
                continue

            previous_ids.add(vid)

            # ✅ SAFE THUMBNAIL FALLBACK
            thumbnail = video.get("thumbnail")
            if not thumbnail:
                thumbnail = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"

            songs.append({
                "name":      title,
                "artist":    video.get("uploader", "Unknown Artist"),
                "thumbnail": thumbnail,
                "videoId":   vid,
                "duration":  duration
            })

            if len(songs) >= 10:
                break

    except Exception as e:
        print(f"❌ yt-dlp ERROR: {e}")

    # ✅ FALLBACK IF EMPTY
    if not songs:
        print("⚠️ EMPTY → USING FALLBACK QUERY")
        fallback_query = f"trending {language} songs"

        try:
            with yt_dlp.YoutubeDL({'quiet': True, 'skip_download': True}) as ydl:
                results = ydl.extract_info(
                    f"ytsearch20:{fallback_query}",
                    download=False
                )

            entries = results.get("entries", [])
            random.shuffle(entries)

            for video in entries:
                if not video:
                    continue

                vid      = video.get("id")
                title    = video.get("title")
                duration = video.get("duration") or 0

                if not vid or not title:
                    continue

                if duration == 0 or duration > 600 or duration < 60:
                    continue

                thumbnail = video.get("thumbnail")
                if not thumbnail:
                    thumbnail = f"https://img.youtube.com/vi/{vid}/hqdefault.jpg"

                songs.append({
                    "name":      title,
                    "artist":    video.get("uploader", "Unknown Artist"),
                    "thumbnail": thumbnail,
                    "videoId":   vid,
                    "duration":  duration
                })

                if len(songs) >= 10:
                    break

        except Exception as e:
            print(f"❌ FALLBACK ERROR: {e}")

    print(f"✅ FINAL SONG COUNT: {len(songs)}")
    return songs[:10]