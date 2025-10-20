# komentorivi-ai-apustaja

"apua" on komentorivin tekoälyavustaja, joka auttaa ymmärtämään komentoja ja
antaa neuvoja suoraan terminaalissa. Asennusskripti on testattu toimivaksi
Linux Mintin versiolla 22.2. 

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

Pro tip: Voit käydä hakemassa **ilmaisen** API-tokenin osoitteesta llm7.io ja asettaa sen tiedostoon `~/.apua/api_token.txt` niin AI saattaa vastata nopeammin!

## Jos asennus epäonnistuu

Asennusskripti ja itse sovellus tarvitsee toimiakseen seuraavat:
- Bash
- Curl
- Python3
- Requests Python kirjaston

Jos asennusscripti epäonnistuu esimerkiksi Requests kirjaston asentamiseen,
voit yrittää asentaa sen manuaalisesti aptilla (tai vastaavalla).

```bash
sudo apt update
sudo apt install python3-requests
```

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
