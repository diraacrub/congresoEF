#!/usr/bin/env python3
"""
Genera los imprimibles del congreso a partir de index.html:

  qr-mesa.pdf      Cartel de mesa con QR (A4 para doblar a la mitad)
  qr-a4.pdf        Cartel A4 con QR para pegar
  programa-a4.pdf  Programa completo en varias hojas A4 (con ponencias)
  programa-a3.pdf  Programa general en una hoja A3

Uso:  python3 imprimibles/generar.py
Requiere: beautifulsoup4, Google Chrome. El QR (qr-programa.svg) se regenera
solo si está instalado el paquete `qrcode`; si no, se usa el SVG existente.
"""
import copy
import os
import subprocess
from pathlib import Path

from bs4 import BeautifulSoup

URL = "https://huayca.crub.uncoma.edu.ar/congresoEF/#programa"
URL_CORTA = "huayca.crub.uncoma.edu.ar/congresoEF"

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
LOGO = "../static/Logo%20educacion%20fisica.jpg"
QR = "qr-programa.svg"

TITULO = "VII Congreso Patagónico, IV Nacional y I Internacional de Educación Física y Formación Docente"
LEMA = "Desafíos e interrogantes de prácticas y saberes en movimiento"
FECHAS = "8, 9 y 10 de octubre de 2026"
SEDE = "Centro Regional Universitario Bariloche · Quintral 1250"

FUENTES = ('<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
           'family=Source+Sans+3:ital,wght@0,400;0,600;0,700;0,800;1,400&display=swap">')

BASE_CSS = """
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
:root { --azul: #14375a; --azul2: #1f5f8b; --tinta: #1d2b38; --gris: #5d6d7e;
        --panel: #1f5f8b; --mesa: #0e7c7b; --taller: #3f8f3a; --acto: #b9770e; --pausa: #95a5a6; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Source Sans 3', 'DejaVu Sans', sans-serif; color: var(--tinta); background: #fff; }
"""


def generar_qr():
    try:
        import qrcode
        import qrcode.image.svg
    except ImportError:
        print("· qrcode no instalado: se usa", QR, "existente")
        return
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    qr.add_data(URL)
    img = qr.make_image(image_factory=qrcode.image.svg.SvgPathFillImage)
    img.save(AQUI / QR)
    print("· QR generado para", URL)


def pagina(titulo, css, cuerpo):
    return (f'<!doctype html><html lang="es"><head><meta charset="utf-8">'
            f'<title>{titulo}</title>{FUENTES}<style>{BASE_CSS}{css}</style></head>'
            f'<body>{cuerpo}</body></html>')


# ───────────────────────────────────────────── QR de mesa y A4
def qr_mesa():
    mitad = f"""
    <div class="mitad">
      <div class="txt">
        <div class="marca"><img src="{LOGO}" alt=""><span>VII Congreso Patagónico de<br>Educación Física y Formación Docente</span></div>
        <h1>Programa<br>del Congreso</h1>
        <p class="sub">Escaneá el código con la cámara de tu celular para ver horarios, aulas, mesas y talleres.</p>
        <p class="fechas">{FECHAS}<br>CRUB · Bariloche</p>
      </div>
      <div class="qr"><img src="{QR}" alt="QR al programa"><p>{URL_CORTA}</p></div>
    </div>"""
    css = """
    @page { size: A4 portrait; margin: 0; }
    .hoja { width: 210mm; height: 297mm; position: relative; overflow: hidden; }
    .mitad { height: 148.5mm; display: flex; align-items: center; gap: 8mm; padding: 12mm 14mm; }
    .mitad:first-child { transform: rotate(180deg); }
    .txt { flex: 1; }
    .marca { display: flex; align-items: center; gap: 3mm; font-size: 9.5pt; line-height: 1.2; color: var(--gris); font-weight: 600; }
    .marca img { height: 15mm; }
    h1 { margin: 6mm 0 4mm; font-size: 34pt; line-height: 1; font-weight: 800; color: var(--azul); }
    .sub { font-size: 13pt; line-height: 1.3; }
    .fechas { margin-top: 5mm; font-size: 11pt; line-height: 1.3; font-weight: 700; color: var(--azul2); }
    .qr { width: 92mm; text-align: center; }
    .qr img { width: 92mm; height: 92mm; display: block; }
    .qr p { margin-top: 2.5mm; font-size: 9.5pt; color: var(--gris); }
    .pliegue { position: absolute; left: 0; right: 0; top: 148.5mm; border-top: 0.3mm dashed #b0b8c0; }
    .pliegue span { position: absolute; right: 4mm; top: -2.2mm; background: #fff; padding: 0 1.5mm; font-size: 6.5pt; color: #9aa4ae; }
    """
    cuerpo = f'<div class="hoja">{mitad}{mitad}<div class="pliegue"><span>doblar aquí</span></div></div>'
    return pagina("QR mesa – Programa", css, cuerpo)


