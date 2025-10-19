# komentorivi-ai-apustaja

"apua" on komentorivin tekoälyavustaja, joka auttaa ymmärtämään komentoja ja antaa neuvoja suoraan terminaalissa.

## Asennus

Suorita tämä komento terminaalissa:

```bash
curl -fsSL https://raw.githubusercontent.com/M4R774/komentorivi-ai-apustaja/refs/heads/main/install.sh | bash
```

Asennusskripti:
- Lataa ja asentaa tarvittavat riippuvuudet (python3, pip3, requests)
- Lataa "apua"-komentoskriptin hakemistoon `~/.local/bin/apua`
- Lisää `~/.local/bin` automaattisesti PATH:iin, jos sitä ei vielä ole
- Lisää bashrc:iin (tai vastaavaan) terminaalilokituslohkon

## Käyttö

Kirjoita vain:

```bash
apua mitä toi meinaa?
```

Kysymys lähetetään tekoälylle ja mukaan liitetään:
- Näkyvissä olevaa komentorivihistoriaa
- Nykyinen työskentelukansio ja sen tiedostolistaus
- Käyttöjärjestelmän nimi ja versio

## Päivitys

Aja asennuskomento uudelleen, niin bashrc-lokituslohko ja "apua"-komento päivittyvät automaattisesti.

## Poistaminen


1. Poista halutessasi terminaalilokituslohko tiedostosta `~/.bashrc` (tai vastaavasta). Voit tehdä tämän esimerkiksi seuraavalla komennolla:

	```bash
	sed -i '/BEGIN_TERMINAL_LOGGING/,/END_TERMINAL_LOGGING/d' ~/.bashrc
	```

2. Poista komentoskripti:

	```bash
	rm ~/.local/bin/apua
	```

3. (Vapaaehtoinen) Poista Python ja pip, jos et tarvitse niitä muuhun:

	Ubuntu/Debian:
	```bash
	sudo apt-get remove --purge python3 python3-pip
	sudo apt-get autoremove
	```

	Huom! Python voi olla tarpeellinen monille järjestelmän osille, joten poista se vain jos tiedät mitä olet tekemässä.
