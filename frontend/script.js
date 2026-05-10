// ===============================
// 🌐 BACKEND URL AUTO-DETECT
// ===============================
const BACKEND_URL = window.location.hostname === "localhost" ||
                    window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:8000"
    : "https://ai-mood-based-music-recommender1.onrender.com"; // 👈 replace after Render deploy

console.log("🌐 Backend URL:", BACKEND_URL);

// ===============================
// 🎯 STATE
// ===============================
let playlist        = [];
let currentIndex    = 0;
let player          = null;
let ytReady         = false;
let selectedEmotion = "";
let userClicked     = false;

// ===============================
// 🎨 MOOD COLORS
// ===============================
const moodColors = {
    calm:      "#6EC6CA",
    love:      "#FF6B81",
    sad:       "#5A6C8C",
    joy:       "#FFD93D",
    angry:     "#FF3B3B",
    motivated: "#FF8C00",
    anxious:   "#9B59B6"
};

// ===============================
// 💬 MOOD MESSAGES
// ===============================
const moodMessages = {
    calm:      "🌙 Relax and unwind... let the music soothe your mind.",
    love:      "❤️ Love is in the air... enjoy these romantic vibes.",
    sad:       "💙 It's okay to feel... music will heal you.",
    joy:       "✨ Keep smiling! Let these songs boost your mood.",
    angry:     "🔥 Release the energy... feel the power in music.",
    motivated: "💪 Stay focused! Let the music fuel your grind.",
    anxious:   "🫧 Breathe easy... let the music calm your mind."
};

// ===============================
// 🎬 YOUTUBE API READY
// ===============================
function onYouTubeIframeAPIReady() {
    ytReady = true;
    console.log("✅ YouTube API Ready");
}

// ===============================
// 🔢 CHAR COUNTER
// ===============================
function updateCharCount(textarea) {
    const count = textarea.value.length;
    const el = document.getElementById("charCount");
    if (el) {
        el.textContent = count;
        el.style.color = count > 450
            ? "#FF6B6B"
            : "rgba(255,255,255,0.5)";
    }
}

// ===============================
// 🎯 SELECT EMOTION
// ===============================
function selectEmotion(emotion, btn) {
    selectedEmotion = emotion;
    document.querySelectorAll(".mood-btn").forEach(b => {
        b.classList.remove("active");
    });
    btn.classList.add("active");
}

// ===============================
// 🗑️ CLEAR ALL
// ===============================
function clearAll() {

    // reset state
    playlist        = [];
    currentIndex    = 0;
    selectedEmotion = "";
    userClicked     = false;

    // destroy player
    if (player) {
        try { player.destroy(); } catch (e) {}
        player = null;
    }

    // reset UI elements
    document.getElementById("userText").value        = "";
    document.getElementById("languageSelect").value  = "";
    document.getElementById("charCount").textContent = "0";
    document.getElementById("songs").innerHTML       = "";
    document.getElementById("nowPlaying").textContent = "";
    document.getElementById("songCount").classList.add("hidden");
    document.getElementById("emotion").innerHTML =
        "🤖 Your mood insight will appear here...";

    // reset video player
    const videoContainer = document.getElementById("videoPlayer");
    if (videoContainer) {
        videoContainer.innerHTML = `
            <div class="player-placeholder">
                🎵 Your music will play here
            </div>
        `;
    }

    // reset youtube link
    const ytLink = document.getElementById("ytLink");
    if (ytLink) ytLink.classList.add("hidden");

    // reset mood buttons
    document.querySelectorAll(".mood-btn").forEach(b => {
        b.classList.remove("active");
    });

    // reset background
    document.body.style.background =
        "linear-gradient(135deg, #0f172a, #1e3a8a)";

    const heading = document.querySelector(".left-panel h1");
    if (heading) heading.style.color = "white";

    console.log("🗑️ Cleared all");
}

// ===============================
// ⏱ FORMAT DURATION
// ===============================
function formatDuration(seconds) {
    if (!seconds) return "";
    const m = Math.floor(seconds / 60);
    const s = seconds % 60;
    return `${m}:${s.toString().padStart(2, "0")}`;
}

