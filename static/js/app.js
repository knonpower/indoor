const qs = (s, p=document) => p.querySelector(s);
const qsa = (s, p=document) => [...p.querySelectorAll(s)];

const year = qs("#year");
if (year) year.textContent = new Date().getFullYear();

const menuButton = qs("#menuButton");
const mobileNav = qs("#mobileNav");
if (menuButton && mobileNav) {
  menuButton.addEventListener("click", () => { const open = mobileNav.classList.toggle("open"); menuButton.setAttribute("aria-expanded", String(open)); menuButton.setAttribute("aria-label", open ? "Cerrar menú" : "Abrir menú"); });
  qsa("#mobileNav a").forEach(a => a.addEventListener("click", () => { mobileNav.classList.remove("open"); menuButton.setAttribute("aria-expanded", "false"); menuButton.setAttribute("aria-label", "Abrir menú"); }));
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") { mobileNav.classList.remove("open"); menuButton.setAttribute("aria-expanded", "false"); menuButton.setAttribute("aria-label", "Abrir menú"); } });
}

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add("visible");
      observer.unobserve(entry.target);
    }
  });
}, {threshold: .08});
qsa(".reveal").forEach(el => observer.observe(el));

const tempSlider = qs("#tempSlider");
const tempValue = qs("#tempValue");
const extractorState = qs("#extractorState");
const fanState = qs("#fanState");
const heaterState = qs("#heaterState");

function updateSimulator(){
  if (!tempSlider || !tempValue || !extractorState || !fanState || !heaterState) return;
  const value = Number(tempSlider.value);
  tempValue.textContent = `${value} °C`;
  extractorState.textContent = value >= 27 ? "ON" : "OFF";
  fanState.textContent = value >= 25 ? "ON" : "OFF";
  heaterState.textContent = value <= 20 ? "ON" : "OFF";
  [extractorState, fanState, heaterState].forEach(el => {
    el.style.color = el.textContent === "ON" ? "var(--green)" : "#6f8985";
  });
}
if (tempSlider) tempSlider.addEventListener("input", updateSimulator);
updateSimulator();
