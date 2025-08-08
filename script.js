document.addEventListener("DOMContentLoaded", () => {
  const words = document.querySelectorAll(".word");
  const styleSelector = document.getElementById("styleSelector");
  const playAllBtn = document.getElementById("playAllBtn");
  const stopBtn = document.getElementById("stopBtn");
  const searchInput = document.getElementById("searchInput");
  const nowPlaying = document.getElementById("nowPlaying");

  let currentIndex = 0;
  let isPlaying = false;
  let currentAudio = null;

  function normalizeFileName(text) {
    return text
      .trim()
      .toLowerCase()
      .replace(/\s+/g, "_")
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function normalizeText(text) {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "")
      .replace(/\s+/g, "");
  }

  function checkAudioExists(fileName, callback) {
    fetch(`audio/${fileName}.mp3`, { method: "HEAD" })
      .then(response => callback(response.ok))
      .catch(() => callback(false));
  }

  function playWord(index) {
    if (!isPlaying || index >= words.length) return;

    const word = words[index];
    playSingleWord(word, () => playWord(index + 1));
  }

  function playSingleWord(word, onEndCallback = null) {
    const style = styleSelector.value;
    const fileName = normalizeFileName(word.textContent);
    const audioPath = `audio/${fileName}.mp3`;

    checkAudioExists(fileName, exists => {
      if (!exists) {
        console.warn(`❌ Audio mancante: ${audioPath}`);
        word.classList.add("missing");
        if (onEndCallback) setTimeout(onEndCallback, 300);
        return;
      }

      const audio = new Audio(audioPath);
      currentAudio = audio;

      console.log(`▶️ Riproduco: ${audioPath}`);
      nowPlaying.textContent = `🔊 ${word.textContent}`;

      word.classList.remove("pulse", "glow", "shadow", "neon", "rainbow", "missing");
      word.classList.add("pulse", style);

      audio.load();
      audio.play().then(() => {
        audio.addEventListener("ended", () => {
          word.classList.remove("pulse", style);
          nowPlaying.textContent = "";
          if (onEndCallback) setTimeout(onEndCallback, 300);
        });
      }).catch((error) => {
        console.warn(`⚠️ Errore nella riproduzione di "${word.textContent}":`, error);
        word.classList.remove("pulse", style);
        nowPlaying.textContent = "";
        if (onEndCallback) setTimeout(onEndCallback, 300);
      });
    });
  }

  playAllBtn.addEventListener("click", () => {
    if (isPlaying) return;
    isPlaying = true;
    currentIndex = 0;
    playWord(currentIndex);
  });

  stopBtn.addEventListener("click", () => {
    isPlaying = false;
    if (currentAudio) {
      currentAudio.pause();
      currentAudio.currentTime = 0;
    }
    nowPlaying.textContent = "";
    words.forEach(word => {
      word.classList.remove("pulse", "glow", "shadow", "neon", "rainbow", "missing");
      word.style.display = "inline-block";
    });
  });

  // 🔊 Riproduzione singola al clic
  words.forEach(word => {
    word.addEventListener("click", () => {
      if (isPlaying) return;
      playSingleWord(word);
    });
  });

  // 🔍 Ricerca intelligente con accenti rimossi
  searchInput.addEventListener("input", () => {
    const query = normalizeText(searchInput.value.trim());
    let found = false;

    words.forEach(word => {
      const wordText = normalizeText(word.textContent);
      const match = wordText.includes(query);
      word.style.display = match ? "inline-block" : "none";
      if (match) found = true;
    });

    nowPlaying.textContent = found ? "" : "❌ Nessuna parola trovata";
  });
});