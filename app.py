from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# CONFIGURAÇÕES - Depois você troca aqui no GitHub
VERIFY_TOKEN = "pizzaria123"
WHATSAPP_TOKEN = os.environ.get("WHATSAPP_TOKEN", "SEU_TOKEN_AQUI")
PHONE_NUMBER_ID = os.environ.get("PHONE_NUMBER_ID", "SEU_PHONE_NUMBER_ID_AQUI")

# Cardápio
CARDAPIO = """
🍕 *PIZZARIA GARAGEM* 🍕
Seja bem-vindo! Escolha uma opção:

1️⃣ - Ver Cardápio
2️⃣ - Fazer Pedido
3️⃣ - Falar com Atendente
4️⃣ - Endereço e Horário
"""

MENU_PIZZAS = """
🍕 *NOSSO CARDÁPIO*

*Tradicionais - R$ 39,90*
- Calabresa
- Marguerita
- Frango com Catupiry
- Portuguesa

*Especiais - R$ 49,90*
- Quatro Queijos
- Bacon com Cheddar
- Camarão
- Garagem (Especial da casa)

Digite o nome da pizza que você quer!
Ex: *Quero uma Calabresa*
"""

@app.route("/")
def home():
    return "Pizzaria Garagem - Robô Online! 🍕"

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Erro de verificação", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        if data.get("object") == "whatsapp_business_account":
            for entry in data.get("entry", []):
                for change in entry.get("changes", []):
                    value = change.get("value", {})
                    messages = value.get("messages", [])
                    for msg in messages:
                        from_number = msg.get("from")
                        text = msg.get("text", {}).get("body", "").lower()
                       
