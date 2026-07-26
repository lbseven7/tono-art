#!/usr/bin/env python3
"""Gerador de PDFs dos tutoriais tonoCast (xhtml2pdf)."""

import markdown
from pathlib import Path
from xhtml2pdf import pisa

BASE_DIR = Path(__file__).parent
ENSINO_DIR = BASE_DIR / "ensino"
IMAGES_DIR = BASE_DIR / "images"
CSS_FILE = BASE_DIR / "css" / "tutorial.css"
PDF_DIR = BASE_DIR / "pdf"
LOGO_PATH = IMAGES_DIR / "logo-oficial" / "logo-sb-tono.png"

PDFS = {
    "01-fundamentos-valor-tonal": {
        "titulo": "Fundamentos do Valor Tonal",
        "tutoriais": [
            {"arquivo": "01-o-que-e-valor-tonal.md", "titulo": "O que é Valor Tonal", "slide": "slide-02.jpg"},
            {"arquivo": "02-escala-de-cinzas.md", "titulo": "Escala de Cinzas", "slide": "slide-04.jpg"},
            {"arquivo": "03-luz-e-sombra.md", "titulo": "Luz e Sombra", "slide": "slide-05.jpg"},
        ],
    },
    "02-misturas-percepcao": {
        "titulo": "Misturas e Percepção Visual",
        "tutoriais": [
            {"arquivo": "04-misturas-e-paleta.md", "titulo": "Misturas e Paleta", "slide": "slide-06.jpg"},
            {"arquivo": "05-ilusao-de-optica.md", "titulo": "Ilusão de Óptica", "slide": "slide-08.jpg"},
        ],
    },
    "03-tecnicas-ferramentas": {
        "titulo": "Técnicas e Ferramentas",
        "tutoriais": [
            {"arquivo": "06-posterizacao-e-zonas.md", "titulo": "Posterização e Zonas", "slide": "slide-07.jpg"},
            {"arquivo": "07-risco-linear-e-quadricular.md", "titulo": "Risco Linear e Quadricular", "slide": None},
            {"arquivo": "08-converter-e-isolador.md", "titulo": "Converter e Isolador", "slide": "slide-09.jpg"},
        ],
    },
    "04-grayscale-escala-de-cinza": {
        "titulo": "Grayscale — Escala de Cinza",
        "tutoriais": [
            {"arquivo": "09-grayscale-escala-de-cinza.md", "titulo": "Grayscale (Escala de Cinza)", "slide": None},
        ],
    },
}


def ler_markdown(caminho: Path) -> str:
    texto = caminho.read_text(encoding="utf-8")
    return markdown.markdown(texto, extensions=["extra", "smarty", "sane_lists"])


def gerar_html_capa(titulo: str) -> str:
    logo_src = LOGO_PATH.as_posix()
    return f"""
    <div style="text-align:center; padding-top:200px; page-break-after:always;">
      <img src="{logo_src}" width="80" style="margin-bottom:30px;" />
      <h1 style="font-family:Helvetica;font-size:32pt;color:#1c1a18;border:none;margin-bottom:10px;">
        {titulo}
      </h1>
      <div style="width:60px;height:3px;background:#d88800;margin:20px auto;"></div>
      <p style="font-size:14pt;color:#d88800;font-style:italic;">tonoCast — Tutoriais</p>
      <p style="font-size:9pt;color:#6e6860;margin-top:60px;letter-spacing:2px;text-transform:uppercase;">
        tono.art.br
      </p>
    </div>
    """


def gerar_html_sumario(tutoriais: list) -> str:
    itens = ""
    for t in tutoriais:
        ep_num = t["arquivo"].split("-")[0]
        itens += f"""
        <tr>
          <td style="padding:10px 0;border-bottom:1px solid #e0dbd5;font-size:9pt;color:#d88800;font-weight:bold;letter-spacing:1px;text-transform:uppercase;width:60px;">
            Ep. {ep_num}
          </td>
          <td style="padding:10px 0;border-bottom:1px solid #e0dbd5;font-size:13pt;color:#1c1a18;font-family:Georgia,serif;">
            {t['titulo']}
          </td>
        </tr>"""
    return f"""
    <div style="page-break-after:always;padding:20px 0;">
      <h2 style="font-family:Helvetica;font-size:18pt;color:#d88800;border-bottom:2px solid #d88800;padding-bottom:8px;margin-bottom:20px;">
        Sumário
      </h2>
      <table width="100%" cellpadding="0" cellspacing="0" style="border-collapse:collapse;">
        {itens}
      </table>
    </div>
    """


