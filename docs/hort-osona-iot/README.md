<h1 id="-hort-osona-iot-sistema-complert">🌱 Hort Osona IoT — Sistema complert</h1>
<p>Sistema de monitoratge de l&#x27;hort amb sensors, LoRa, Raspberry Pi, Supabase i Ollama.</p>
<h2 id="-arquitectura">🏗️ Arquitectura</h2>
<pre><code>
┌──────────────────────┐                                ┌──────────────────────┐
│  HORT (400 m)         │                                │  CASA (Raspberry Pi 4) │
│                       │                                │                       │
│  [Sensor humitat]─┐   │                                │                       │
│  [BME280]─────────┤   │     LoRa 868 MHz              │  [Waveshare LoRa HAT] │
│  [18650 + Solar]──┤   │ ────────────────────────────&gt; │           │           │
│  [TTGO LoRa32]   │   │   T:18.5,H:62.3,P:1013.2,    │           ↓           │
│   (ESP32 + OLED)  │   │   S:45,BAT:3.92                │  [lora_receiver.py]   │
└──────────────────────┘                                │           │           │
                                                          │           ↓           │
                                                          │  [Supabase Realtime]  │
                                                          │           │           │
                                                          │           ↓           │
                                                          │  [Ollama + Hermes]   │
                                                          │  (consells cada 6h)   │
                                                          └──────────┬───────────┘
                                                                     │
                                                                     ↓
                                                          ┌──────────────────────┐
                                                          │  GitHub Pages (PWA)   │
                                                          │  Hort Osona Portal    │
                                                          │  + Vista &quot;Hort live&quot;  │
                                                          └──────────────────────┘
</code></pre>
<h2 id="-estructura-del-projecte">📁 Estructura del projecte</h2>
<pre><code>
hort-osona-iot/
├── node-emissor/                  # ESP32 + sensors (a l&#x27;hort)
│   ├── README.md                  # Visió general del node
│   ├── platformio.ini             # Build config
│   ├── src/
│   │   ├── main.cpp              # Cicle deep sleep + sensors + LoRa
│   │   └── config.h              # Pins del TTGO LoRa32
│   ├── specs/bom.json            # Llista de materials
│   └── docs/steps.json           # Guia de muntatge pas a pas
│
├── backend/                       # Raspberry Pi (a casa)
│   ├── lora_receiver.py           # Rep LoRa → Supabase → Ollama
│   ├── api_chat.py                # Xat RAG amb Ollama (existent)
│   ├── main.py                    # Backend MQTT (existent)
│   ├── uart_to_mqtt.py            # Bridge UART-MQTT (existent)
│   └── supabase_schema.sql        # Schema SQL per a Supabase
│
└── web/                           # Frontend (PWA)
    └── hort-live.html             # Vista amb dades realtime
