from flask import Flask, request
import os

app = Flask(__name__)
VERIFY_TOKEN = "pizzaria123"

MENU = """
Pizzaria Garagem - Cardapio:
- Calabresa
- Frango com Catupiry
- Bacon com Cheddar
- Camarao
- Garagem (Especial da casa)

Digite o nome da pizza que voce quer!
Ex: Quero uma Calabresa
"""

@app.route("/")
def inicio():
    return "Pizzaria Garagem - Robo Online! 🍕"

@app.route("/webhook", methods=["GET"])
def verificar():
    modo = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    desafio = request.args.get("hub.challenge")
    if modo == "subscribe" and token == VERIFY_TOKEN:
        return desafio, 200
    return "Erro de verificacao", 403

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.get_json()
    try:
        if dados.get("object") == "whatsapp_business_account":
            for entrada in dados.get("entry", []):
                for alterar in entrada.get("changes", []):
                    valor = alterar.get("value", {})
                    mensagens = valor.get("messages", [])
                    for msg in mensagens:
                        from_number = msg.get("from")
                        texto = msg.get("text", {}).get("body", "")
                        print(f"Mensagem de {from_number}: {texto}")
    except Exception as e:
        print(f"Erro: {e}")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
