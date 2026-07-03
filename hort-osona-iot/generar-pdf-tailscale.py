#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera el PDF d'instal·lacio i configuracio de Tailscale al Mac.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, Table, TableStyle,
    KeepTogether, Image
)
from reportlab.lib.enums import TA_LEFT

# Paleta hort (mateixa que la web)
OLIVE = HexColor('#3D4A2A')
OCHRE = HexColor('#A8783E')
CREAM = HexColor('#F5EBD8')
LEAF = HexColor('#5C7A3A')
MUD = HexColor('#6B4F2A')
INK = HexColor('#2A2A2A')
INK2 = HexColor('#5A5A52')

OUT = r'C:\Users\iadmin\hort-osona\hort-osona\hort-osona-iot\GUIA-TAILSCALE-MAC.pdf'

doc = SimpleDocTemplate(
    OUT, pagesize=A4,
    leftMargin=20*mm, rightMargin=20*mm,
    topMargin=18*mm, bottomMargin=18*mm,
    title='Guia Tailscale al Mac · Hort Osona',
    author='Hort Osona IoT'
)

ss = getSampleStyleSheet()
H1 = ParagraphStyle('H1', parent=ss['Heading1'], fontSize=22, textColor=OLIVE,
                    spaceAfter=10, spaceBefore=0, fontName='Helvetica-Bold')
H2 = ParagraphStyle('H2', parent=ss['Heading2'], fontSize=15, textColor=OLIVE,
                    spaceAfter=6, spaceBefore=14, fontName='Helvetica-Bold')
H3 = ParagraphStyle('H3', parent=ss['Heading3'], fontSize=12, textColor=MUD,
                    spaceAfter=4, spaceBefore=8, fontName='Helvetica-Bold')
P = ParagraphStyle('P', parent=ss['BodyText'], fontSize=10.5, leading=14,
                   textColor=INK, spaceAfter=6, alignment=TA_LEFT)
CODE = ParagraphStyle('Code', parent=ss['Code'], fontSize=10, leading=13,
                      textColor=INK, backColor=CREAM, borderColor=OCHRE,
                      borderWidth=0.5, borderPadding=6, leftIndent=4, rightIndent=4,
                      spaceAfter=4, spaceBefore=2, fontName='Courier')
TIP = ParagraphStyle('Tip', parent=P, fontSize=10, textColor=OLIVE, leading=13)
SMALL = ParagraphStyle('Small', parent=P, fontSize=8.5, textColor=INK2, alignment=TA_LEFT)

story = []

# ───────── COBERTA ─────────
story.append(Spacer(1, 30*mm))
story.append(Paragraph('🌱 Hort Osona IoT', H1))
story.append(Paragraph('Guia d\'instal·lació de Tailscale al Mac', H2))
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    'Tailscale és una xarxa privada virtual (VPN) gratuïta que et permet accedir '
    'al teu Mac des del mòbil o la Raspberry Pi, sense servidor central ni configurar el router. '
    'Aquesta guia t\'acompanya pas a pas per instal·lar-la al teu Mac, configurar-la al mòbil, '
    'i fer que l\'assistent IA i els sensors IoT funcionin des de qualsevol lloc.',
    P
))
story.append(Spacer(1, 4*mm))
story.append(Paragraph('📅 Data: 2026-07-03 · Versió 1.0', SMALL))
story.append(PageBreak())

# ───────── 1. QUÈ ÉS TAILSCALE ─────────
story.append(Paragraph('1. Què és Tailscale i per què el necessites', H1))
story.append(Paragraph(
    'Tailscale crea una <b>xarxa privada virtual</b> (VPN) que connecta els teus dispositius '
    '(Mac, iPhone, Raspberry Pi) com si estiguessis a la mateixa WiFi, '
    'però funciona des de qualsevol lloc amb cobertura (4G, 5G, WiFi de bar, etc.).',
    P
))
story.append(Paragraph('Avantatges:', H3))
pros = [
    '✅ <b>Gratuït</b> per a ús personal (fins a 100 dispositius)',
    '✅ <b>Zero configuració</b> del router o ports',
    '✅ <b>Privacitat total</b>: les dades no passen per servidors tercers',
    '✅ <b>Funciona des de qualsevol xarxa</b>: 4G, 5G, WiFi públic, etc.',
    '✅ <b>Compatible amb macOS, iOS, Linux, Raspberry Pi</b>',
]
for p in pros:
    story.append(Paragraph(p, P))