</code></pre>
<h2 id="-flux-de-dades">🔄 Flux de dades</h2>
<ol>
<li><strong>Node hort</strong> (cada 15 min):</li>
<li>Es desperta del deep sleep</li>
<li>Llegeix BME280 (T, H, P) + sensor sol + bateria</li>
<li>Mostra a l&#x27;OLED 5 segons</li>
<li>Envia payload CSV per LoRa</li>
<li>Torna a dormir</li>
</ul>
<ol>
<li><strong>Receptor Pi 4</strong> (continu):</li>
<li>Escolta LoRa amb el HAT SX1262</li>
<li>Parseja el CSV</li>
<li>INSERT a Supabase (<code>mesures</code>)</li>
<li>Cada 6h: crida Ollama, desa consell (<code>consells_ia</code>)</li>
</ul>
<ol>
<li><strong>Web</strong> (a l&#x27;obrir):</li>
<li>Carrega últimes 100 mesures</li>
<li>Mostra stats (T, H, sol, bat)</li>
<li>Dibuixa gràfic 24h</li>
<li>Subscriu al Realtime de Supabase</li>
<li>Actualitza stats quan arriba nova mesura</li>
</ul>
<h2 id="-com-posar-ho-en-marxa">🚀 Com posar-ho en marxa</h2>
<h3 id="pas-1-configurar-supabase">Pas 1: Configurar Supabase</h3>
<ol>
<li>Crear compte a https://supabase.com</li>
<li>Crear nou projecte</li>
<li>Anar a SQL Editor i executar <code>backend/supabase_schema.sql</code></li>
<li>Copiar URL i anon key → posar-les a <code>lora_receiver.py</code> i <code>web/hort-live.html</code></li>
</ul>
<h3 id="pas-2-muntar-el-node-emissor">Pas 2: Muntar el node emissor</h3>
<ul>
<li>Seguir <code>node-emissor/docs/steps.json</code> (10 passos)</li>
<li>Flashejar amb <code>pio run --target upload</code> (PlatformIO)</li>
</ul>
<h3 id="pas-3-muntar-el-receptor-a-la-pi-4">Pas 3: Muntar el receptor a la Pi 4</h3>
<ul>
<li>Connectar el HAT Waveshare SX1262 als pins GPIO</li>
<li>Instal·lar dependencies:</li>
</ul>
<pre><code>
  pip install supabase RPi.GPIO spidev
  git clone https://github.com/lesept777/SX126x.git
  cd SX126x &amp;&amp; sudo python3 setup.py install
</code></pre>
<ul>
<li>Editar <code>lora_receiver.py</code> amb les claus Supabase</li>
<li>Executar: <code>python3 lora_receiver.py</code></li>
</ul>
<h3 id="pas-4-activar-la-vista-web">Pas 4: Activar la vista web</h3>
<ul>
<li>Editar <code>web/hort-live.html</code> amb les claus Supabase</li>
<li>O afegir el botó al portal principal (build_portal_v2.py)</li>
</ul>
<h2 id="-format-del-payload-lora">📊 Format del payload LoRa</h2>
<pre><code>
T:18.5,H:62.3,P:1013.2,S:45,BAT:3.92
</code></pre>
<ul>
<li><strong>T</strong>: temperatura (°C)</li>
<li><strong>H</strong>: humitat ambiental (%)</li>
<li><strong>P</strong>: pressió atmosfèrica (hPa)</li>
<li><strong>S</strong>: humitat del sòl (%)</li>
<li><strong>BAT</strong>: tensió bateria (V)</li>
</ul>
<h2 id="-cost-del-hardware">💰 Cost del hardware</h2>
<table>
<thead><tr>
<th>Component</th>
<th>Preu</th>
</tr></thead><tbody>
<tr>
<td>TTGO LoRa32 868 MHz</td>
<td>22 €</td>
</tr>
<tr>
<td>BME280</td>
<td>8 €</td>
</tr>
<tr>
<td>Sensor sol capacitiu (×2)</td>
<td>7 €</td>
</tr>
<tr>
<td>Bateria 18650 (×2)</td>
<td>16 €</td>
</tr>
<tr>
<td>Panell solar 5V</td>
<td>10 €</td>
</tr>
<tr>
<td>Caixa IP65</td>
<td>8 €</td>
</tr>
<tr>
<td>Cables Dupont</td>
<td>4 €</td>
</tr>
<tr>
<td><strong>HAT Waveshare SX1262</strong></td>
<td><strong>30 €</strong></td>
</tr>
<tr>
<td><strong>TOTAL</strong></td>
<td><strong>~105 €</strong></td>
</tr>
</table>
<h2 id="-cosa-a-fer">🎯 Cosa a fer</h2>
<ul>
<li>[x] Hardware especificat (Bricogeek + Amazon ES)</li>
<li>[x] Node emissor firmware (PlatformIO)</li>
<li>[x] Receptor Python (RPi 4 + LoRa → Supabase)</li>
<li>[x] Schema Supabase (2 taules + Realtime)</li>
<li>[x] Vista web amb dades realtime</li>
<li>[ ] Comprar hardware</li>
<li>[ ] Muntar el node</li>
<li>[ ] Muntar el receptor</li>
<li>[ ] Crear compte Supabase</li>
<li>[ ] Provar el flux complet</li>
</ul>