// ===============================
// 🎧 GET EMOTION + SONGS
// ===============================
async function getEmotion(refresh = false) {

    // destroy old player
    if (player) {
        try { player.destroy(); } catch (e) {}
        player = null;
    }

    // reset video container
    const videoContainer = document.getElementById("videoPlayer");
    if (videoContainer) {
        videoContainer.innerHTML = `
            <div class="player-placeholder">
                🎵 Loading your songs...
            </div>
        `;
    }

    // hide youtube link
    const ytLink = document.getElementById("ytLink");
    if (ytLink) ytLink.classList.add("hidden");

    // reset playlist
    playlist     = [];
    currentIndex = 0;

    // get inputs
    const text          = document.getElementById("userText").value.trim();
    const language      = document.getElementById("languageSelect").value;
    const emotionToSend = selectedEmotion || null;

    // ✅ VALIDATIONS
    if (!text && !emotionToSend) {
        alert("Please type how you feel or select a mood 😊");
        return;
    }
    if (!language) {
        alert("Please select a language 🌐");
        return;
    }

    // ✅ DISABLE ANALYZE BUTTON
    const analyzeBtn = document.getElementById("analyzeBtn");
    if (analyzeBtn) analyzeBtn.disabled = true;

    // show loader
    document.getElementById("loader").classList.remove("hidden");
    document.getElementById("songs").innerHTML = "";
    document.getElementById("songCount").classList.add("hidden");

    try {

        // ✅ FETCH FROM BACKEND
        const res = await fetch(`${BACKEND_URL}/predict`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text:     text,
                emotion:  emotionToSend,
                language: language,
                refresh:  refresh
            })
        });

        if (!res.ok) throw new Error(`Backend error: ${res.status}`);

        const data = await res.json();
        console.log("🎧 RESPONSE:", data);

        const finalEmotion = data.emotion || emotionToSend || "calm";

        // ✅ UPDATE BACKGROUND COLOR
        const color = moodColors[finalEmotion] || "#6c5ce7";
        document.body.style.background =
            `linear-gradient(135deg, ${color}33, #0f172a)`;

        const heading = document.querySelector(".left-panel h1");
        if (heading) heading.style.color = color;

        document.documentElement.style
            .setProperty("--accent-color", color);

        // ✅ SET PLAYLIST
        playlist     = Array.isArray(data.songs) ? data.songs : [];
        currentIndex = 0;

        // ✅ SONG COUNT
        const songCountEl = document.getElementById("songCount");
        if (songCountEl && playlist.length > 0) {
            songCountEl.textContent =
                `🎵 ${playlist.length} songs found for "${finalEmotion}" mood`;
            songCountEl.classList.remove("hidden");
        }

        // ✅ RENDER SONG LIST
        renderSongs();

        // ✅ AUTOPLAY FIRST SONG
        if (playlist.length > 0) {
            setTimeout(() => {
                if (ytReady) {
                    playSong(0);
                } else {
                    const retry = setInterval(() => {
                        if (ytReady) {
                            clearInterval(retry);
                            playSong(0);
                        }
                    }, 300);
                }
            }, 400);
        } else {
            showNoSongs();
        }

        // ✅ MOOD BOX
        const moodNote = moodMessages[finalEmotion] || "🎧 Enjoy your music";
        document.getElementById("emotion").innerHTML = `
            🎯 Detected Mood: <b>${finalEmotion.toUpperCase()}</b><br>
            💬 ${moodNote}<br>
            <small style="opacity:0.6; font-size:0.75rem;">
                ⚠️ Some videos may be unavailable due to YouTube restrictions.
                Use the ▶ Open in YouTube button to watch directly.
            </small>
        `;

    } catch (err) {
        console.error("❌ ERROR:", err);
        showError(err.message);
    }

    // ✅ HIDE LOADER + RE-ENABLE BUTTON
    document.getElementById("loader").classList.add("hidden");
    if (analyzeBtn) analyzeBtn.disabled = false;
}

// ===============================
// 🎵 RENDER SONGS
// ===============================
function renderSongs() {

    const container = document.getElementById("songs");
    container.innerHTML = "";

    playlist.forEach((song, index) => {

        if (!song || !song.videoId) return;

        const div = document.createElement("div");
        div.className = "song-card";

        // ✅ STAGGERED ANIMATION
        div.style.animationDelay = `${index * 0.06}s`;

        div.onclick = () => playSong(index, true);

        const duration = song.duration
            ? `<div class="duration">⏱ ${formatDuration(song.duration)}</div>`
            : "";

        div.innerHTML = `
            <img
                src="${song.thumbnail}"
                alt="${song.name}"
                onerror="this.src='https://img.youtube.com/vi/${song.videoId}/hqdefault.jpg'"
            />
            <div class="song-info">
                <h4>${song.name}</h4>
                <p>${song.artist || "Unknown Artist"}</p>
                ${duration}
            </div>
            <div class="play-icon">▶</div>
        `;

        container.appendChild(div);
    });
}

