document.addEventListener("DOMContentLoaded", () => {
  const cards = Array.from(document.querySelectorAll(".workout-card"));
  const sortSelect = document.getElementById("sortWorkouts");
  const grid = document.querySelector(".workout-grid");

  // Toggle workout details
  cards.forEach(card => {
    card.addEventListener("click", () => {
      const details = card.querySelector(".workout-details");
      const icon = card.querySelector(".bi");

      const isActive = details.classList.contains("active");
      document.querySelectorAll(".workout-details").forEach(d => d.classList.remove("active"));
      document.querySelectorAll(".bi").forEach(i => {
        i.classList.remove("bi-chevron-up");
        i.classList.add("bi-chevron-down");
      });

      if (!isActive) {
        details.classList.add("active");
        icon.classList.remove("bi-chevron-down");
        icon.classList.add("bi-chevron-up");
      }
    });
  });

  // Function to sort cards
  const sortCards = (order) => {
    const sorted = cards.slice().sort((a, b) => {
      const dateA = new Date(a.dataset.date);
      const dateB = new Date(b.dataset.date);
      return order === "newest" ? dateB - dateA : dateA - dateB;
    });
    grid.innerHTML = "";
    sorted.forEach(card => grid.appendChild(card));
  };

  // Sort by default to newest first
  sortCards("newest");
  sortSelect.value = "newest"; // optional: set select to match default

  // Sort on change
  sortSelect.addEventListener("change", () => {
    sortCards(sortSelect.value);
  });
});
