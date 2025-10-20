#!/bin/bash
# Asennusskripti komentorivisovellus 'apua'lle

echo "🚀 Asennetaan 'apua' AI komentoriviavustaja!"

# Tarkista Python3
if ! command -v python3 > /dev/null; then
    echo "🐍 Python3 puuttuu, asennetaan..."
    sudo apt-get update && sudo apt-get install -y python3 || { echo "❌ Python3-asennus epäonnistui"; exit 1; }
fi

# Tarkista pip3
if ! command -v pip3 > /dev/null; then
    echo "📦 pip3 puuttuu, asennetaan..."
    sudo apt-get install -y python3-pip || { echo "❌ pip3-asennus epäonnistui"; exit 1; }
fi

# Asenna Python-kirjasto requests, jos puuttuu
if ! python3 -c "import requests" &> /dev/null; then
    echo "🔗 Python-kirjasto 'requests' puuttuu, asennetaan..."
    pip3 install --user requests || { echo "❌ requests-kirjaston asennus epäonnistui"; exit 1; }
fi

# Kopioi 'apua' skripti ~/.local/bin ja tee suoritettavaksi
mkdir -p "$HOME/.local/bin"
curl -fsSL https://raw.githubusercontent.com/M4R774/komentorivi-ai-apustaja/refs/heads/main/main.py -o "$HOME/.local/bin/apua"
chmod +x "$HOME/.local/bin/apua"
echo "🛠️ 'apua' komento ladattu hakemistoon ~/.local/bin/apua"

# Lisää ~/.local/bin PATHiin, jos ei jo ole
if [ -n "$BASH_VERSION" ]; then
    shell_profile="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    shell_profile="$HOME/.zshrc"
else
    shell_profile="$HOME/.profile"
fi

LOGDIR="$HOME/.apua"
LOGFILE="$LOGDIR/terminal_history.log"
mkdir -p "$LOGDIR"

# Poista vanha terminal-logging-lohko, jos sellainen löytyy
if grep -q "BEGIN_TERMINAL_LOGGING" "$shell_profile" 2>/dev/null; then
    # Poista kaikki rivit BEGIN...END -väliltä (mukaan lukien)
    sed -i '/BEGIN_TERMINAL_LOGGING/,/END_TERMINAL_LOGGING/d' "$shell_profile"
fi
# Lisää uusi lohko
cat <<'EOF' >> "$shell_profile"
# === BEGIN_TERMINAL_LOGGING ===
# Tallentaa kaikki terminaalin tulosteet ~/.apua/terminal_history.log tiedostoon
if [[ -z $SCRIPT ]]; then
    LOGDIR="$HOME/.apua"
    mkdir -p "$LOGDIR"
    LOGFILE="$LOGDIR/terminal_history.log"
    rm -f "$LOGFILE"
    touch "$LOGFILE"
    export SCRIPT=$LOGFILE
    script -q -f "$SCRIPT"
fi
# === END_TERMINAL_LOGGING ===
EOF

# Päivitä .bashrc
if ! grep -q 'export PATH=.*\$HOME/.local/bin' "$shell_profile" &> /dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$shell_profile"
fi
echo "🤓 PATH-muutos ja script-lokitus lisätty profiilitiedostoon: $shell_profile"

# Yritetään automatisoida PATH-muutoksen voimaantulo
if [[ $- == *i* ]] && [ -n "$BASH_VERSION" ]; then
    echo "🔄 Otetaan muutokset käyttöön (source $shell_profile)..."
    source "$shell_profile"
    echo "✅ Kaikki on valmista! 'apua' komento on nyt käytettävissä. 🎉"
else
    echo "✅ Asennus on valmis! 🎉"
    echo ""
    echo -e "\033[33m⚠️  HUOM! 'apua' komento on käytettävissä vasta kun avaat uuden terminaalin tai suoritat 'source $shell_profile'. ⚠️\033[0m"
    echo ""
fi

# Tulosta käyttöohjeet
echo "💡 Käyttö:"
echo "- Kirjoita vain 'apua' ja tekoäly vastaa!"
echo "- Voit myös antaa lisätietoja esim.: 'apua mitä tapahtuu? 🆘'"
echo "- Tekoäly saa automaattisesti ruudulla näkyvän komentorivihistorian, nykyisen työskentelykansion, aiemmin suoritetut komentorivikomennot ja yleisiä tietoja järjestelmän tilasta kontekstiksi."
echo "- Pro tip: Voit käydä hakemassa ilmaisen API-tokenin osoitteesta llm7.io ja asettaa sen tiedostoon ~/.apua/api_token.txt niin AI saattaa vastata nopeammin!"