def qr_a4():
    css = """
    @page { size: A4 portrait; margin: 0; }
    .hoja { width: 210mm; height: 297mm; display: flex; flex-direction: column; }
    header { background: linear-gradient(135deg, var(--azul) 0%, var(--azul2) 100%); color: #fff;
             padding: 12mm 16mm 10mm; text-align: center; }
    header .org { font-size: 10pt; letter-spacing: .03em; opacity: .9; }
    header h2 { margin-top: 3mm; font-size: 17pt; line-height: 1.2; font-weight: 700; }
    header .lema { margin-top: 2mm; font-size: 11.5pt; font-style: italic; opacity: .9; }
    main { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding: 0 16mm; }
    h1 { font-size: 54pt; line-height: 1; font-weight: 800; color: var(--azul); }
    .sub { margin-top: 4mm; font-size: 17pt; line-height: 1.3; }
    .qr { margin-top: 10mm; width: 125mm; height: 125mm; }
    .url { margin-top: 5mm; font-size: 12pt; color: var(--gris); }
    footer { display: flex; align-items: center; justify-content: space-between; padding: 0 16mm 12mm; }
    footer img { height: 22mm; }
    footer .dat { text-align: right; font-size: 13pt; line-height: 1.35; font-weight: 700; color: var(--azul2); }
    footer .dat span { font-weight: 400; color: var(--gris); font-size: 11pt; }
    """
    cuerpo = f"""
    <div class="hoja">
      <header>
        <p class="org">Universidad Nacional del Comahue · Centro Regional Universitario Bariloche</p>
        <h2>{TITULO}</h2>
        <p class="lema">{LEMA}</p>
      </header>
      <main>
        <h1>Programa<br>del Congreso</h1>
        <p class="sub">Escaneá el código con la cámara de tu celular<br>para ver horarios, aulas, mesas y talleres</p>
        <img class="qr" src="{QR}" alt="QR al programa">
        <p class="url">{URL_CORTA}</p>
      </main>
      <footer>
        <img src="{LOGO}" alt="">
        <p class="dat">{FECHAS}<br><span>{SEDE}</span></p>
      </footer>
    </div>"""
    return pagina("QR A4 – Programa", css, cuerpo)


# ───────────────────────────────────────────── Programa
def dias_del_index():
    soup = BeautifulSoup((RAIZ / "index.html").read_text(encoding="utf-8"), "html.parser")
    dias = []
    for dia in soup.select("#programa .prog-day"):
        d = copy.copy(dia)
        for b in d.select("button"):
            b.decompose()
        for el in d.select("[hidden]"):
            del el["hidden"]
        dias.append(d)
    return dias


