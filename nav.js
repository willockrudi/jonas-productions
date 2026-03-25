// Mobile nav toggle
const hamburger = document.querySelector('.hamburger');
const nav = document.querySelector('nav');
if (hamburger && nav) {
  hamburger.addEventListener('click', () => nav.classList.toggle('open'));
}

// Active nav link
const links = document.querySelectorAll('nav a');
const current = location.pathname.split('/').pop() || 'index.html';
links.forEach(a => {
  const href = a.getAttribute('href');
  if (href === current) a.classList.add('active');
});
