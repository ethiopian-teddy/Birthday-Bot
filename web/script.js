const config = window.LOVE_COUNTDOWN_CONFIG;
const birthday = new Date(config.birthdayIso);

document.getElementById("title").textContent = `For ${config.girlfriendName}`;
document.getElementById("subtitle").textContent =
  `From ${config.boyfriendName}, with every second carrying a little more love.`;

const pad = (value) => String(value).padStart(2, "0");

function updateCountdown() {
  const diff = Math.max(0, birthday.getTime() - Date.now());
  const days = Math.floor(diff / 86_400_000);
  const hours = Math.floor((diff % 86_400_000) / 3_600_000);
  const minutes = Math.floor((diff % 3_600_000) / 60_000);
  const seconds = Math.floor((diff % 60_000) / 1_000);

  document.getElementById("days").textContent = days;
  document.getElementById("hours").textContent = pad(hours);
  document.getElementById("minutes").textContent = pad(minutes);
  document.getElementById("seconds").textContent = pad(seconds);
}

function renderNotes() {
  const notes = document.getElementById("notes");
  notes.replaceChildren(...config.notes.map((text) => {
    const article = document.createElement("article");
    article.className = "note";
    article.textContent = text;
    return article;
  }));
}

function renderGallery() {
  const gallery = document.getElementById("gallery");
  gallery.replaceChildren(...config.gallery.map((src, index) => {
    const image = document.createElement("img");
    image.src = src;
    image.alt = `Memory ${index + 1}`;
    return image;
  }));
}

function renderMusic() {
  const link = document.getElementById("musicLink");
  if (!config.musicUrl) {
    link.hidden = true;
    return;
  }
  link.href = config.musicUrl;
}

function createHearts() {
  const layer = document.querySelector(".hearts");
  for (let index = 0; index < 26; index += 1) {
    const heart = document.createElement("span");
    heart.className = "heart";
    heart.style.left = `${Math.random() * 100}%`;
    heart.style.bottom = `${Math.random() * 70}%`;
    heart.style.animationDuration = `${8 + Math.random() * 9}s`;
    heart.style.animationDelay = `${Math.random() * 8}s`;
    layer.appendChild(heart);
  }
}

updateCountdown();
renderNotes();
renderGallery();
renderMusic();
createHearts();
setInterval(updateCountdown, 1000);