story.append(Paragraph('Què hi connectaràs:', H3))
story.append(Paragraph(
    '• L\'<b>assistent IA local</b> (Ollama + RAG) que corre al teu Mac al port 8001<br/>'
    '• Els <b>sensors de l\'hort</b> (Xiaomi MiFlora) que vindran de la Raspberry Pi<br/>'
    '• Qualsevol altre servei que corre al teu Mac o Raspberry',
    P
))
story.append(PageBreak())

# ───────── 2. INSTAL·LACIÓ AL MAC ─────────
story.append(Paragraph('2. Instal·lació al Mac', H1))

story.append(Paragraph('Pas 1 — Obrir el Terminal', H2))
story.append(Paragraph(
    'Al teu Mac, obre l\'app <b>Terminal</b> (la trobaràs a Aplicacions > Utilitats, '
    'o cerca-la amb Spotlight prement <font name="Courier">Cmd + Espai</font>).',
    P
))

story.append(Paragraph('Pas 2 — Instal·lar Tailscale amb Homebrew', H2))
story.append(Paragraph(
    'Si tens Homebrew instal·lat (el gestor de paquets per a Mac), executa:',
    P
))
story.append(Paragraph(
    'brew install --cask tailscale',
    CODE
))
story.append(Paragraph(
    '<b>Si NO tens Homebrew</b>, pots instal·lar Tailscale d\'una altra manera:',
    P
))
story.append(Paragraph(
    '1. Vés a <b>https://tailscale.com/download/mac</b><br/>'
    '2. Descarrega el fitxer <b>.pkg</b><br/>'
    '3. Obre\'l i segueix les instruccions (drag & drop a Aplicacions)',
    P
))

story.append(Paragraph('Pas 3 — Obrir Tailscale i fer login', H2))
story.append(Paragraph(
    'Un cop instal·lat, obre l\'app <b>Tailscale</b> des del Launchpad. Et mostrarà una finstra emergent '
    'demanant-te que iniciïs sessió.',
    P
))
story.append(Paragraph('Tens 4 opcions per fer login:', H3))

login_table = Table([
    ['Opció', 'Recomanació'],
    ['Google', '⭐ La més fàcil. Si tens un compte de Gmail, fes-ho amb aquest.'],
    ['Apple (iCloud)', 'També molt fàcil. Bona opció si tens iCloud.'],
    ['Microsoft (Outlook)', 'Bo si tens correu d\'empresa o de Hotmail.'],
    ['GitHub', 'Tècnic. Recomanable si tens compte de programador.'],
    ['Correu + OTP', 'Crear compte nou. Funciona però és menys pràctic.'],
], colWidths=[40*mm, 120*mm])
login_table.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
    ('TEXTCOLOR', (0, 0), (-1, 0), CREAM),
    ('BACKGROUND', (0, 0), (-1, 0), OLIVE),
    ('FONTSIZE', (0, 1), (-1, -1), 9.5),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.4, OCHRE),
    ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(login_table)
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    '💡 <b>Recomanació</b>: tria <b>Google</b> si tens Gmail, o <b>Apple</b> si ja tens iCloud. '
    'Són els més ràpids.',
    TIP
))
story.append(PageBreak())

# ───────── 3. OBTENIR LA IP ─────────
story.append(Paragraph('3. Obtenir la IP del Mac a Tailscale', H1))
story.append(Paragraph(
    'Un cop loguejat, Tailscale assigna al teu Mac una adreça IP privada del tipus '
    '<b>100.x.x.x</b>. Aquesta és la IP que hauràs d\'usar des del mòbil.',
    P
))

story.append(Paragraph('Com trobar-la:', H2))
story.append(Paragraph(
    '1. Al Mac, obre el <b>Terminal</b><br/>'
    '2. Executa:',
    P
))
story.append(Paragraph(
    'tailscale ip -4',
    CODE
))
story.append(Paragraph(
    '3. Et retornarà una IP com <b>100.84.55.22</b> (les xifres varien)',
    P
))

