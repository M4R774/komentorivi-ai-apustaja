#!/bin/bash
# Asennusskripti komentorivisovellus 'apua'lle

echo "🚀 Asennetaan 'apua' AI komentoriviavustaja!"


# Tarkista Python3
if ! command -v python3 > /dev/null; then
    echo "🐍 Python3 puuttuu, asennetaan..."
    sudo apt-get update && sudo apt-get install -y python3 > /dev/null || { echo "❌ Python3-asennus epäonnistui"; exit 1; }
fi

# Tarkista pip3
if ! command -v pip3 > /dev/null; then
    echo "📦 pip3 puuttuu, asennetaan..."
    sudo apt-get install -y python3-pip > /dev/null || { echo "❌ pip3-asennus epäonnistui"; exit 1; }
fi

# Asenna Python-kirjasto requests, jos puuttuu
if ! python3 -c "import requests" &> /dev/null; then
    echo "🔗 Python-kirjasto 'requests' puuttuu, asennetaan..."
    pip3 install --user requests > /dev/null || { echo "❌ requests-kirjaston asennus epäonnistui"; exit 1; }
fi

# Kopioi 'apua' skripti ~/.local/bin ja tee suoritettavaksi
mkdir -p "$HOME/.local/bin"
curl -fsSL https://raw.githubusercontent.com/M4R774/komentorivi-ai-apustaja/refs/heads/main/main.py -o "$HOME/.local/bin/apua"
chmod +x "$HOME/.local/bin/apua"
echo "✅ 'apua' komento ladattu hakemistoon ~/.local/bin/apua"

# Luo lokihakemisto ~/.apua/logs
mkdir -p "$HOME/.apua/logs"
echo "📁 Lokit löytyvät hakemistosta ~/.apua/logs."

# Lisää ~/.local/bin PATHiin, jos ei jo ole
if [ -n "$BASH_VERSION" ]; then
    shell_profile="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    shell_profile="$HOME/.zshrc"
else
    shell_profile="$HOME/.profile"
fi

# Päivitä .bashrc tai .profile
if ! grep -q 'export PATH=.*\$HOME/.local/bin' "$shell_profile" &> /dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$shell_profile"
fi

# Yritetään automatisoida PATH-muutoksen voimaantulo
if [[ $- == *i* ]] && [ -n "$BASH_VERSION" ]; then
    echo "🔄 Otetaan muutokset käyttöön (source $shell_profile)..."
    source "$shell_profile"
    echo "✅ Kaikki on valmista! 'apua' komento on nyt käytettävissä. 🎉"
else
    echo "✅ Asennus valmis!"
    echo ""
    echo "⚠️ HUOM! 'apua' komento on käytettävissä kun avaat uuden terminaalin tai suoritat 'source $shell_profile'. ⚠️"
    echo ""
fi

# Tulosta käyttöohjeet
echo "💡 Käyttö:"
echo "- Kirjoita vain 'apua' ja tekoäly vastaa!"
echo "- Voit myös antaa lisätietoja esim.: 'apua mitä tapahtuu? 🆘'"
echo "- Tekoäly saa automaattisesti ruudulla näkyvän komentorivihistorian, nykyisen työskentelykansion, aiemmin suoritetut komentorivikomennot ja yleisiä tietoja järjestelmän tilasta kontekstiksi."