// ===============================
// 🎬 CREATE / LOAD PLAYER
// ===============================
function createPlayer(videoId) {

    if (!ytReady) return;

    // ✅ UPDATE YOUTUBE LINK
    const ytLink = document.getElementById("ytLink");
    if (ytLink) {
        ytLink.href = `https://www.youtube.com/watch?v=${videoId}`;
        ytLink.classList.remove("hidden");
    }

    if (!player) {

        // clear container first
        const container = document.getElementById("videoPlayer");
        if (container) container.innerHTML = "";

        player = new YT.Player("videoPlayer", {
            height:  "280",
            width:   "100%",
            videoId: videoId,
            playerVars: {
                autoplay:       1,
                rel:            0,
                modestbranding: 1
            },
            events: {

                onReady: (event) => {
                    event.target.playVideo();
                },

                // ✅ AUTO NEXT WHEN SONG ENDS
                onStateChange: (event) => {
                    if (event.data === YT.PlayerState.ENDED) {
                        console.log("⏭ Song ended → next");
                        nextSong();
                    }
                },

                onError: (event) => {
                    console.log("❌ Video error:", event.data);
                    handleVideoError(videoId);
                }
            }
        });

    } else {
        player.loadVideoById(videoId);
    }
}

// ===============================
// ❌ HANDLE VIDEO ERROR
// ===============================
function handleVideoError(videoId) {

    const emotionEl = document.getElementById("emotion");

    if (userClicked) {

        // manually clicked → show message + skip after 5s
        if (emotionEl) {
            emotionEl.innerHTML += `
                <br>
                <span style="color:#ffb3b3; font-size:0.82rem;">
                    ⚠️ This video is unavailable. Opening next song in 5s...<br>
                    Or use the ▶ Open in YouTube button above.
                </span>
            `;
        }
        setTimeout(() => nextSong(), 5000);

    } else {
        // autoplay → skip instantly
        nextSong();
    }
}

// ===============================
// ▶ PLAY SONG
// ===============================
function playSong(index, isUserClick = false) {

    if (!playlist.length) return;

    const song = playlist[index];
    if (!song || !song.videoId) {
        nextSong();
        return;
    }

    currentIndex = index;
    userClicked  = isUserClick;

    if (!ytReady) {
        setTimeout(() => playSong(index, isUserClick), 500);
        return;
    }

    // ✅ UPDATE NOW PLAYING
    const nowPlaying = document.getElementById("nowPlaying");
    if (nowPlaying) {
        nowPlaying.textContent =
            `▶ Now Playing: ${song.name} — ${song.artist || "Unknown"}`;
    }

    createPlayer(song.videoId);
    highlightActive(index);
}

// ===============================
// ⏭ NEXT SONG
// ===============================
function nextSong() {
    if (!playlist.length) return;
    currentIndex = (currentIndex + 1) % playlist.length;
    playSong(currentIndex, false);
}

// ===============================
// ⏮ PREVIOUS SONG
// ===============================
function prevSong() {
    if (!playlist.length) return;
    currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
    playSong(currentIndex, false);
}

// ===============================
// 🎯 HIGHLIGHT ACTIVE SONG
// ===============================
function highlightActive(index) {
    document.querySelectorAll(".song-card").forEach((card, i) => {
        card.classList.toggle("active", i === index);
    });

    // ✅ SCROLL INTO VIEW
    const cards = document.querySelectorAll(".song-card");
    if (cards[index]) {
        cards[index].scrollIntoView({
            behavior: "smooth",
            block:    "nearest"
        });
    }
}

// ===============================
// ⚠ NO SONGS UI
// ===============================
function showNoSongs() {
    document.getElementById("songs").innerHTML = `
        <div style="
            text-align: center;
            padding: 40px 20px;
            color: rgba(255,255,255,0.5);
        ">
            <div style="font-size: 2rem; margin-bottom: 10px;">🎵</div>
            <p>No songs found for this mood.</p>
            <p style="font-size:0.8rem; margin-top:6px;">
                Try a different mood or language.
            </p>
        </div>
    `;
}

// ===============================
// ❌ ERROR UI
// ===============================
function showError(msg = "") {
    document.getElementById("songs").innerHTML = `
        <div style="
            text-align: center;
            padding: 40px 20px;
            color: rgba(255,100,100,0.8);
        ">
            <div style="font-size: 2rem; margin-bottom: 10px;">❌</div>
            <p>Something went wrong.</p>
            <p style="font-size:0.8rem; margin-top:6px; color:rgba(255,255,255,0.4)">
                ${msg || "Make sure the backend server is running."}
            </p>
        </div>
    `;
}