def gerar_html_tutorial(ep_num: str, titulo: str, conteudo_html: str, slide: str | None) -> str:
    slide_html = ""
    if slide:
        slide_src = (IMAGES_DIR / slide).as_posix()
        slide_html = f"""
        <div style="text-align:center;margin:20px 0;">
          <img src="{slide_src}" width="480" style="border-radius:8px;border:1px solid #e0dbd5;" />
        </div>
        """

    return f"""
    <div style="page-break-before:always;padding-top:10px;">
      <p style="font-size:9pt;color:#d88800;font-weight:bold;letter-spacing:2px;text-transform:uppercase;margin-bottom:4px;">
        Ep. {ep_num}
      </p>
      <h1 style="font-family:Helvetica;font-size:22pt;color:#1c1a18;border-bottom:2px solid #d88800;padding-bottom:10px;margin-bottom:20px;">
        {titulo}
      </h1>
      {slide_html}
      <div style="color:#1c1a18;font-size:10pt;line-height:1.7;">
        {conteudo_html}
      </div>
    </div>
    """


def gerar_html_completo(titulo_pdf: str, tutoriais: list) -> str:
    css_src = CSS_FILE.as_posix()
    capa = gerar_html_capa(titulo_pdf)
    sumario = gerar_html_sumario(tutoriais)

    partes = []
    for t in tutoriais:
        ep_num = t["arquivo"].split("-")[0]
        caminho_md = ENSINO_DIR / t["arquivo"]
        conteudo = ler_markdown(caminho_md)
        partes.append(gerar_html_tutorial(ep_num, t["titulo"], conteudo, t["slide"]))

    conteudo_final = "\n".join(partes)

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <style>
    @page {{
      size: A4;
      margin: 2.5cm 2cm;
      background: #fafaf8;
    }}
    body {{
      font-family: Helvetica, Arial, sans-serif;
      background: #fafaf8;
      color: #1c1a18;
      font-size: 10pt;
      line-height: 1.65;
    }}
    h1 {{
      font-family: Helvetica, Arial, sans-serif;
      font-weight: bold;
    }}
    h2 {{
      font-family: Helvetica, Arial, sans-serif;
      font-weight: bold;
    }}
    p {{
      margin-bottom: 10px;
      text-align: justify;
      color: #1c1a18;
    }}
    strong {{
      color: #d88800;
    }}
    em {{
      color: #d88800;
    }}
    hr {{
      border: none;
      border-top: 1px solid #e0dbd5;
      margin: 30px 0;
    }}
    img {{
      max-width: 100%;
    }}
  </style>
</head>
<body>
  {capa}
  {sumario}
  {conteudo_final}
  <div style="margin-top:40px;padding-top:16px;border-top:1px solid #e0dbd5;font-size:8pt;color:#6e6860;text-align:center;">
    <strong style="color:#d88800;">Tono</strong> — tono.art.br<br/>
    tutoriais tonoCast · valores tonais para artistas
  </div>
</body>
</html>"""


def gerar_pdf(nome: str, titulo: str, tutoriais: list) -> Path:
    html_completo = gerar_html_completo(titulo, tutoriais)
    PDF_DIR.mkdir(exist_ok=True)
    caminho_pdf = PDF_DIR / f"{nome}.pdf"

    with open(caminho_pdf, "w+b") as f:
        pisa.CreatePDF(html_completo, dest=f, encoding="utf-8")

    return caminho_pdf


def main():
    print("Gerando PDFs dos tutoriais tonoCast...\n")
    for nome, config in PDFS.items():
        pdf = gerar_pdf(nome, config["titulo"], config["tutoriais"])
        tamanho_kb = pdf.stat().st_size / 1024
        print(f"  OK {pdf.name} ({tamanho_kb:.0f} KB)")
    print(f"\nPronto! {len(PDFS)} PDFs gerados em: {PDF_DIR}")


if __name__ == "__main__":
    main()