story.append(Paragraph('Alternativa — des de la interfície gràfica:', H2))
story.append(Paragraph(
    '1. Fes clic a la icona de Tailscale a la <b>barra de menú superior</b> (a dalt a la dreta)<br/>'
    '2. Veure\'s la teva IP <b>100.x.x.x</b> a la finstra emergent<br/>'
    '3. <b>Copia-la</b> — la necessitaràs per al pas 4',
    P
))
story.append(Spacer(1, 4*mm))
story.append(Paragraph(
    '⚠️ <b>Important</b>: no confondre la IP de Tailscale (<font name="Courier">100.x.x.x</font>) '
    'amb la IP de la teva xarxa WiFi local (<font name="Courier">192.168.1.x</font>). '
    'La de Tailscale funciona des de qualsevol xarxa.',
    TIP
))
story.append(PageBreak())

# ───────── 4. MÒBIL ─────────
story.append(Paragraph('4. Instal·lació al mòbil (iPhone)', H1))

story.append(Paragraph('Pas 1 — Descarregar l\'app', H2))
story.append(Paragraph(
    '1. Obre l\'<b>App Store</b> al teu iPhone<br/>'
    '2. Cerca <b>"Tailscale"</b><br/>'
    '3. Descarrega l\'app oficial (gratis, ~30 MB)<br/>'
    '4. Obre-la',
    P
))

story.append(Paragraph('Pas 2 — Fer login amb el MATEIX compte', H2))
story.append(Paragraph(
    'A la pantalla de benvinguda, selecciona el <b>mateix proveïdor</b> que vas fer servir al Mac '
    '(Google, Apple, etc.) i entra amb el <b>mateix compte</b>.',
    P
))
story.append(Paragraph(
    '✅ Si tot ha anat bé, veuràs una pantalla que diu <b>"Connected"</b> amb un lliscant activat. '
    'Això vol dir que el mòbil ja és a la teva xarxa privada Tailscale.',
    P
))

story.append(Paragraph('Pas 3 — Comprovar que funciona', H2))
story.append(Paragraph(
    'Al Terminal del Mac, pots veure quins dispositius estan connectats:',
    P
))
story.append(Paragraph(
    'tailscale status',
    CODE
))
story.append(Paragraph(
    'Hauries de veure dues línies: una per al Mac i una per al mòbil (iPhone), '
    'totes dues amb la IP <b>100.x.x.x</b>.',
    P
))
story.append(PageBreak())

# ───────── 5. CONFIGURAR ASSISTENT ─────────
story.append(Paragraph('5. Connectar l\'assistent IA al mòbil', H1))
story.append(Paragraph(
    'Ara que el mòbil pot veure el Mac a través de Tailscale, podem fer que l\'assistent '
    'IA funcioni des del navegador del mòbil.',
    P
))

story.append(Paragraph('Pas 1 — Assegurar que el backend està actiu', H2))
story.append(Paragraph(
    'Al Mac, comprova que el backend FastAPI encara està corrent:',
    P
))
story.append(Paragraph(
    'curl http://127.0.0.1:8001/chat/health',
    CODE
))
story.append(Paragraph(
    'Si tot va bé, veuràs: <b>{"status":"ok","model":"llama3.1","docs_loaded":147}</b>',
    P
))
story.append(Paragraph(
    'Si NO està actiu, cal arrencar-lo. En una terminal nova, executa:',
    P
))
story.append(Paragraph(
    'cd ~/Documents/hort-osona/hort-osona-iot\n'
    'python -m uvicorn backend.api_chat:app --host 0.0.0.0 --port 8001',
    CODE
))
story.append(Paragraph(
    '⚠️ <b>Important</b>: el paràmetre <font name="Courier">--host 0.0.0.0</font> '
    'és clau — fa que el backend escolti a TOTES les interfícies, no només a localhost.',
    TIP
))

story.append(Paragraph('Pas 2 — Configurar la URL al mòbil', H2))
story.append(Paragraph(
    '1. Al mòbil, obre Safari (o Chrome)<br/>'
    '2. Vés a <b>https://BernatMora.github.io/hort-osona/#assistent</b><br/>'
    '3. A la pàgina, busca el quadre <b>"URL backend"</b> (just a sobre de les preguntes suggerides)<br/>'
    '4. Substitueix <font name="Courier">http://localhost:8001</font> per:',
    P
))
story.append(Paragraph(
    'http://100.84.55.22:8001',
    CODE
))
story.append(Paragraph(
    '5. Fes clic a <b>"Desar"</b><br/>'
    '6. Fes una pregunta — l\'assistent respondrà des del Mac a través de Tailscale!',
    P
))
story.append(Paragraph(
    '🔁 <b>Substitueix 100.84.55.22 per la teva IP real de Tailscale</b> '
    '(l\'has obtinguda al pas 3 de la secció anterior).',
    TIP
))
story.append(PageBreak())

