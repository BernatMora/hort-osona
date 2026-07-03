#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Genera un PDF amb la llista de compra d'Amazon per al projecte Hort Osona IoT.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER

OUTPUT = r"C:\Users\iadmin\hort-osona\hort-osona\hort-osona-iot\PEDIDO-AMAZON.pdf"

# Paleta del projecte
COLOR_OLIVE = HexColor("#3D4A2A")
COLOR_OCHRE = HexColor("#A8783E")
COLOR_BG = HexColor("#F5EBD8")
COLOR_LIGHT = HexColor("#E8DCC0")

# Estils
styles = getSampleStyleSheet()
title_style = ParagraphStyle('Title', parent=styles['Title'],
    fontSize=24, textColor=COLOR_OLIVE, spaceAfter=8, alignment=TA_CENTER)
subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'],
    fontSize=12, textColor=COLOR_OCHRE, spaceAfter=20, alignment=TA_CENTER)
h1_style = ParagraphStyle('H1', parent=styles['Heading1'],
    fontSize=18, textColor=COLOR_OLIVE, spaceBefore=20, spaceAfter=10,
    borderPadding=8, leftIndent=0)
h2_style = ParagraphStyle('H2', parent=styles['Heading2'],
    fontSize=14, textColor=COLOR_OLIVE, spaceBefore=12, spaceAfter=6)
normal = ParagraphStyle('Normal', parent=styles['Normal'],
    fontSize=10, leading=14, spaceAfter=6, alignment=TA_LEFT)
small = ParagraphStyle('Small', parent=styles['Normal'],
    fontSize=8, leading=10, textColor=HexColor("#666666"))
price_style = ParagraphStyle('Price', parent=styles['Normal'],
    fontSize=10, alignment=TA_LEFT, fontName='Helvetica-Bold')


def hr():
    """Línia horitzontal."""
    t = Table([['']], colWidths=[17*cm], rowHeights=[0.05*cm])
    t.setStyle(TableStyle([('BACKGROUND', (0,0), (-1,-1), COLOR_OLIVE)]))
    return t


def section_header(emoji, text):
    """Capçalera de secció amb emoji."""
    return Paragraph(f"{emoji}  {text}", h1_style)


def product_table(rows):
    """Genera una taula amb productes (4 columnes: #, Producte, Quant., Preu)."""
    data = [['#', 'Producte', 'Quant.', 'Preu aprox.']]
    for r in rows:
        data.append(r)
    t = Table(data, colWidths=[1*cm, 11*cm, 1.5*cm, 3.5*cm])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_OLIVE),
        ('TEXTCOLOR', (0,0), (-1,0), white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,0), 11),
        ('BOTTOMPADDING', (0,0), (-1,0), 8),
        ('TOPPADDING', (0,0), (-1,0), 8),
        ('BACKGROUND', (0,1), (-1,-1), COLOR_BG),
        ('TEXTCOLOR', (0,1), (-1,-1), black),
        ('FONTSIZE', (0,1), (-1,-1), 9),
        ('ALIGN', (0,0), (0,-1), 'CENTER'),
        ('ALIGN', (2,0), (2,-1), 'CENTER'),
        ('ALIGN', (3,0), (3,-1), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, COLOR_OCHRE),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [COLOR_BG, COLOR_LIGHT]),
    ]))
    return t


# Document
doc = SimpleDocTemplate(
    OUTPUT, pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="PEDIDO-AMAZON — Hort Osona IoT",
    author="Bernat Mora",
)

story = []

# === TITULAR ===
story.append(Paragraph("🛒 Llista de compra Amazon", title_style))
story.append(Paragraph("Hort Osona IoT — Sistema de sensors amb Raspberry Pi 4", subtitle_style))
story.append(hr())
story.append(Spacer(1, 0.5*cm))

# === INFO GENERAL ===
info = (
    "<b>Data:</b> 2026-07-03<br/>"
    "<b>Projecte:</b> Hort Osona IoT (sensors MiFlora + LoRa 868MHz + backend Raspberry Pi 4)<br/>"
    "<b>Estratègia triada:</b> Opció 1 — Tot d'Amazon España (1-2 dies d'entrega)<br/>"
    "<b>Pressupost total:</b> ~220€<br/>"
    "<b>Repositori:</b> https://github.com/BernatMora/hort-osona"
)
story.append(Paragraph(info, normal))
story.append(Spacer(1, 0.3*cm))

# === SECCIÓ 1: RASPBERRY PI 4B ===
story.append(section_header("🖥️", "1. Raspberry Pi 4B (core del sistema)"))
story.append(Paragraph(
    "El cervell del sistema. Compacte, eficient (~5W), perfecta per funcionar 24/7 a casa.",
    normal
))
story.append(Spacer(1, 0.2*cm))
story.append(product_table([
    ['1', 'Raspberry Pi 4 Model B 4GB', '1', '55-65€'],
    ['2', 'Carregador USB-C 5V/3A oficial ⚠️', '1', '12-15€'],
    ['3', 'MicroSD 32GB Classe 10 A2 (Sandisk/Samsung)', '1', '8-12€'],
    ['4', 'Carcassa alumini + dissipador', '1', '10-15€'],
]))
story.append(Paragraph(
    "<b>⚠️ Important:</b> El carregador ha de ser 5V/3A mínim. Un de 2A farà reiniciar la Pi sota càrrega.",
    small
))
story.append(Paragraph("<b>Subtotal secció 1: ~85-105€</b>", price_style))
story.append(Spacer(1, 0.3*cm))

