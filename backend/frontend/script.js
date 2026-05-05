let playlist = [];
let currentIndex = 0;
let player;
let ytReady = false;
let selectedEmotion = "";
let userClicked = false;

const moodColors = {
    calm: "#6EC6CA",     // soft teal
    love: "#FF6B81",     // pink/red
    sad: "#5A6C8C",      // blue gray
    joy: "#FFD93D",      // yellow
    angry: "#FF3B3B"     // red
};

const moodMessages = {
    calm: "🌙 Relax and unwind... let the music soothe your mind.",
    love: "❤️ Love is in the air... enjoy these romantic vibes.",
    sad: "💙 It's okay to feel... music will heal you.",
    joy: "✨ Keep smiling! Let these songs boost your mood.",
    angry: "🔥 Release the energy... feel the power in music."
};

// ===============================
// 🎬 YOUTUBE API READY
// ===============================
function onYouTubeIframeAPIReady() {
    ytReady = true;
}

// ===============================
// 🎯 SELECT MOOD
// ===============================
function selectEmotion(emotion, btn) {
    selectedEmotion = emotion;

    document.querySelectorAll(".mood-btn").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
}

// ===============================
// 🎧 GET EMOTION + SONGS
// ===============================
async function getEmotion(refresh = false) {

    // 🔥 RESET PLAYER (important)
    if (player) {
        try {
            player.destroy();
        } catch (e) {}
        player = null;
    }

    // 🔥 CLEAR VIDEO CONTAINER
    const videoContainer = document.getElementById("videoPlayer");
    if (videoContainer) {
        videoContainer.innerHTML = "";
    }

    playlist = [];
    currentIndex = 0;

    const text = document.getElementById("userText").value.trim();
    const language = document.getElementById("languageSelect").value;

    // 🔥 FIX: ensure emotion always exists
    let emotionToSend = selectedEmotion || null;

    // if no text AND no mood → stop
    if (!text && !emotionToSend) {
        alert("Please type something or select a mood");
        return;
    }

    if (!language) {
        alert("Please select a language");
        return;
    }

    document.getElementById("loader").classList.remove("hidden");

    try {
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                text: text,
                emotion: emotionToSend,
                language: language,
                refresh: refresh
            })
        });

        const data = await res.json();

        console.log("🎧 RESPONSE:", data);

        // 🔥 FIX: safe emotion fallback
        const finalEmotion = data.emotion || emotionToSend || "calm";

        // 🎨 APPLY MOOD COLOR
        const color = moodColors[finalEmotion] || "#6c5ce7";

        document.body.style.background =
            `linear-gradient(135deg, ${color}, #0f172a)`;

        // heading color
        const heading = document.querySelector(".left-panel h1");
        if (heading) heading.style.color = color;

        // accent color (buttons, active song)
        document.documentElement.style.setProperty("--accent-color", color);

        // 🎵 SONGS
        playlist = Array.isArray(data.songs) ? data.songs : [];
        currentIndex = 0;

        renderSongs();

        // 🔥 CRITICAL FIX (no refresh bug + always play first song)
        if (playlist.length > 0) {

            // wait for YouTube API + DOM render
            setTimeout(() => {
                if (ytReady) {
                    playSong(0);
                } else {
                    // retry if API not ready
                    let retry = setInterval(() => {
                        if (ytReady) {
                            clearInterval(retry);
                            playSong(0);
                        }
                    }, 300);
                }
            }, 300);

        } else {
            showNoSongs();
        }

        // 💬 MOOD MESSAGE
        const moodNote = moodMessages[finalEmotion] || "🎧 Enjoy your music";

        document.getElementById("emotion").innerHTML = `
            🎯 Mood: <b>${finalEmotion}</b><br>
            💬 ${moodNote}<br>
            <small style="opacity:0.7">
            ⚠️ Unavailable videos can't play due to YouTube restrictions. You can open them directly on YouTube.
            </small>
        `;

    } catch (err) {
        console.error("❌ ERROR:", err);
        showError();
    }

    document.getElementById("loader").classList.add("hidden");
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
        div.onclick = () => playSong(index, true); // 👈 user click

        div.innerHTML = `
            <img src="${song.thumbnail}" />
            <div>
                <h4>${song.name}</h4>
                <p>${song.artist}</p>
            </div>
        `;

        container.appendChild(div);
    });
}

// ===============================
// ▶ PLAYER
// ===============================
function createPlayer(videoId) {

    if (!player) {
        player = new YT.Player("videoPlayer", {
            height: "300",
            width: "100%",
            videoId: videoId,
            playerVars: {
                autoplay: 1,
                rel: 0
            },
            events: {

                onReady: (event) => {
                    event.target.playVideo();
                },

                onError: () => {

                    console.log("❌ Video unavailable");

                    if (userClicked) {
                        document.getElementById("emotion").innerHTML += `
                        <br><span style="color:#ffb3b3">
                        ⚠️ This video is unavailable. You can watch it on YouTube or wait...
                        </span>
                        `;

                        setTimeout(() => {
                            nextSong();
                        }, 5000);

                    } else {
                        // ⚡ AUTO PLAY → SKIP FAST
                        nextSong();
                    }
                }
            }
        });

    } else {
        player.loadVideoById(videoId);
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
    userClicked = isUserClick;  // 🔥 SET FLAG

    if (!ytReady) {
        setTimeout(() => playSong(index, isUserClick), 500);
        return;
    }

    createPlayer(song.videoId);
    highlightActive(index);
}
// ===============================
// ⏭ NEXT / PREV
// ===============================
function nextSong() {
    if (!playlist.length) return;

    currentIndex = (currentIndex + 1) % playlist.length;

    playSong(currentIndex, false); // 👈 auto play
}

function prevSong() {
    currentIndex = (currentIndex - 1 + playlist.length) % playlist.length;
    playSong(currentIndex);
}

// ===============================
// 🎯 HIGHLIGHT
// ===============================
function highlightActive(index) {
    document.querySelectorAll(".song-card").forEach((c, i) => {
        c.classList.toggle("active", i === index);
    });
}

// ===============================
// ⚠ UI STATES
// ===============================
function showNoSongs() {
    document.getElementById("songs").innerHTML =
        `<p style="color:white;">⚠ No songs found</p>`;
}

function showError() {
    document.getElementById("songs").innerHTML =
        `<p style="color:red;">❌ Error loading songs</p>`;
}