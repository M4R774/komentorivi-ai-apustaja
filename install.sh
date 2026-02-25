#!/usr/bin/env bash
# Asennusskripti komentorivisovellus 'apua'lle

set -euo pipefail

echo "🚀 Asennetaan 'apua' AI komentoriviavustaja!"

# Detect platform
OS_TYPE="$(uname -s)"
if [ "$OS_TYPE" = "Darwin" ]; then
    PLATFORM="mac"
elif [ "$OS_TYPE" = "Linux" ]; then
    PLATFORM="linux"
else
    PLATFORM="unknown"
fi

echo "🔎 Ympäristö: $PLATFORM ($OS_TYPE)"

# Helper: try installing packages with available package manager
install_package() {
    pkg="$1"
    if [ "$PLATFORM" = "mac" ]; then
        if command -v brew >/dev/null 2>&1; then
            brew install "$pkg"
        else
            echo "❌ Homebrew ei löydy. Asenna Homebrew tai Python manuaalisesti: https://brew.sh/" >&2
            return 1
        fi
    elif [ "$PLATFORM" = "linux" ]; then
        if command -v apt-get >/dev/null 2>&1; then
            sudo apt-get update && sudo apt-get install -y "$pkg"
        elif command -v dnf >/dev/null 2>&1; then
            sudo dnf install -y "$pkg"
        elif command -v pacman >/dev/null 2>&1; then
            sudo pacman -S --noconfirm "$pkg"
        else
            echo "❌ Tuntematon Linux-pakettienhallinta — asenna $pkg manuaalisesti." >&2
            return 1
        fi
    else
        echo "❌ Tuntematon alusta — asenna $pkg manuaalisesti." >&2
        return 1
    fi
}

# Ensure python3 exists
if ! command -v python3 >/dev/null 2>&1; then
    echo "🐍 Python3 puuttuu — yritetään asentaa..."
    if ! install_package python3; then
        echo "❌ Python3-asennus epäonnistui tai vaatii manuaalisen asennuksen." >&2
        exit 1
    fi
fi

# Ensure pip (python -m pip) is available
if ! python3 -m pip --version >/dev/null 2>&1; then
    echo "📦 pip (python3 -m pip) puuttuu — yritetään asentaa..."
    if [ "$PLATFORM" = "linux" ] && command -v apt-get >/dev/null 2>&1; then
        sudo apt-get install -y python3-pip || true
    elif [ "$PLATFORM" = "linux" ] && command -v dnf >/dev/null 2>&1; then
        sudo dnf install -y python3-pip || true
    elif [ "$PLATFORM" = "mac" ] && command -v brew >/dev/null 2>&1; then
        brew install python || true
    else
        echo "⚠️  pip:n asennusta ei voitu automatisoida; yritetään käyttää get-pip.py..."
        curl -sS https://bootstrap.pypa.io/get-pip.py -o /tmp/get-pip.py
        python3 /tmp/get-pip.py --user || true
        rm -f /tmp/get-pip.py
    fi
fi

# Install requests if missing
if ! python3 -c "import requests" &>/dev/null; then
    echo "🔗 Python-kirjasto 'requests' puuttuu — asennetaan käyttäjätilille..."
    if python3 -m pip install --user requests; then
        echo "✅ requests asennettu käyttäjätilille"
    else
        echo "❌ requests-asennus epäonnistui, yritä suorittaa 'python3 -m pip install --user requests' manuaalisesti." >&2
    fi
fi

# Install the wrapper script to ~/.local/bin
mkdir -p "$HOME/.local/bin"
RAW_URL="https://raw.githubusercontent.com/M4R774/komentorivi-ai-apustaja/main/main.py"
echo "⬇️ Ladataan apua-komentoskripti..."
if curl -fsSL "$RAW_URL" -o "$HOME/.local/bin/apua"; then
    chmod +x "$HOME/.local/bin/apua"
    echo "🛠️ 'apua' komento ladattu hakemistoon ~/.local/bin/apua"
else
    echo "❌ Lataus epäonnistui: $RAW_URL" >&2
    exit 1
fi

# Choose shell profile file
shell_profile="$HOME/.profile"
if [ -n "${BASH_VERSION-}" ] && [ -f "$HOME/.bashrc" ]; then
    shell_profile="$HOME/.bashrc"
elif [ -n "${ZSH_VERSION-}" ] && [ -f "$HOME/.zshrc" ]; then
    shell_profile="$HOME/.zshrc"
fi

LOGDIR="$HOME/.apua"
LOGFILE="$LOGDIR/terminal_history.log"
mkdir -p "$LOGDIR"

# Remove existing terminal-logging block (portable)
if [ -f "$shell_profile" ] && grep -q "BEGIN_TERMINAL_LOGGING" "$shell_profile" 2>/dev/null; then
    awk 'BEGIN{skip=0} /BEGIN_TERMINAL_LOGGING/{skip=1; next} /END_TERMINAL_LOGGING/{skip=0; next} !skip{print}' "$shell_profile" > "$shell_profile.tmp" && mv "$shell_profile.tmp" "$shell_profile"
fi

# Append new terminal logging block
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

# Ensure ~/.local/bin is in PATH in the profile
if ! grep -q 'export PATH=.*\$HOME/.local/bin' "$shell_profile" 2>/dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$shell_profile"
fi

echo "🤓 PATH-muutos ja script-lokitus lisätty profiilitiedostoon: $shell_profile"

# Try to source profile if interactive
if [[ $- == *i* ]]; then
    echo "🔄 Otetaan muutokset käyttöön (source $shell_profile)..."
    # shellcheck disable=SC1090
    source "$shell_profile" || true
    echo "✅ Kaikki on valmista! 'apua' komento on nyt käytettävissä. 🎉"
else
    echo "✅ Asennus on valmis! 🎉"
    echo
    echo "⚠️  HUOM! 'apua' komento on käytettävissä vasta kun avaat uuden terminaalin tai suoritat 'source $shell_profile'."
    echo
fi

# Usage tips
echo "💡 Käyttö:"
echo "- Kirjoita vain 'apua' ja tekoäly vastaa!"
echo "- Voit myös antaa lisätietoja esim.: 'apua mitä tapahtuu? 🆘'"
echo "- Tekoäly saa automaattisesti ruudulla näkyvän komentorivihistorian, nykyisen työskentelykansion, aiemmin suoritetut komentorivikomennot ja yleisiä tietoja järjestelmän tilasta kontekstiksi."
echo "- Pro tip: Voit käydä hakemassa ilmaisen API-tokenin osoitteesta llm7.io ja asettaa sen tiedostoon ~/.apua/api_token.txt niin AI saattaa vastata nopeammin!"
