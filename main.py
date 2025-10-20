#!/usr/bin/env python3
import time
import threading
import random

calm_messages = [
    "🧘 Hengitä syvään, kaikki on hyvin... ❤️",
    "🌿 Rauhoitu hetkeksi, kaikki järjestyy...",
    "☕ Hengitä syvään, ei hätä ole tämän näköinen...",
    "🌸 Ei paniikkia, katsotaas...",
    "🕊️ No panic, kyllä tästä selvitään...",
    "🌈 Pieni tauko tekee ihmeitä...",
    "💫 Venttaas hetki, mietin hetken...",
    "🌼 Hei, mä tiiän tän! Eiku hmmm...",
    "🍃 Rauhotu saatana, se on vaa tietokone...",
    "🛋️ Ota pieni hengähdystauko, kyl se siitä...",
    "🌙 Maltti on valttia, hetkinen vain...",
    "👀 Lepuuta hetki silmiäsi. Mietin...",
    "☕ Oota mä juon ensin kahvini loppuun...",
    "🍺 Ota olut ja rentoudu...",
    "🍵 Ota tee ja rauhoitu...",
    "🍫 Tilanne vaatii suklaata...",
    "🧦 Vedä villasukat jalkaan, mulla menee hetki...",
    "🦉 Viisas pöllökin miettii rauhassa...",
    "🦔 Siili ei kiirehdi, eikä sunkaan tarvi...",
    "🧃 Ota mehu ja chillaa...",
    "🧀 Juusto ei sula stressistä, älä sinäkään...",
    "🧊 Yritetään pitää pää kylmänä...",
    "💻 Take it iisi in the tietokonekriisi...",
    "🪖 Ei tilanne ole koskaan paha...",
    "🪑 Pitääpä istua ihan alas miettimään...",
    "🐢 Hitaasti hyvä tulee... tai ainakin jotain tulee.",
    "🔥 Ei hätää, ei vielä savua.",
    "🎩 Taikatemppu latautuu... tai virheviesti.",
    "🧙 Koodi on taikuutta, ja mä oon just selaamassa loitsukirjaa.",
    "🥶 Älä jäädy, mä selvitän tän.",
    "🍕 Pizza auttaa kaikkeen, mutta kokeillaan tätä ensin...",
    "🛠️  Työstän ratkaisua...",
    "🔍 Etsin ratkaisua...",
    "👁️  Hallusinoidaan vastausta...",
    "💸 Aika on rahaa, ja tämä sovellus on ilmainen...",
    "💡 Hitto mites tää nyt menikään...",
    "🤖 Analysoin, lasken, arvaan... siinä järjestyksessä.",
    "📚 Konsultoin pyhiä dokumentaatioita...",
    "🔮 Näen tulevaisuuden, jossa kaikki toimii...",
    "🧴 Sivelin vähän kärsivällisyysvoidetta, jatketaan...",
]
message = random.choice(calm_messages)
spinner = ['🕛', '🕐', '🕑', '🕒', '🕓', '🕔', '🕕', '🕖', '🕗', '🕘', '🕙', '🕚']


def spinner_func(stop_event):
    import sys
    spin_idx = 0
    bar_length = 16
    bar_symbols = ['░', '▒', '▓', '█']
    phase = 0
    progress = 0
    # Animate message one character at a time
    animated_message = ''
    msg_idx = 0
    msg_done = False
    while not stop_event.is_set():
        if not msg_done:
            if msg_idx < len(message):
                animated_message += message[msg_idx]
                msg_idx += 1
            else:
                msg_done = True
            display_message = animated_message
            print(f"\r{display_message}", end="")
            sys.stdout.flush()
            time.sleep(0.07)
            continue
        else:
            display_message = message
        if progress >= bar_length:
            progress = 0
            phase = (phase + 1) % 4
        filled_symbol = bar_symbols[(phase + 1) % 4]
        bar = filled_symbol * (progress)
        empty_symbol = bar_symbols[phase]
        bar = bar + empty_symbol * (bar_length - progress)
        print(f"\r{display_message}  {spinner[spin_idx % len(spinner)]}  [{bar}]  ", end="")
        sys.stdout.flush()
        progress += 1
        spin_idx += 1
        time.sleep(0.15)
