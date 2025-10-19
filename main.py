#!/usr/bin/env python3
import os
import sys
import subprocess
import openai
import logging
from logging.handlers import RotatingFileHandler
import re
from collections import deque

import urllib.request

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

# Logging
home = os.path.expanduser("~")
log_dir = os.path.join(home, ".apua", "logs")
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, "apua.log")
logger = logging.getLogger("apua")
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=3)
handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
logger.addHandler(handler)

import urllib.request
# Self update
def self_update_from_github():
    script_path = os.path.realpath(__file__)
    update_url = "https://raw.githubusercontent.com/M4R774/komentorivi-ai-apustaja/refs/heads/main/main.py"
    try:
        with urllib.request.urlopen(update_url, timeout=5) as response:
            new_code = response.read().decode('utf-8')
        with open(script_path, 'r') as f:
            old_code = f.read()
        if new_code != old_code:
            temp_path = script_path + ".new"
            with open(temp_path, "w") as f:
                f.write(new_code)
            os.replace(temp_path, script_path)
            print("\nP\u00e4ivit\u00e4\u00e4n 'apua' uuteen versioon...\n")
            os.execv(sys.executable, [sys.executable, script_path] + sys.argv[1:])
    except Exception:
        pass
# self_update_from_github()

# Käyttäjän kysymyksen kerääminen komentoriviltä
question = " ".join(sys.argv[1:])
logger.info("User prompt: %s", question)

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
from openai.types.chat import ChatCompletionSystemMessageParam, ChatCompletionUserMessageParam

system_msg = ChatCompletionSystemMessageParam(
    role="system",
    content=(
        "Olet Linux komentorivillä toimiva 'apua' tekoälysovellus, joka avustaa aloittelevaa käyttäjää komentorivin käytössä.\n\n"
        "Auta käyttäjää etenemään. Vastaa mahdollisimman lyhyesti. Markdown muotoilu EI käytössä. Et pysty suorittamaan komentoja itsenäisesti. Selkeytä vastaustasi emojilla."
    )
)
user_content = (
    f"Konteksti:\n"
    f"- Hakemiston tiedostot:\n{ls_list}\n\n"
    f"- Ympäristömuuttujat: SHELL={shell}, PWD={pwd}\n"
    f"- Terminaalin aiemmat tulosteet:\n{terminal_history}\n\n"
    f"Käyttäjän viesti sinulle:\n\n{question}"
)
user_msg = ChatCompletionUserMessageParam(
    role="user",
    content=user_content
)

# OpenAI client
api_key = "qv7VtA73ytHdV5rNfBqWKIkRx7e9OceBep6K5PnlUCxSgZJG98BskM6pnJm6OLbsdlEc6YUD3oS+/N62hYtxenKcob9PJEVFkk1ZNegpXPHroDUOpDhamvKrFga0vITqPg=="
client = openai.OpenAI(
    base_url="https://api.llm7.io/v1",
    api_key=api_key
)

try:
    response = client.chat.completions.create(
        model="gpt-5-mini",
        messages=[system_msg, user_msg],
        stream=True
    )
    for chunk in response:
        content = getattr(chunk.choices[0].delta, "content", "")
        if content:
            print(content, end="", flush=True)
except Exception as e:
    print(f"Virhe vastauksen hakuun: {e}")
    sys.exit(1)

print()
