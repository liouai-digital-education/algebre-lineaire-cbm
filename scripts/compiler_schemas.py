"""Compile les schémas TikZ de schemas/*.tex en SVG dans assets/schemas/.

Chaque schéma est un document « standalone » qui commence par \\input{_preambule}
(couleurs Liouaï, polices, bibliothèques TikZ). Les fichiers dont le nom commence
par « _ » ne sont pas compilés.

Prérequis : une distribution LaTeX (TeX Live ou MiKTeX) avec TikZ et circuitikz,
et un convertisseur PDF -> SVG : pdftocairo (Poppler), dvisvgm ou Inkscape.

Usage :
    python scripts/compiler_schemas.py            # ne recompile que les schémas modifiés
    python scripts/compiler_schemas.py --tout     # recompile tout
    python scripts/compiler_schemas.py schema-kayak
"""
from __future__ import annotations

import argparse
import pathlib
import shutil
import re
import subprocess
import sys
import tempfile

RACINE = pathlib.Path(__file__).resolve().parent.parent
SOURCES = RACINE / "schemas"
SORTIE = RACINE / "assets" / "schemas"
ECHELLE = 1.6   # agrandissement des SVG produits : le dessin TikZ reste en cm, l'affichage web est plus grand


def convertisseur() -> list[str] | None:
    """Commande de conversion PDF -> SVG disponible sur cette machine."""
    if shutil.which("pdftocairo"):
        return ["pdftocairo", "-svg", "{pdf}", "{svg}"]
    if shutil.which("dvisvgm"):
        return ["dvisvgm", "--pdf", "--no-fonts", "--exact-bbox", "-o", "{svg}", "{pdf}"]
    if shutil.which("inkscape"):
        return ["inkscape", "{pdf}", "--export-type=svg", "--export-text-to-path", "-o", "{svg}"]
    return None


def agrandir(svg: pathlib.Path, facteur: float = ECHELLE) -> bool:
    """Multiplie la largeur et la hauteur affichées du SVG (le viewBox est conservé).

    Un attribut data-echelle mémorise l'agrandissement, pour ne jamais l'appliquer deux fois.
    """
    texte = svg.read_text(encoding="utf-8")
    debut = texte.find("<svg")
    fin = texte.find(">", debut)
    balise = texte[debut:fin]
    if debut < 0 or "data-echelle" in balise or "viewBox" not in balise:
        return False

    def mettre_a_l_echelle(m):
        return f'{m.group(1)}="{float(m.group(2)) * facteur:.3f}{m.group(3)}"'

    nouvelle = re.sub(r'\b(width|height)="([\d.]+)([a-z]*)"', mettre_a_l_echelle, balise)
    nouvelle += f' data-echelle="{facteur}"'
    svg.write_text(texte[:debut] + nouvelle + texte[fin:], encoding="utf-8")
    return True


def compiler(tex: pathlib.Path, conv: list[str]) -> bool:
    svg = SORTIE / f"{tex.stem}.svg"
    with tempfile.TemporaryDirectory() as tmp:
        tmp = pathlib.Path(tmp)
        res = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"-output-directory={tmp}", tex.name],
            cwd=SOURCES, capture_output=True, text=True, encoding="utf-8", errors="replace")
        pdf = tmp / f"{tex.stem}.pdf"
        if res.returncode != 0 or not pdf.exists():
            erreurs = [l for l in res.stdout.splitlines() if l.startswith("!") or "Error" in l]
            print(f"  ÉCHEC {tex.name} :", *erreurs[:5], sep="\n    ")
            return False
        cmd = [c.replace("{pdf}", str(pdf)).replace("{svg}", str(svg)) for c in conv]
        subprocess.run(cmd, check=True, capture_output=True)
    agrandir(svg)
    print(f"  {tex.name} -> {svg.relative_to(RACINE)}")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Compile les schémas TikZ en SVG.")
    parser.add_argument("noms", nargs="*", help="schémas à compiler (sans extension)")
    parser.add_argument("--tout", action="store_true", help="recompiler même les schémas à jour")
    args = parser.parse_args()

    if not shutil.which("pdflatex"):
        sys.exit("pdflatex introuvable : installez TeX Live ou MiKTeX.")
    conv = convertisseur()
    if conv is None:
        sys.exit("Aucun convertisseur PDF -> SVG trouvé : installez Poppler (pdftocairo), dvisvgm ou Inkscape.")

    SORTIE.mkdir(parents=True, exist_ok=True)
    preambule = SOURCES / "_preambule.tex"
    sources = sorted(p for p in SOURCES.glob("*.tex") if not p.name.startswith("_"))
    if args.noms:
        sources = [p for p in sources if p.stem in args.noms]

    a_faire = []
    for tex in sources:
        svg = SORTIE / f"{tex.stem}.svg"
        perime = not svg.exists() or svg.stat().st_mtime < max(tex.stat().st_mtime, preambule.stat().st_mtime)
        if args.tout or args.noms or perime:
            a_faire.append(tex)

    print(f"{len(a_faire)} schéma(s) à compiler sur {len(sources)}.")
    echecs = sum(not compiler(tex, conv) for tex in a_faire)
    if echecs:
        sys.exit(f"{echecs} échec(s).")


if __name__ == "__main__":
    main()
