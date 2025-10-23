import requests
import time
from datetime import datetime
from pathlib import Path

settori = [
    '01/B1', '02/A1', '02/A2', '02/B1', '02/B2',
    '02/C1', '02/D1', '03/A1', '03/A2', '03/B1', '03/B2', '03/C1', '03/C2', '03/D1', '03/D2', '04/A1',
    '04/A2', '04/A3', '04/A4', '05/A1', '05/A2', '05/B1', '05/B2', '05/C1', '05/D1', '05/E1', '05/E2',
    '05/E3', '05/F1', '05/G1', '05/H1', '05/H2', '05/I1', '05/I2', '06/A1', '06/A2', '06/A3', '06/A4',
    '06/B1', '06/C1', '06/D1', '06/D2', '06/D3', '06/D4', '06/D5', '06/D6', '06/E1', '06/E2', '06/E3',
    '06/F1', '06/F2', '06/F3', '06/F4', '06/G1', '06/H1', '06/I1', '06/L1', '06/M1', '06/M2', '06/N1',
    '06/N2', '07/A1', '07/B1', '07/B2', '07/C1', '07/D1', '07/E1', '07/F1', '07/G1', '07/H1', '07/H2',
    '07/H3', '07/H4', '07/H5', '07/I1', '08/A1', '08/A2', '08/A3', '08/A4', '08/B1', '08/B2', '08/B3',
    '08/C1', '08/D1', '08/E1', '08/E2', '08/F1', '09/A1', '09/A2', '09/A3', '09/B1', '09/B2', '09/B3',
    '09/C1', '09/C2', '09/D1', '09/D2', '09/D3', '09/E1', '09/E2', '09/E3', '09/E4', '09/F1', '09/F2',
    '09/G1', '09/G2', '09/H1', '10/A1', '10/B1', '10/C1', '10/D1', '10/D2', '10/D3', '10/D4', '10/E1',
    '10/F1', '10/F2', '10/F3', '10/F4', '10/G1', '10/H1', '10/I1', '10/L1', '10/M1', '10/M2', '10/N1',
    '10/N3', '11/A1', '11/A2', '11/A3', '11/A4', '11/A5', '11/B1', '11/C1', '11/C2', '11/C3', '11/C4',
    '11/C5', '11/D1', '11/D2', '11/E1', '11/E2', '11/E3', '11/E4', '12/A1', '12/B1', '12/B2', '12/C1',
    '12/C2', '12/D1', '12/D2', '12/E1', '12/E2', '12/E3', '12/E4', '12/F1', '12/G1', '12/G2', '12/H1',
    '12/H2', '12/H3', '13/A1', '13/A2', '13/A3', '13/A4', '13/A5', '13/B1', '13/B2', '13/B3', '13/B4',
    '13/B5', '13/C1', '13/D1', '13/D2', '13/D3', '13/D4', '14/A1', '14/A2', '14/B1', '14/B2', '14/C1',
    '14/C2', '14/C3', '14/D1'
]

quadrimestre = '5'
readme_path = Path("README.md")


def get_page(url: str) -> str:
    """Fetches a page and returns its content as text."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; Python script)"}
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
    return response.text


def main():
    # Load or initialize README.md
    if not readme_path.exists():
        readme_path.write_text("\n")

    cache = readme_path.read_text(encoding="utf-8").splitlines()
    cache = "\n".join(cache[6:]) if len(cache) > 6 else ""

    usciti = 0
    usciti_nuovi = 0
    new_found = ""

    for settore in settori:
        if settore in cache:
            print(f"{settore}: SÌ (cached)")
            usciti += 1
            continue

        encoded = settore.replace("/", "%252F")
        url = f"https://asn23.cineca.it/pubblico/miur/esito/{encoded}/1/{quadrimestre}"

        try:
            page = get_page(url)
        except Exception as e:
            print(f"Errore fetching {settore}: {e}")
            continue

        pubblicato = "Sessione Principale" in page
        print(f"{settore}: {'SÌ' if pubblicato else 'NO'}")

        if pubblicato:
            usciti += 1
            usciti_nuovi += 1
            date_str = datetime.now().strftime("%d/%m/%Y")

            new_entry = (
                f"- {date_str}: {settore} "
                f"([I Fascia](https://asn23.cineca.it/pubblico/miur/esito/{encoded}/1/{quadrimestre}), "
                f"[II Fascia](https://asn23.cineca.it/pubblico/miur/esito/{encoded}/2/{quadrimestre}))\n"
            )

            new_found = new_entry + new_found
            readme_path.write_text(new_found + cache, encoding="utf-8")

        time.sleep(0.5)  # 500ms pause

    print(f"\n{usciti_nuovi} nuovi settori pubblicati.")
    print(f"Usciti {usciti} settori su {len(settori)}.\n")

    header = (
        f"# Risultati V Quadrimestre ASN 2023\n\n"
        f"Usciti {usciti} settori su {len(settori)}.\n\n"
        f"Credits: https://github.com/alessandropellegrini/risultati-asn."
    )

    readme_path.write_text(header + new_found + cache, encoding="utf-8")


if __name__ == "__main__":
    main()
