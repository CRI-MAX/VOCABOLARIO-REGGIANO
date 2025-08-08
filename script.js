document.addEventListener('DOMContentLoaded', () => {
  const data = [
    {
      "italiano": "abbastanza",
      "dialetto": "abâsta",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/abasta.mp3"
    },
    {
      "italiano": "dietro",
      "dialetto": "adrē",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/adree.mp3"
    },
    {
      "italiano": "adesso",
      "dialetto": "adès",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/ades.mp3"
    },
    {
      "italiano": "acqua",
      "dialetto": "acua",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/acua.mp3"
    },
    {
      "italiano": "aglio",
      "dialetto": "aj",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/aj.mp3"
    },
    {
      "italiano": "alto",
      "dialetto": "alt",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/alt.mp3"
    },
    {
      "italiano": "amaro",
      "dialetto": "amèr",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/amer.mp3"
    },
    {
      "italiano": "amico",
      "dialetto": "amîgh",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/amigh.mp3"
    },
    {
      "italiano": "andare",
      "dialetto": "andar",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/andar.mp3"
    },
    {
      "italiano": "anello",
      "dialetto": "anèl",
      "audio": "https://lenguamedra.it/wp-content/uploads/2022/08/anel.mp3"
    }
  ];

  const searchInput = document.getElementById('searchInput');
  const resultsContainer = document.getElementById('results');
  const playAllBtn = document.getElementById('playAllBtn');

  function renderResults(filtered) {
    resultsContainer.innerHTML = '';

    if (filtered.length === 0) {
      resultsContainer.innerHTML = '<p>Nessun risultato trovato.</p>';
      return;
    }

    filtered.forEach(item => {
      const entry = document.createElement('div');
      entry.classList.add('entry');

      const italiano = document.createElement('h3');
      italiano.textContent = item.italiano;

      const dialetto = document.createElement('p');
      dialetto.textContent = `Dialetto: ${item.dialetto}`;

      const audio = document.createElement('audio');
      audio.controls = true;
      audio.src = item.audio;

      entry.appendChild(italiano);
      entry.appendChild(dialetto);
      entry.appendChild(audio);

      resultsContainer.appendChild(entry);
    });
  }

  searchInput.addEventListener('input', () => {
    const query = searchInput.value.toLowerCase();
    const filtered = data.filter(item =>
      item.italiano.toLowerCase().includes(query)
    );
    renderResults(filtered);
  });

  playAllBtn.addEventListener('click', () => {
    const query = searchInput.value.toLowerCase();
    const filtered = data.filter(item =>
      item.italiano.toLowerCase().includes(query)
    );

    if (filtered.length === 0) {
      alert('Nessuna parola da riprodurre.');
      return;
    }

    let index = 0;
    const audio = new Audio();

    const playNext = () => {
      if (index >= filtered.length) return;
      audio.src = filtered[index].audio;
      audio.play();
      index++;
    };

    audio.addEventListener('ended', playNext);
    playNext();
  });

  // Render iniziale (tutte le parole)
  renderResults(data);
});