PROG_CSS = """
.cab { display: flex; align-items: center; gap: 5mm; border-bottom: 0.6mm solid var(--azul); padding-bottom: 3mm; }
.cab img.logo { height: 16mm; }
.cab .t { flex: 1; }
.cab .t b { display: block; font-size: 12.5pt; line-height: 1.2; color: var(--azul); }
.cab .t span { font-size: 9pt; color: var(--gris); }
.cab .qr { text-align: center; font-size: 6.5pt; line-height: 1.15; color: var(--gris); }
.cab .qr img { display: block; width: 18mm; height: 18mm; margin: 0 auto 1mm; }

.prog-day-title { margin: 4mm 0 2mm; padding: 1.6mm 4mm; background: var(--azul); color: #fff;
                  font-size: 15pt; font-weight: 800; border-radius: 1.5mm; }
.prog-item { position: relative; padding: 2mm 0 2mm 25mm; border-bottom: 0.2mm solid #dfe4e8; }
.prog-item .prog-time { position: absolute; left: 0; top: 2mm; width: 22mm; }
.prog-time { font-weight: 800; color: var(--azul); font-size: 10.5pt; line-height: 1.25; }
.prog-body { border-left: 1.2mm solid #c5d0da; padding-left: 3mm; font-size: 9.5pt; line-height: 1.32; }
.prog-panel .prog-body { border-color: var(--panel); }
.prog-mesa .prog-body  { border-color: var(--mesa); }
.prog-taller .prog-body { border-color: var(--taller); }
.prog-acto .prog-body  { border-color: var(--acto); }
.prog-pausa .prog-body { border-color: var(--pausa); color: var(--gris); }
.prog-body h4, .prog-tag { break-after: avoid; }
.prog-body h4 { font-size: 11pt; line-height: 1.25; font-weight: 700; margin-bottom: .6mm; }
.prog-pausa h4 { font-weight: 600; }
.prog-tag { display: inline-block; background: var(--panel); color: #fff; font-size: 7.5pt; font-weight: 700;
            text-transform: uppercase; letter-spacing: .05em; padding: .2mm 1.6mm; border-radius: 1mm; margin-bottom: .6mm; }
.prog-body p { margin-top: .4mm; }
.prog-meta strong { color: var(--gris); font-weight: 600; }
.taller-group { margin-top: 1.5mm !important; font-weight: 700; color: var(--taller); }
ul { list-style: none; }
.prog-sublist, .taller-list { margin-top: 1mm; }
.prog-sub, .taller { padding: 1.2mm 0 1.2mm; border-top: 0.2mm dotted #c9d1d8; }
.prog-sub-title, .taller-title { font-size: 10pt; line-height: 1.25; font-weight: 700; }
.prog-sub-meta, .taller-people, .taller-facts { font-size: 8.8pt; color: var(--gris); }
.prog-sub-meta span { font-weight: 600; color: var(--mesa); }
.taller-names { color: var(--tinta); }
.taller-inst::before { content: " · "; }
.taller-fact + .taller-fact::before { content: " · "; }
.taller-fact b { font-weight: 600; }
.taller-desc { display: none; }
.prog-table { width: 100%; border-collapse: collapse; margin-top: 1mm; font-size: 8.3pt; line-height: 1.25; }
.prog-table th { text-align: left; font-weight: 700; color: var(--gris); border-bottom: 0.3mm solid #9fb0bf; padding: .4mm 1.2mm; }
.prog-table td { vertical-align: top; padding: .7mm 1.2mm; border-bottom: 0.15mm solid #e3e7eb; }
.prog-table td:first-child { width: 28%; }
.prog-table td:nth-child(2) { width: 22%; color: var(--gris); }
.prog-table td:last-child { font-weight: 600; }
.prog-table tr { break-inside: avoid; }
.prog-list li { padding: .5mm 0 .5mm 3mm; text-indent: -3mm; font-size: 8.8pt; }
.prog-list li::before { content: "• "; color: var(--gris); }
.prog-list em { font-style: normal; font-weight: 600; }
"""


def programa_a4(dias):
    cab = f"""<div class="cab"><img class="logo" src="{LOGO}" alt="">
      <div class="t"><b>{TITULO}</b><span>{FECHAS} · {SEDE} · Programa completo</span></div>
      <div class="qr"><img src="{QR}" alt="">Programa<br>online</div></div>"""
    css = PROG_CSS + """
    @page { size: A4 portrait; margin: 11mm 12mm 11mm; }
    .dia + .dia { break-before: page; }
    .prog-item { break-inside: avoid; }
    .prog-item:has(.prog-sublist), .prog-item:has(.taller-list) { break-inside: auto; }
    .prog-sub, .taller, .taller-group { break-inside: avoid; }
    .taller-group { break-after: avoid; }
    .prog-sub-title { break-after: avoid; }
    """
    cuerpo = "".join(f'<section class="dia">{cab}{d}</section>' for d in dias)
    return pagina("Programa completo – A4", css, cuerpo)