stop_event = threading.Event()
spinner_thread = threading.Thread(target=spinner_func, args=(stop_event,), daemon=True)
spinner_thread.start()

import json
import os
import sys
import subprocess
import re
from collections import deque
import requests
import distro

# Get terminal output
def get_terminal_output_history(filepath: str, rows: int = 50) -> str:
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
        bottom_rows = deque(f, maxlen=rows)
    # Jätetään 2 viimeisintä riviä pois
    rows_to_use = list(bottom_rows)[:-2] if len(bottom_rows) > 2 else []
    without_ansi_chars = ''.join(ansi_escape.sub('', row) for row in rows_to_use)
    return without_ansi_chars
filepath = os.path.expanduser('~/.apua/terminal_history.log')
terminal_history = get_terminal_output_history(filepath)

# Käyttäjän kysymyksen kerääminen komentoriviltä
question = " ".join(sys.argv[1:])

try:
    ls_proc = subprocess.run(['ls', '-A'], capture_output=True, text=True)
    ls_lines = ls_proc.stdout.splitlines()[:80]
except Exception:
    ls_lines = []
ls_list = "\n".join(ls_lines)

# ENV
shell = os.environ.get('SHELL', '')
pwd = os.environ.get('PWD', '')

# Prompt
api_url = "https://api.llm7.io/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream"
}
token_path = os.path.expanduser('~/.apua/api_token.txt')
if os.path.exists(token_path):
    with open(token_path, 'r') as tiedosto:
        token = tiedosto.read().strip()
    headers['Authorization'] = f'Bearer {token}'
system_msg = {
    "role": "system",
    "content": (
        "Olet Linux komentorivillä toimiva 'apua' tekoälysovellus, joka avustaa aloittelevaa käyttäjää komentorivin käytössä.\n\n"
        "Auta käyttäjää etenemään. Vastaa mahdollisimman lyhyesti. Markdown muotoilu EI käytössä. Et pysty suorittamaan komentoja itsenäisesti. Selkeytä vastaustasi emojilla."
    )
}
user_content = (
    f"Konteksti:\n"
    f"- Linux Distro: {distro.name()} {distro.version()}\n"
    f"- Hakemiston tiedostot:\n{ls_list}\n\n"
    f"- Ympäristömuuttujat: SHELL={shell}, PWD={pwd}\n"
    f"- Terminaalin aiemmat tulosteet:\n{terminal_history}\n\n"
    f"Käyttäjän viesti sinulle:\n\n{question}"
)
user_msg = {"role": "user", "content": user_content}
data = {
    "model": "gpt-5-mini",
    "messages": [system_msg, user_msg],
    "stream": True,
}

try:
    response = requests.post(api_url, headers=headers, json=data, stream=True)
    if response.status_code != 200:
        print(f"Virhe: Palvelin palautti tilan {response.status_code}")
        sys.exit(1)
    got_content = False
    for line in response.iter_lines():
        if not line:
            continue
        line = line.decode('utf-8')
        if line.startswith("data:"):
            payload = line[len("data:"):].strip()
            if payload == "[DONE]":
                break
            chunk = json.loads(payload)
            delta = chunk.get('choices', [])[0].get('delta', {})
            content = delta.get('content', "")
            if content:
                if not got_content:
                    stop_event.set()
                    # Poista spinneri peittämällä se tarpeeksi pitkällä rivillä
                    print("\r" + " " * 90 + "\r", end="")
                    sys.stdout.flush()
                    got_content = True
                print(content, end="", flush=True)
    stop_event.set()
    spinner_thread.join(timeout=0.2)
    print()
except requests.RequestException as e:
    print(f"Virhe vastauksen hakuun: {e}")
    sys.exit(1)
