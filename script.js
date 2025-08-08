document.addEventListener("DOMContentLoaded", () => {
  const words = document.querySelectorAll(".word");
  const styleSelector = document.getElementById("styleSelector");
  const playAllBtn = document.getElementById("playAllBtn");
  const stopBtn = document.getElementById("stopBtn");

  let currentIndex = 0;
  let isPlaying = false;
  let currentAudio = null;

  function normalizeFileName(text) {
    return text
      .trim()
      .toLowerCase()
      .replace(/\s+/g, "_") // spazi → underscore
      .normalize("NFD") // separa lettere e accenti
      .replace(/[\u0300-\u036f]/g, ""); // rimuove accenti
  }

  function playWord(index) {
    if (!isPlaying || index >= words.length) return;

    const word = words[index];
    const style = styleSelector.value;
    const fileName = normalizeFileName(word.textContent);
    const audio = new Audio(`audio/${fileName}.mp3`);
    currentAudio = audio;

    console.log(`▶️ Riproduco: ${fileName}.mp3`);

    word.classList.add("pulse", style);

    audio.load();
    audio.play().then(() => {
      audio.addEventListener("ended", () => {
        word.classList.remove("pulse", style);
        setTimeout(() => playWord(index + 1), 300);
      });
    }).catch((error) => {
      console.warn(`⚠️ Errore nella riproduzione di "${word.textContent}":`, error);
      word.classList.remove("pulse", style);
      setTimeout(() => playWord(index + 1), 300);
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
    words.forEach(word => word.classList.remove("pulse", "glow", "shadow"));
  });
});