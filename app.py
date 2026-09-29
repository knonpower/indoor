import hashlib
import hmac
import os
from urllib.parse import quote

import requests
from flask import Flask, Response, jsonify, render_template, request

app = Flask(__name__)

WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "").strip()
WHATSAPP_VERIFY_TOKEN = os.getenv("WHATSAPP_VERIFY_TOKEN", "").strip()
WHATSAPP_ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN", "").strip()
WHATSAPP_PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID", "").strip()
META_APP_SECRET = os.getenv("META_APP_SECRET", "").strip()
WHATSAPP_GRAPH_VERSION = os.getenv("WHATSAPP_GRAPH_VERSION", "v26.0").strip()


def obtener_whatsapp_url():
    numero = "".join(c for c in WHATSAPP_NUMBER if c.isdigit())
    if not numero:
        return ""

    mensaje = (
        "Hola, vi Super Magic Box en supermagicbox.cl y quiero más información "
        "sobre el sistema."
    )
    return f"https://wa.me/{numero}?text={quote(mensaje)}"


def whatsapp_cloud_configurado():
    return bool(
        WHATSAPP_VERIFY_TOKEN
        and WHATSAPP_ACCESS_TOKEN
        and WHATSAPP_PHONE_NUMBER_ID
    )


def verificar_firma_webhook(raw_body: bytes, signature_header: str) -> bool:
    if not META_APP_SECRET:
        return True
    if not signature_header or not signature_header.startswith("sha256="):
        return False

    firma_recibida = signature_header.split("=", 1)[1]
    firma_calculada = hmac.new(
        META_APP_SECRET.encode("utf-8"),
        raw_body,
        hashlib.sha256,
    ).hexdigest()
    return hmac.compare_digest(firma_calculada, firma_recibida)


def respuesta_automatica(texto: str) -> str:
    texto = (texto or "").strip().lower()

    if not texto:
        return (
            "Hola. Soy el asistente automático de Super Magic Box.\n\n"
            "Escribe una opción:\n"
            "1. ¿Qué es Super Magic Box?\n"
            "2. Cotización\n"
            "3. Instalación\n"
            "4. Tecnología\n"
            "5. Hablar con una persona"
        )

    if texto in {"hola", "buenas", "buenos dias", "buenos días", "buenas tardes", "menu", "menú"}:
        return respuesta_automatica("")

    if texto == "1" or "que es" in texto or "qué es" in texto or "que hace" in texto or "qué hace" in texto:
        return (
            "Super Magic Box es una plataforma de control ambiental para cultivo indoor. "
            "Centraliza sensores y controla equipos como iluminación, extractor, ventilador, "
            "humidificador y calefactor desde una sola lógica de automatización."
        )

    if texto == "2" or "precio" in texto or "cotiz" in texto:
        return (
            "La configuración y el valor dependen de cada instalación. "
            "Para evaluar tu proyecto, envíanos las dimensiones del espacio, cantidad de luminarias "
            "y los equipos que quieres controlar. Un integrante del equipo puede continuar la cotización."
        )

    if texto == "3" or "instal" in texto:
        return (
            "Super Magic Box puede instalarse en proyectos compactos o de mayor tamaño. "
            "La configuración depende de sensores, iluminación y equipos conectados. "
            "Cuéntanos las dimensiones de tu instalación y qué equipos utilizas."
        )

    if texto == "4" or "tecnolog" in texto or "modbus" in texto or "rs485" in texto:
        return (
            "La arquitectura de Super Magic Box utiliza procesamiento local, sensores digitales, "
            "comunicación RS485 / Modbus RTU y puede integrar control de iluminación 0–10 V "
            "cuando el hardware compatible está instalado."
        )

    if texto == "5" or "asesor" in texto or "humano" in texto or "persona" in texto:
        return (
            "Perfecto. Escribe tu nombre y un resumen de lo que necesitas. "
            "La consulta quedará en este canal para continuar la atención de forma personal."
        )

    return (
        "Puedo ayudarte con información general de Super Magic Box.\n\n"
        "Escribe una opción:\n"
        "1. Qué es Super Magic Box\n"
        "2. Cotización\n"
        "3. Instalación\n"
        "4. Tecnología\n"
        "5. Hablar con una persona"
    )


def enviar_mensaje_whatsapp(destino: str, texto: str) -> bool:
    if not whatsapp_cloud_configurado():
        app.logger.warning("WhatsApp Cloud API aún no está completamente configurada.")
        return False

    url = (
        f"https://graph.facebook.com/{WHATSAPP_GRAPH_VERSION}/"
        f"{WHATSAPP_PHONE_NUMBER_ID}/messages"
    )
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": destino,
        "type": "text",
        "text": {"body": texto},
    }

    response = requests.post(url, headers=headers, json=payload, timeout=15)
    if not response.ok:
        app.logger.error(
            "Error al enviar mensaje por WhatsApp Cloud API: %s %s",
            response.status_code,
            response.text[:500],
        )
        return False
    return True


def extraer_mensajes(payload: dict):
    mensajes = []
    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            for message in value.get("messages", []) or []:
                if message.get("type") != "text":
                    continue
                origen = message.get("from")
                texto = (message.get("text") or {}).get("body", "")
                if origen and texto:
                    mensajes.append((origen, texto))
    return mensajes


@app.get("/")
def home():
    return render_template("index.html", whatsapp_url=obtener_whatsapp_url())


@app.get("/health")
def health():
    return {
        "ok": True,
        "whatsapp_button_configured": bool(obtener_whatsapp_url()),
        "whatsapp_cloud_configured": whatsapp_cloud_configurado(),
        "signature_validation_enabled": bool(META_APP_SECRET),
        "graph_version": WHATSAPP_GRAPH_VERSION,
    }


@app.get("/webhooks/whatsapp")
def verificar_whatsapp():
    mode = request.args.get("hub.mode", "")
    verify_token = request.args.get("hub.verify_token", "")
    challenge = request.args.get("hub.challenge", "")

    if mode == "subscribe" and verify_token == WHATSAPP_VERIFY_TOKEN:
        return Response(challenge, status=200, mimetype="text/plain")
    return Response("Forbidden", status=403, mimetype="text/plain")


@app.post("/webhooks/whatsapp")
def recibir_whatsapp():
    raw_body = request.get_data(cache=True)
    signature = request.headers.get("X-Hub-Signature-256", "")

    if not verificar_firma_webhook(raw_body, signature):
        return jsonify(error="Firma inválida"), 403

    payload = request.get_json(silent=True) or {}

    for origen, texto in extraer_mensajes(payload):
        enviar_mensaje_whatsapp(origen, respuesta_automatica(texto))

    return jsonify(ok=True)


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.getenv("FLASK_DEBUG") == "1",
    )
