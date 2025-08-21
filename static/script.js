const audio = document.getElementById("introAudio");

// Imposta volume iniziale
audio.volume = 1.0;

// Funzione dissolvenza
function fadeOutAudio() {
  let volume = audio.volume;
  const fadeInterval = setInterval(() => {
    if (volume > 0.01) {
      volume -= 0.01;
      audio.volume = volume;
    } else {
      audio.pause();
      clearInterval(fadeInterval);
    }
  }, 50);
}

// Attiva dissolvenza al primo input
function handleUserInteraction() {
  fadeOutAudio();
  window.removeEventListener("keydown", handleUserInteraction);
  window.removeEventListener("click", handleUserInteraction);
  window.removeEventListener("touchstart", handleUserInteraction);
}

// Ascolta tasto, click o touch
window.addEventListener("keydown", handleUserInteraction);
window.addEventListener("click", handleUserInteraction);
window.addEventListener("touchstart", handleUserInteraction);