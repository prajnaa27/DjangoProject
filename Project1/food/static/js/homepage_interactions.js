const highlight = document.getElementById('highlight-section');
  const explore = document.getElementById('explore-section');

  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.target.id === 'highlight-section' && entry.isIntersecting) {
        highlight.classList.add('active');
      }
      if (entry.target.id === 'explore-section' && entry.isIntersecting) {
        explore.classList.add('active');
      }
    });
  }, { threshold: 0.4 });

  observer.observe(highlight);
  observer.observe(explore);