<script>
  document.addEventListener("DOMContentLoaded", () => {
    const audio = document.getElementById("introAudio");

    if (!audio) {
      console.warn("Elemento audio non trovato");
      return;
    }

    // Prova a riprodurre l'audio
    audio.muted = false;
    audio.volume = 1.0;

    audio.play().catch(() => {
      console.log("Autoplay bloccato dal browser");
    });

    // Funzione dissolvenza
    function fadeOutAudio() {
      const fadeInterval = setInterval(() => {
        if (audio.volume > 0.01) {
          audio.volume = Math.max(0, audio.volume - 0.01);
        } else {
          audio.pause();
          clearInterval(fadeInterval);
        }
      }, 50);
    }

    // Gestione interazione utente
    function handleUserInteraction() {
      fadeOutAudio();
      window.removeEventListener("keydown", handleUserInteraction);
      window.removeEventListener("click", handleUserInteraction);
      window.removeEventListener("touchstart", handleUserInteraction);
    }

    // Ascolta input utente
    window.addEventListener("keydown", handleUserInteraction);
    window.addEventListener("click", handleUserInteraction);
    window.addEventListener("touchstart", handleUserInteraction);
  });
</script>