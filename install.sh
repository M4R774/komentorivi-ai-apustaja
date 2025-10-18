#!/bin/bash
# Asennusskripti komentorivisovellus 'apua'lle

# 1. Tarkista Python3
if ! command -v python3 > /dev/null; then
    echo "Python3 puuttuu, asennetaan..."
    sudo apt-get update && sudo apt-get install -y python3 || { echo "Python3-asennus epäonnistui"; exit 1; }
fi

# 2. Tarkista pip3
if ! command -v pip3 > /dev/null; then
    echo "pip3 puuttuu, asennetaan..."
    sudo apt-get install -y python3-pip || { echo "pip3-asennus epäonnistui"; exit 1; }
fi

# 3. Asenna Python-kirjasto requests, jos puuttuu
if ! python3 -c "import requests" &> /dev/null; then
    echo "Python-kirjasto 'requests' puuttuu, asennetaan käyttäjäkohtaisesti..."
    pip3 install --user requests || { echo "requests-kirjaston asennus epäonnistui"; exit 1; }
fi

# 4. Kopioi 'apua' skripti ~/.local/bin ja tee suoritettavaksi
mkdir -p "$HOME/.local/bin"
curl -fsSL https://raw.githubusercontent.com/M4R774/komentorivi-ai-apustaja/refs/heads/main/main.py -o "$HOME/.local/bin/apua"
chmod +x "$HOME/.local/bin/apua"

# 5. Luo lokihakemisto ~/.apua/logs
mkdir -p "$HOME/.apua/logs"

# 6. Lisää ~/.local/bin PATHiin, jos ei jo ole
# Päivitä .bashrc tai .profile
if [ -n "$BASH_VERSION" ]; then
    shell_profile="$HOME/.bashrc"
elif [ -n "$ZSH_VERSION" ]; then
    shell_profile="$HOME/.zshrc"
else
    shell_profile="$HOME/.profile"
fi

if ! grep -q 'export PATH=.*\$HOME/.local/bin' "$shell_profile" &> /dev/null; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$shell_profile"
    echo "Lis\u00e4tty \$HOME/.local/bin PATHiin tiedostossa $shell_profile."
fi

echo "Asennus valmis! Käynnistä uusi terminaali tai suorita 'source $shell_profile' ottaaksesi muutokset voimaan."