# === SECCIÓ 2: SENSORS I LORA ===
story.append(section_header("📡", "2. Sensors Xiaomi i gateway LoRa"))
story.append(Paragraph(
    "3 sensors d'humitat del sòl + 1 termòmetre ambient. Comunicació via LoRa 868MHz a 245m de distància.",
    normal
))
story.append(Spacer(1, 0.2*cm))
story.append(product_table([
    ['5', 'Xiaomi MiFlora 4-en-1 (humitat, llum, T, fertilitat)', '3', '45€'],
    ['6', 'Xiaomi Mi Thermometer 2 (T + humitat aire)', '1', '8€'],
    ['7', 'TTGO LoRa32 V2 (868MHz, NO 915MHz) ⚠️', '2', '40€'],
    ['8', 'Antena 868MHz 5dBi SMA (per al gateway)', '1', '5€'],
    ['9', 'Caixa estanca IP65 158×90×65mm (pont a l\'hort)', '1', '5€'],
]))
story.append(Paragraph(
    "<b>⚠️ Important:</b> El TTGO ha de ser 868MHz (UE), mai 915MHz (US). Verifica-ho al títol del producte.",
    small
))
story.append(Paragraph("<b>Subtotal secció 2: ~103€</b>", price_style))
story.append(Spacer(1, 0.3*cm))

# === SECCIÓ 3: SOLAR ===
story.append(section_header("🔋", "3. Alimentació solar (per al pont a l'hort)"))
story.append(Paragraph(
    "El pont a l'hort funciona amb energia solar + bateria. Autonomia de mesos sense intervenció.",
    normal
))
story.append(Spacer(1, 0.2*cm))
story.append(product_table([
    ['10', 'Panell solar 5V/2W USB', '1', '12€'],
    ['11', 'Bateria 18650 3000mAh', '1', '5€'],
    ['12', 'Mòdul TP4056 AMB PROTECCIÓ (DW01A) ⚠️', '1', '3€'],
]))
story.append(Paragraph(
    "<b>⚠️ Important:</b> El TP4056 ha de portar el xip DW01A de protecció contra sobrecàrrega. La versió barata sense protecció pot danyar la bateria.",
    small
))
story.append(Paragraph("<b>Subtotal secció 3: ~20€</b>", price_style))
story.append(Spacer(1, 0.3*cm))

# === SECCIÓ 4: CABLES ===
story.append(section_header("🔌", "4. Cables i accessoris"))
story.append(Paragraph(
    "Cablejat bàsic per connectar-ho tot.",
    normal
))
story.append(Spacer(1, 0.2*cm))
story.append(product_table([
    ['13', 'Pack cables Dupont + resistències assortides', '1', '5€'],
    ['14', 'Cable Ethernet Cat6 1-2m (Pi al router)', '1', '3-5€'],
]))
story.append(Paragraph("<b>Subtotal secció 4: ~8-10€</b>", price_style))
story.append(Spacer(1, 0.5*cm))

# === TOTAL ===
story.append(hr())
story.append(Spacer(1, 0.3*cm))
total_box = Table(
    [['TOTAL ESTIMAT', '~220€']],
    colWidths=[10*cm, 5*cm]
)
total_box.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,-1), COLOR_OLIVE),
    ('TEXTCOLOR', (0,0), (-1,-1), white),
    ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 16),
    ('ALIGN', (0,0), (0,-1), 'CENTER'),
    ('ALIGN', (1,0), (1,-1), 'CENTER'),
    ('BOTTOMPADDING', (0,0), (-1,-1), 12),
    ('TOPPADDING', (0,0), (-1,-1), 12),
]))
story.append(total_box)
story.append(Spacer(1, 0.5*cm))

# === CONSELLS ===
story.append(section_header("🔍", "Consells importants abans de comprar"))
consells = [
    "<b>Raspberry Pi 4:</b> Compra directament a Kubii, Melopero o venedors amb moltes valoracions. NO compris a venedors tercers sospitosos (hi ha falsificacions).",
    "<b>TTGO LoRa32:</b> Ha de ser 868MHz (UE), mai 915MHz (US). Mira la descripció i les fotos del xip SX1276 — la versió 868MHz porta '868' marcat.",
    "<b>Xiaomi MiFlora:</b> Compra la versió oficial Xiaomi (blanc amb logotip Mi). Les còpies barates sovint no tenen el xip BLE correcte.",
    "<b>MicroSD:</b> Ha de ser classe A2 (Application class 2), no només A1. La diferència es nota en arrencada i lectura aleatòria.",
    "<b>TP4056:</b> Ha de portar el xip DW01A de protecció. La versió barata pot danyar la bateria o crear situacions de risc.",
]
for c in consells:
    story.append(Paragraph(f"• {c}", normal))
    story.append(Spacer(1, 0.1*cm))

