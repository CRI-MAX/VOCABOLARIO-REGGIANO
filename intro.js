<script>
  document.addEventListener("DOMContentLoaded", () => {
    const audio = new Audio("/static/audio/intro.mp3");
    audio.volume = 0.5;

    // Prova autoplay immediato (funziona su desktop)
    audio.play().catch(() => {
      // Se fallisce (mobile), aspetta interazione utente
      const enableAudio = () => {
        audio.play().catch(() => {});
        document.removeEventListener("click", enableAudio);
        document.removeEventListener("touchstart", enableAudio);
      };

      document.addEventListener("click", enableAudio);
      document.addEventListener("touchstart", enableAudio);
    });
  });
</script>