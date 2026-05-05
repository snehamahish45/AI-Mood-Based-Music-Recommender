import yt_dlp
import random

# 🔥 store previous songs to avoid repetition
previous_ids = set()


def get_songs_by_emotion(emotion, language):

    mood_map = {
        "calm": "chill songs",
        "sad": "sad songs",
        "love": "romantic songs",
        "joy": "happy songs",
        "angry": "rap songs"
    }

    keyword = mood_map.get(emotion, emotion)

    # 🔥 RANDOM KEYWORDS (VERY IMPORTANT)
    variations = ["latest", "new", "trending", "top", "viral"]
    random_word = random.choice(variations)

    query = f"{random_word} {language} {keyword}"

    print("🔍 QUERY:", query)

    ydl_opts = {
        'quiet': True,
        'skip_download': True
    }

    songs = []

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch20:{query}", download=False)

        entries = results.get("entries", [])
        print("📦 RAW RESULTS:", len(entries))

        # 🔥 SHUFFLE RESULTS (IMPORTANT)
        random.shuffle(entries)

        for video in entries:

            if not video:
                continue

            vid = video.get("id")
            title = video.get("title")

            if not vid or not title:
                continue

            # 🚫 SKIP PREVIOUS SONGS
            if vid in previous_ids:
                continue

            previous_ids.add(vid)

            songs.append({
                "name": title,
                "artist": video.get("uploader", "Unknown"),
                "thumbnail": video.get("thumbnail"),
                "videoId": vid
            })

            if len(songs) >= 10:
                break

    except Exception as e:
        print("❌ yt-dlp ERROR:", e)

    # 🔥 FALLBACK (if still empty)
    if len(songs) == 0:
        print("⚠️ EMPTY → USING FALLBACK")

        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                results = ydl.extract_info("ytsearch20:trending songs", download=False)

            entries = results.get("entries", [])
            random.shuffle(entries)

            for video in entries[:10]:
                songs.append({
                    "name": video.get("title"),
                    "artist": video.get("uploader"),
                    "thumbnail": video.get("thumbnail"),
                    "videoId": video.get("id")
                })

        except Exception as e:
            print("❌ FALLBACK ERROR:", e)

    print("✅ FINAL SONG COUNT:", len(songs))

    return songs[:10]