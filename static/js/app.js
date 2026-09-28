const qs = (s, p=document) => p.querySelector(s);
const qsa = (s, p=document) => [...p.querySelectorAll(s)];

qs("#year").textContent = new Date().getFullYear();

const menuButton = qs("#menuButton");
const mobileNav = qs("#mobileNav");
menuButton.addEventListener("click", () => mobileNav.classList.toggle("open"));
qsa("#mobileNav a").forEach(a => a.addEventListener("click", () => mobileNav.classList.remove("open")));

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
  const value = Number(tempSlider.value);
  tempValue.textContent = `${value} °C`;
  extractorState.textContent = value >= 27 ? "ON" : "OFF";
  fanState.textContent = value >= 25 ? "ON" : "OFF";
  heaterState.textContent = value <= 20 ? "ON" : "OFF";
  [extractorState, fanState, heaterState].forEach(el => {
    el.style.color = el.textContent === "ON" ? "var(--green)" : "#6f8985";
  });
}
tempSlider.addEventListener("input", updateSimulator);
updateSimulator();

const chatLauncher = qs("#chatLauncher");
const chatWindow = qs("#chatWindow");
const chatClose = qs("#chatClose");
const chatForm = qs("#chatForm");
const chatInput = qs("#chatInput");
const chatMessages = qs("#chatMessages");
const sendButton = qs("#sendButton");
const quickPrompts = qs("#quickPrompts");
let history = [];

function openChat(){
  chatWindow.classList.add("open");
  chatWindow.setAttribute("aria-hidden", "false");
  setTimeout(() => chatInput.focus(), 160);
}
function closeChat(){
  chatWindow.classList.remove("open");
  chatWindow.setAttribute("aria-hidden", "true");
}
chatLauncher.addEventListener("click", openChat);
chatClose.addEventListener("click", closeChat);
qsa("[data-open-chat]").forEach(btn => btn.addEventListener("click", openChat));

function escapeHTML(str){
  return str.replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#039;'}[c]));
}
function addMessage(role, text, extraClass=""){
  const row = document.createElement("div");
  row.className = `message ${role} ${extraClass}`.trim();
  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = `<p>${escapeHTML(text)}</p>`;
  row.appendChild(bubble);
  chatMessages.appendChild(row);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return row;
}
function setLoading(loading){
  sendButton.disabled = loading;
  chatInput.disabled = loading;
}
async function sendChat(text){
  const clean = text.trim();
  if(!clean) return;
  if(quickPrompts) quickPrompts.style.display = "none";
  addMessage("user", clean);
  history.push({role:"user", content:clean});
  chatInput.value = "";
  autoSize();
  setLoading(true);
  const typing = addMessage("assistant", "Box IA está escribiendo…", "typing");
  try{
    const res = await fetch("/api/chat", {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({messages:history.slice(-12)})
    });
    const data = await res.json().catch(() => ({}));
    typing.remove();
    if(!res.ok) throw new Error(data.error || "No fue posible conectar con el asistente.");
    const answer = (data.reply || "No recibí una respuesta. Intenta nuevamente.").trim();
    addMessage("assistant", answer);
    history.push({role:"assistant", content:answer});
  }catch(err){
    typing.remove();
    addMessage("assistant", err.message || "Ocurrió un problema al conectar con Box IA.");
  }finally{
    setLoading(false);
    chatInput.focus();
  }
}
chatForm.addEventListener("submit", e => {
  e.preventDefault();
  sendChat(chatInput.value);
});
qsa(".quick-prompts button").forEach(btn => btn.addEventListener("click", () => sendChat(btn.textContent)));
function autoSize(){
  chatInput.style.height = "auto";
  chatInput.style.height = Math.min(chatInput.scrollHeight, 110) + "px";
}
chatInput.addEventListener("input", autoSize);
chatInput.addEventListener("keydown", e => {
  if(e.key === "Enter" && !e.shiftKey){
    e.preventDefault();
    chatForm.requestSubmit();
  }
});