def programa_a3(dias):
    # Versión resumida: sin listado de ponencias ni presentaciones
    resumidos = []
    for d in dias:
        d = copy.copy(d)
        for el in d.select(".prog-sub-detail, .taller-desc"):
            el.decompose()
        resumidos.append(d)
    css = PROG_CSS + """
    @page { size: A3 portrait; margin: 0; }
    .hoja { width: 297mm; height: 420mm; display: flex; flex-direction: column; overflow: hidden; }
    header { background: linear-gradient(135deg, var(--azul) 0%, var(--azul2) 100%); color: #fff;
             display: flex; align-items: center; gap: 7mm; padding: 9mm 12mm; }
    header .logo { height: 30mm; background: #fff; border-radius: 2mm; padding: 1.5mm; }
    header .t { flex: 1; }
    header .org { font-size: 10pt; opacity: .9; }
    header h1 { font-size: 21pt; line-height: 1.15; font-weight: 800; margin: 1.5mm 0; }
    header .lema { font-size: 12pt; font-style: italic; opacity: .92; }
    header .dat { margin-top: 2mm; font-size: 12.5pt; font-weight: 700; }
    header .qr { background: #fff; color: var(--tinta); border-radius: 2mm; padding: 2.5mm; text-align: center; font-size: 8pt; line-height: 1.2; }
    header .qr img { display: block; width: 30mm; height: 30mm; margin-bottom: 1.2mm; }
    .titulo { padding: 4mm 12mm 0; display: flex; align-items: baseline; justify-content: space-between; }
    .titulo h2 { font-size: 20pt; font-weight: 800; color: var(--azul); }
    .ref { font-size: 9pt; color: var(--gris); display: flex; gap: 4mm; }
    .ref i { display: inline-block; width: 3mm; height: 3mm; border-radius: .6mm; margin-right: 1mm; vertical-align: -.3mm; }
    .cols { flex: 1; min-height: 0; columns: 4; column-gap: 6mm; column-fill: auto; column-rule: 0.2mm solid #dfe4e8; padding: 1mm 12mm 0; }
    .prog-day-title { font-size: 13pt; text-align: center; margin: 2mm 0 1mm; break-after: avoid; }
    .prog-day:first-child .prog-day-title { margin-top: 1mm; }
    .prog-item { padding: 1.2mm 0; break-inside: avoid; }
    .prog-item:has(.prog-sublist), .prog-item:has(.taller-list) { break-inside: auto; }
    .prog-item .prog-time { position: static; width: auto; margin-bottom: .4mm; }
    .prog-sub, .taller { break-inside: avoid; }
    .prog-time { font-size: 10pt; }
    .prog-body { font-size: 8.6pt; padding-left: 2.2mm; }
    .prog-body h4 { font-size: 9.6pt; }
    .prog-sub, .taller { padding: .8mm 0; }
    .prog-sub-title, .taller-title { font-size: 8.8pt; }
    .prog-sub-meta, .taller-people, .taller-facts { font-size: 8pt; }
    .taller-inst { display: none; }
    footer { padding: 3mm 12mm 7mm; font-size: 9pt; color: var(--gris); text-align: center; }
    """
    ref = "".join(f'<span><i style="background:var(--{k})"></i>{n}</span>' for k, n in
                  [("panel", "Paneles"), ("mesa", "Mesas de ponencias"), ("taller", "Talleres"),
                   ("acto", "Actos"), ("pausa", "Pausas")])
    cuerpo = f"""
    <div class="hoja">
      <header>
        <img class="logo" src="{LOGO}" alt="">
        <div class="t">
          <p class="org">Universidad Nacional del Comahue · Centro Regional Universitario Bariloche</p>
          <h1>{TITULO}</h1>
          <p class="lema">{LEMA}</p>
          <p class="dat">{FECHAS} · {SEDE}</p>
        </div>
        <div class="qr"><img src="{QR}" alt="">Ponencias y detalle<br>de cada actividad</div>
      </header>
      <div class="titulo"><h2>Programa general</h2><div class="ref">{ref}</div></div>
      <div class="cols">{"".join(str(d) for d in resumidos)}</div>
      <footer>El listado de ponencias de cada mesa y la descripción de los talleres están en {URL_CORTA}</footer>
    </div>"""
    return pagina("Programa general – A3", css, cuerpo)


def a_pdf(html_path, pdf_path):
    chrome = os.environ.get("CHROME", "google-chrome")
    subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                    "--allow-file-access-from-files", "--virtual-time-budget=8000",
                    f"--print-to-pdf={pdf_path}", html_path.as_uri()],
                   check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("·", pdf_path.name)


def main():
    generar_qr()
    dias = dias_del_index()
    salidas = {
        "qr-mesa": qr_mesa(),
        "qr-a4": qr_a4(),
        "programa-a4": programa_a4(dias),
        "programa-a3": programa_a3(dias),
    }
    for nombre, html in salidas.items():
        h = AQUI / f"{nombre}.html"
        h.write_text(html, encoding="utf-8")
        a_pdf(h, AQUI / f"{nombre}.pdf")


if __name__ == "__main__":
    main()