# ───────── 6. PROBLEMES ─────────
story.append(Paragraph('6. Resolució de problemes', H1))

problem_table = Table([
    ['Problema', 'Solució'],
    ['El mòbil no troba el Mac',
     'Comprova que Tailscale està actiu als dos dispositius (icona verda o blava). '
     'També pots executar "tailscale ping mac" al mòbil.'],
    ['"Connexió refusada"',
     'El backend FastAPI pot estar parat. Reinicia\'l amb la comanda del pas 1 de la secció 5.'],
    ['La URL no es desa',
     'A la PWA, el quadre d\'URL desa a localStorage. Si estàs en mode incògnit, '
     'es perdrà cada vegada. Usa el mode normal.'],
    ['El Mac s\'adorm',
     'Vés a System Settings > Energy > i desactiva "Put hard disks to sleep" '
     'i "Prevent computer from sleeping automatically".'],
    ['He canviat de WiFi i ha deixat de funcionar',
     'Tailscale s\'hauria de reconnectar automàticament. Si no, obre l\'app Tailscale '
     'al mòbil i comprova que està actiu.'],
    ['Vull accedir des d\'un altre país',
     'Tailscale funciona des de qualsevol lloc amb cobertura. Només cal que el Mac '
     'estigui encès i connectat a Internet.'],
], colWidths=[45*mm, 120*mm])
problem_table.setStyle(TableStyle([
    ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
    ('TEXTCOLOR', (0, 0), (-1, 0), CREAM),
    ('BACKGROUND', (0, 0), (-1, 0), OLIVE),
    ('FONTSIZE', (0, 1), (-1, -1), 9),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('GRID', (0, 0), (-1, -1), 0.4, OCHRE),
    ('LEFTPADDING', (0, 0), (-1, -1), 5),
    ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ('TOPPADDING', (0, 0), (-1, -1), 4),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
]))
story.append(problem_table)
story.append(PageBreak())

# ───────── 7. SEGÜENTS PASSOS ─────────
story.append(Paragraph('7. Següents passos', H1))
story.append(Paragraph(
    'Un cop tinguis Tailscale funcionant entre el Mac i el mòbil, ja podràs:',
    P
))
story.append(Paragraph('A curt termini:', H3))
story.append(Paragraph(
    '• Usar l\'<b>assistent IA</b> des del mòbil (quan siguis a l\'hort)<br/>'
    '• Rebre <b>alertes</b> si els sensors detecten quelcom (proper pas)<br/>'
    '• Consultar el <b>quadern d\'observació</b> des del mòbil',
    P
))
story.append(Paragraph('A mitjà termini (quan arribi la Raspberry):', H3))
story.append(Paragraph(
    '• Instal·lar Tailscale a la Raspberry Pi (<font name="Courier">curl -fsSL https://tailscale.com/install.sh | sh</font>)<br/>'
    '• Accedir a la pàgina <b>#sensors</b> des del mòbil amb dades reals<br/>'
    '• Veure <b>gràfiques d\'humitat</b> en temps real del teu hort',
    P
))
story.append(Paragraph('Alternatives si Tailscale no funciona:', H3))
story.append(Paragraph(
    'Si tens problemes amb Tailscale, hi ha alternatives:<br/>'
    '• <b>ngrok</b>: túnel HTTP gratuït amb una URL pública<br/>'
    '• <b>Cloudflare Tunnel</b>: similar, una mica més tècnic<br/>'
    '• <b>Només local</b>: obre l\'assistent al mateix Mac, sense mòbil',
    P
))
story.append(Spacer(1, 8*mm))
story.append(Paragraph('─ Fi de la guia ─', SMALL))
story.append(Paragraph(
    'Si tens cap dubte, escriu-me. Bona collita! 🌱',
    TIP
))

doc.build(story)

import os
size = os.path.getsize(OUT)
print(f'PDF generat: {OUT}')
print(f'Mida: {size} bytes')
