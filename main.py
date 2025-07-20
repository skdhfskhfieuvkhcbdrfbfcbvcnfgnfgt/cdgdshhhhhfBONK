import requests
from nacl.signing import SigningKey
import base58
import threading
import time
import random
import logging
from flask import Flask

# Flask Keep Alive
app = Flask(__name__)

@app.route('/')
def home():
    return "🟢 I am alive"

def run_flask():
    try:
        app.run(host='0.0.0.0', port=8085)
    except Exception as e:
        logging.error(f"Error in Flask server: {e}")

def keep_alive():
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()

# Bot Configuration
BOT_TOKEN = "7816959898:AAG1IKGYIC1GYyB32Whz9qH9J1YtXANwZwY"
CHAT_ID = "-1002899014663"
messages_todo = 3

def send_message(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg,
        "parse_mode": "Markdown"
    }
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def her_ily_message():
    try:
        with open("comments.txt", "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
        return random.choice(lines) if lines else None
    except FileNotFoundError:
        return None

def c_check(mint, target_message):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0'
    }
    response = requests.get(f'https://gated.chat/comment/get/{mint}', headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            messages = [entry["message"].strip() for entry in data if "message" in entry]
            return target_message.strip() in messages
        except:
            return False
    return False

def get_latest_mints():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'user-agent': 'Mozilla/5.0'
    }
    response = requests.get(
        'https://launch-mint-v1.raydium.io/get/list?platformId=FfYek5vEz23cMkWsdJwG2oa6EphsvXSHrGpdALN4g6W1,BuM6KDpWiTcxvrpXywWFiw45R2RNH8WURdvqoTDV1BW4&sort=new&size=100&&mintType=default&includeNsfw=false',
        headers=headers,
    )
    data = response.json()
    if data.get("success"):
        mints = [item["mint"] for item in data.get("data", {}).get("rows", [])]
        for mint in mints:
            caller(mint)

def caller(mint):
    try:
        with open("done.txt", "r") as f:
            done_mints = set(line.strip() for line in f)
    except FileNotFoundError:
        done_mints = set()
    if mint not in done_mints:
        message_text = her_ily_message()
        def thread_func():
            try:
                bonk_flow(message_text, f"{mint}")
            except:
                pass
        threads = []
        for _ in range(messages_todo):
            t = threading.Thread(target=thread_func)
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        with open("done.txt", "a") as ayushi:
            ayushi.write(f"{mint}\n")

def bonk_flow(message, mint):
    def assign_me_daddy(auth_token):
        headers = {
            'authorization': f'{auth_token}',
            'content-type': 'application/json',
            'user-agent': user_agent,
        }
        json_data = {
            'name': 'Best Solana Tools',
            'bio': 'Hello, welcome to my profile!',
        }
        requests.post('https://gated.chat/user/assign', headers=headers, json=json_data)

    def post_comment(auth, comment, mint):
        headers = {
            'authorization': f'{auth}',
            'content-type': 'application/json',
            'user-agent': user_agent,
        }
        json_data = {
            'comment': comment,
            'tokenMint': mint,
        }
        requests.post('https://gated.chat/comment/post', headers=headers, json=json_data)

    signing_key = SigningKey.generate()
    verify_key = signing_key.verify_key
    wallet_address = base58.b58encode(verify_key.encode()).decode()
    user_agent = 'Mozilla/5.0'

    challenge_url = f'https://api.letsbonk.fun/auth/challenge/{wallet_address}'
    challenge_response = requests.get(challenge_url, headers={'user-agent': user_agent})
    if challenge_response.status_code != 200:
        return

    challenge = challenge_response.json()['challenge']
    signed = signing_key.sign(challenge.encode())
    signature = base58.b58encode(signed.signature).decode()

    json_data = {
        'walletAddress': wallet_address,
        'signature': signature,
    }
    verify_response = requests.post(
        'https://api.letsbonk.fun/auth/verify',
        headers={'user-agent': user_agent, 'content-type': 'application/json'},
        json=json_data
    )
    auth_token = verify_response.json().get("jwt")
    if not auth_token:
        return

    assign_me_daddy(auth_token)
    post_comment(auth_token, message, mint)

# Main Loop
def main():
    keep_alive()
    while True:
        try:
            get_latest_mints()
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
