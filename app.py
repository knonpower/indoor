import os
import time
from collections import defaultdict, deque
from threading import Lock

from flask import Flask, jsonify, render_template, request
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = Flask(__name__)

MODEL = os.getenv("OPENAI_MODEL", "gpt-5.6-luna")
API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
client = OpenAI(api_key=API_KEY) if API_KEY else None

RATE_LIMIT_MESSAGES = 20
RATE_LIMIT_WINDOW_SECONDS = 600
_requests_by_ip = defaultdict(deque)
_rate_lock = Lock()

SYSTEM_INSTRUCTIONS = """
Eres Box IA, el asistente informativo del sitio web de Super Magic Box.

Tu función es ayudar a visitantes a entender el producto, no inventar especificaciones.
Responde en español claro, breve y profesional.

Información confirmada para utilizar:
- Super Magic Box es una plataforma de control ambiental para instalaciones de cultivo indoor.
- Centraliza lectura de sensores y control de equipos.
- Puede supervisar temperatura y humedad en más de un punto.
- Puede controlar iluminación, ventilador, extractor, humidificador y calefactor.
- La arquitectura contempla control local y comunicación industrial RS485 / Modbus RTU.
- La regulación de iluminación puede integrarse mediante señal 0-10 V cuando el hardware compatible está instalado.
- El software puede trabajar con planes y etapas, por ejemplo germinación, vegetación, floración y secado.
- El proyecto puede escalar desde instalaciones compactas a configuraciones de mayor tamaño, pero la configuración exacta depende de cada instalación.

Reglas:
1. No inventes precios, disponibilidad, certificaciones, ahorros energéticos garantizados, plazos de entrega ni compatibilidades que no estén confirmadas.
2. Si una pregunta requiere una especificación comercial o técnica no indicada arriba, dilo claramente y sugiere solicitar evaluación del proyecto.
3. No prometas resultados biológicos, producción, potencia, calidad, rendimiento ni concentraciones de compuestos.
4. Puedes explicar las funciones de automatización y control ambiental de manera general.
5. No pidas claves, contraseñas ni datos sensibles.
6. Si el visitante quiere cotización o instalación, indícale que use la sección "Solicitar información" del sitio.
7. Mantén las respuestas normalmente entre 2 y 6 frases, salvo que el usuario pida más detalle.
""".strip()


def is_rate_limited(ip: str) -> bool:
    now = time.time()
    with _rate_lock:
        q = _requests_by_ip[ip]
        while q and now - q[0] > RATE_LIMIT_WINDOW_SECONDS:
            q.popleft()
        if len(q) >= RATE_LIMIT_MESSAGES:
            return True
        q.append(now)
        return False


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/health")
def health():
    return {"ok": True, "ai_configured": bool(API_KEY), "model": MODEL}


@app.post("/api/chat")
def chat():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr or "unknown").split(",")[0].strip()
    if is_rate_limited(ip):
        return jsonify(error="Has enviado varias consultas seguidas. Espera unos minutos antes de continuar."), 429

    if client is None:
        return jsonify(
            error="Box IA todavía no está conectado. El administrador debe configurar OPENAI_API_KEY en el servidor."
        ), 503

    data = request.get_json(silent=True) or {}
    messages = data.get("messages", [])
    if not isinstance(messages, list) or not messages:
        return jsonify(error="No se recibió un mensaje válido."), 400

    cleaned = []
    for item in messages[-12:]:
        if not isinstance(item, dict):
            continue
        role = item.get("role")
        content = item.get("content")
        if role not in ("user", "assistant") or not isinstance(content, str):
            continue
        content = content.strip()[:1200]
        if content:
            cleaned.append({"role": role, "content": content})

    if not cleaned or cleaned[-1]["role"] != "user":
        return jsonify(error="La conversación no contiene una pregunta válida."), 400

    try:
        response = client.responses.create(
            model=MODEL,
            instructions=SYSTEM_INSTRUCTIONS,
            input=cleaned,
            max_output_tokens=500,
        )
        reply = (response.output_text or "").strip()
        if not reply:
            reply = "No pude generar una respuesta en este momento. Intenta nuevamente."
        return jsonify(reply=reply)
    except Exception:
        app.logger.exception("Error al consultar OpenAI")
        return jsonify(error="No fue posible obtener una respuesta de Box IA en este momento."), 502


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=os.getenv("FLASK_DEBUG") == "1")
