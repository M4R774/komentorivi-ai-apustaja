#!/usr/bin/env python3
import os
import sys
import subprocess
import requests
import json
import logging
from logging.handlers import RotatingFileHandler

# Logituksen asetukset
home = os.path.expanduser("~")
log_dir = os.path.join(home, ".apua", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "apua.log")
logger = logging.getLogger("apua")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(handler)

# Itsepäivitys GitHubista
script_path = os.path.realpath(__file__)
update_url = "https://raw.githubusercontent.com/aleksi/komentorivi-ai-apustaja/main/apua"
try:
    res = requests.get(update_url, timeout=5)
    res.raise_for_status()
    new_code = res.text
    with open(script_path, 'r') as f:
        old_code = f.read()
    if new_code != old_code:
        # Kirjoitetaan uusi versio tiedostoon ja uudelleenkäynnistetään
        temp_path = script_path + ".new"
        with open(temp_path, "w") as f:
            f.write(new_code)
        os.replace(temp_path, script_path)
        print("\nP\u00e4ivit\u00e4\u00e4n 'apua' uuteen versioon...\n")
        os.execv(sys.executable, [sys.executable, script_path] + sys.argv[1:])
except Exception:
    # Päivitysyritys epäonnistui, jatketaan vanhalla versiolla
    pass

# Tarkistetaan, että kysymys-parametri on annettu
if len(sys.argv) < 2:
    print("K\u00e4ytt\u00f6: apua [kysymys]")
    sys.exit(1)
question = " ".join(sys.argv[1:])
logger.info("Question: %s", question)  # Kirjataan lokiin käyttäjän kysymys

# Kerätään kontekstitiedot
try:
    hist_proc = subprocess.run(['bash', '-i', '-c', 'history'], capture_output=True, text=True, env=os.environ)
    hist_lines = hist_proc.stdout.splitlines()[-200:]
except Exception:
    hist_lines = []
# Poistetaan rivinumerot historiasta
history_cmds = []
for line in hist_lines:
    parts = line.strip().split(None, 1)
    cmd = parts[1] if len(parts) > 1 else parts[0]
    history_cmds.append(cmd)
history_str = "\n".join(history_cmds)

cwd = os.getcwd()

try:
    ls_proc = subprocess.run(['ls', '-A'], capture_output=True, text=True)
    ls_lines = ls_proc.stdout.splitlines()[:80]
except Exception:
    ls_lines = []
ls_list = "\n".join(ls_lines)

lang = os.environ.get('LANG', '')
shell = os.environ.get('SHELL', '')
term = os.environ.get('TERM', '')

# Valmistellaan POST-pyyntö LLM7.io:lle (OpenAI-yhteensopiva rajapinta)
api_url = "https://api.llm7.io/v1/chat/completions"
headers = {
    "Content-Type": "application/json",
    "Accept": "text/event-stream"
}
# Roolit: järjestelmä (ohjeistus) ja käyttäjä (kysymys + konteksti)
system_msg = {
    "role": "system",
    "content": ("Olet komentorivillä toimiva tekoälyavustaja. Vastaat suomeksi "
                "käyttäjän esittämiin kysymyksiin hyödyntäen annetun ympäristön kontekstin mukaisia tietoja.")
}
user_content = (
    f"Konteksti:\n"
    f"- Hakemisto: {cwd}\n"
    f"- ls -A -lista:\n{ls_list}\n"
    f"- Ympäristömuuttujat: LANG={lang}, SHELL={shell}, TERM={term}\n"
    f"- Viimeiset {len(history_cmds)} komentoa historyssa:\n{history_str}\n"
    f"K\u00e4ytt\u00e4j\u00e4n kysymys: {question}"
)
user_msg = {"role": "user", "content": user_content}

data = {
    "model": "gpt-4o-mini-2024-07-18",  # Valittu malli
    "messages": [system_msg, user_msg],
    "stream": True
}

# Lähetetään pyyntö ja striimataan vastausta käyttäjälle
try:
    resp = requests.post(api_url, headers=headers, json=data, stream=True)
    if resp.status_code != 200:
        print(f"Virhe: Palvelin palautti tilan {resp.status_code}")
        sys.exit(1)
    # Käsitellään saapuvat streaming-linjat
    for line in resp.iter_lines():
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
                print(content, end="", flush=True)
except requests.RequestException as e:
    print(f"Virhe vastauksen hakuun: {e}")
    sys.exit(1)

print()  # Tulostetaan rivinvaihto lopuksi
