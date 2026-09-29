import os
from urllib.parse import quote

from flask import Flask, render_template

app = Flask(__name__)


def obtener_whatsapp_url():
    numero = os.getenv("WHATSAPP_NUMBER", "").strip()
    numero = "".join(c for c in numero if c.isdigit())

    if not numero:
        return ""

    mensaje = (
        "Hola, vi Super Magic Box en supermagicbox.cl y quiero más información "
        "sobre el sistema."
    )
    return f"https://wa.me/{numero}?text={quote(mensaje)}"


@app.get("/")
def home():
    return render_template("index.html", whatsapp_url=obtener_whatsapp_url())


@app.get("/health")
def health():
    return {
        "ok": True,
        "whatsapp_configured": bool(obtener_whatsapp_url()),
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.getenv("FLASK_DEBUG") == "1",
    )
