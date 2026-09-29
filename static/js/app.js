const qs = (s, p=document) => p.querySelector(s);
const qsa = (s, p=document) => [...p.querySelectorAll(s)];

const year = qs("#year");
if (year) year.textContent = new Date().getFullYear();

const menuButton = qs("#menuButton");
const mobileNav = qs("#mobileNav");
if (menuButton && mobileNav) {
  menuButton.addEventListener("click", () => mobileNav.classList.toggle("open"));
  qsa("#mobileNav a").forEach(a => a.addEventListener("click", () => mobileNav.classList.remove("open")));
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