story.append(Spacer(1, 0.5*cm))

# === ON POSAR-HO ===
story.append(section_header("📍", "On instal·lar-ho"))
story.append(Paragraph("<b>Raspberry Pi (a casa):</b>", normal))
story.append(Paragraph("• Al costat del router, connectada per Ethernet", small))
story.append(Paragraph("• O en un calaix/oficina amb bona ventilació", small))
story.append(Paragraph("• Consum: 5W ≈ 0,5€/mes ≈ 6€/any", small))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>Pont LoRa (a l'hort):</b>", normal))
story.append(Paragraph("• Al cobert, a 5-10m dels sensors (per Bluetooth)", small))
story.append(Paragraph("• Dins la caixa estanca IP65", small))
story.append(Paragraph("• Panell solar mirant amunt, protegit de la pluja directa", small))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>Sensors MiFlora (al sòl):</b>", normal))
story.append(Paragraph("• Enterrats a 20-30cm, on hi ha les arrels", small))
story.append(Paragraph("• A 15-20cm de la planta", small))
story.append(Paragraph("• Cap blanc visible per canviar piles", small))
story.append(Spacer(1, 0.2*cm))

story.append(Paragraph("<b>Termòmetre (ambient):</b>", normal))
story.append(Paragraph("• A 1m del terra, a l'ombra", small))
story.append(Paragraph("• NO al sol directe (lectures errònies)", small))

story.append(PageBreak())

# === TIMELINE ===
story.append(section_header("🗓️", "Què fer quan arribi tot"))
timeline = [
    ("1-2 h", "Muntar la Raspberry (carcassa, microSD flashejada, Ethernet, alimentació)"),
    ("1-2 h", "Primer boot headless, connexió SSH des del Mac"),
    ("15 min", "Executar setup-pi.sh — instal·la tot el programari"),
    ("30 min", "Flashejar els TTGO amb MicroPython"),
    ("15 min", "Configurar adreces MAC dels sensors a bridge/main.py"),
    ("1-2 h", "Provar el sistema: logs, MQTT, API"),
    ("30 min", "Integrar amb la PWA (secció 📡 Sensors)"),
]
data = [['Temps', 'Tasca']]
for t, task in timeline:
    data.append([t, task])
t = Table(data, colWidths=[2.5*cm, 12.5*cm])
t.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), COLOR_OLIVE),
    ('TEXTCOLOR', (0,0), (-1,0), white),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('FONTSIZE', (0,0), (-1,-1), 10),
    ('ALIGN', (0,0), (0,-1), 'CENTER'),
    ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ('GRID', (0,0), (-1,-1), 0.5, COLOR_OCHRE),
    ('ROWBACKGROUNDS', (0,1), (-1,-1), [COLOR_BG, COLOR_LIGHT]),
    ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ('TOPPADDING', (0,0), (-1,-1), 6),
]))
story.append(t)
story.append(Spacer(1, 0.5*cm))

# === ENLLAÇOS ===
story.append(section_header("🔗", "Enllaços útils"))
links = [
    ("PWA publicada", "https://BernatMora.github.io/hort-osona/"),
    ("Repositori GitHub", "https://github.com/BernatMora/hort-osona"),
    ("Llista de compra completa", "https://github.com/BernatMora/hort-osona/blob/main/hort-osona-iot/PEDIDO-AMAZON.md"),
    ("Llista curta imprimible", "https://github.com/BernatMora/hort-osona/blob/main/hort-osona-iot/LLISTA-CURTA.md"),
    ("Guia ràpida", "https://github.com/BernatMora/hort-osona/blob/main/hort-osona-iot/INICI-RAPID.md"),
    ("README complet del projecte IoT", "https://github.com/BernatMora/hort-osona/blob/main/hort-osona-iot/README.md"),
    ("Raspberry Pi Imager (descarregar)", "https://www.raspberrypi.com/software/"),
    ("MicroPython per a ESP32", "https://micropython.org/download/ESP32/"),
    ("Kubii (distribuïdor oficial Raspberry a Espanya)", "https://www.kubii.com/"),
    ("Melopero (distribuïdor oficial Raspberry a Espanya)", "https://www.melopero.com/"),
]
for label, url in links:
    story.append(Paragraph(f"• <b>{label}:</b> {url}", small))
    story.append(Spacer(1, 0.05*cm))

story.append(Spacer(1, 1*cm))
story.append(hr())
story.append(Spacer(1, 0.3*cm))
story.append(Paragraph(
    "Fet amb 🫀 per Bernat Mora — Vic, Osona, 2026-07-03",
    ParagraphStyle('Footer', parent=styles['Normal'],
                   fontSize=9, textColor=COLOR_OCHRE, alignment=TA_CENTER)
))

# Generar
doc.build(story)
print(f"✅ PDF generat: {OUTPUT}")
import os
size = os.path.getsize(OUTPUT)
print(f"   Mida: {size:,} bytes ({size/1024:.1f} KB)")
