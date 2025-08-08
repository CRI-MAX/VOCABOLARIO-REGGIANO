fetch('vocabolario.json')
  .then(response => response.json())
  .then(data => {
    const searchInput = document.getElementById('search');
    const resultsList = document.getElementById('results');

    searchInput.addEventListener('input', () => {
      const query = searchInput.value.toLowerCase();
      resultsList.innerHTML = '';

      const filtered = data.filter(entry =>
        entry.italiano.toLowerCase().includes(query) ||
        entry.dialetto.toLowerCase().includes(query)
      );

      filtered.forEach(entry => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${entry.italiano}</strong> → ${entry.dialetto}
          <button onclick="new Audio('${entry.audio}').play()">🔊</button>`;
        resultsList.appendChild(li);
      });
    });
  });