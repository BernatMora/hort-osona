/**
 * main.cpp — Node emissor LoRa per a l'hort d'Osona
 *
 * Cicle:
 *   1. Desperta del deep sleep
 *   2. Llegeix sensor humitat del sol (capacitiu, GPIO 4)
 *   3. Llegeix sensor temperatura DS18B20 (1-Wire, GPIO 5)
 *   4. Llegeix tensio bateria (divisor, GPIO 1)
 *   5. Envia payload JSON per LoRaWAN 868 MHz
 *   6. Deep sleep 15 minuts
 *
 * Hardware:
 *   - ESP32-S3 amb LoRa SX1262 (Waveshare o Waveshare SX1262)
 *   - Sensor humitat del sol capaciti (3 pins)
 *   - Sensor temperatura DS18B20 amb sonda d'acer
 *   - Bateria LiPo 3.7V 2000mAh
 *   - Panell solar 5V 1W (opcional)
 *
 * Connexions:
 *   Sensor humitat:  VCC -> 3V3,  GND -> GND,  AOUT -> GPIO 4
 *   DS18B20:         VCC -> 3V3,  GND -> GND,  DATA -> GPIO 5 (amb R 4.7k a VCC)
 *   Bateria:         Sortida del TP4056 -> 3V3/GND (amb divisor 100k/100k a GPIO 1)
 */

#include <Arduino.h>
#include <SPI.h>
#include <RadioLib.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <ArduinoJson.h>
#include "config.h"

// ──────────── Objectes globals ────────────
SX1262 radio = new Module(LORA_CS, LORA_DIO1, LORA_RST, LORA_BUSY);
OneWire oneWire(ONE_WIRE_PIN);
DallasTemperature ds18b20(&oneWire);

// ──────────── Variables globals ────────────
RTC_DATA_ATTR int bootCount = 0;  // Persisteix entre deep sleeps
RTC_DATA_ATTR int txFailCount = 0;  // Persisteix entre deep sleeps

// ──────────── Funcions auxiliars ────────────

/**
 * Inicialitza el sensor DS18B20.
 * Retorna true si OK.
 */
bool initDS18B20() {
    ds18b20.begin();
    int deviceCount = ds18b20.getDeviceCount();
    if (deviceCount == 0) {
        Serial.println("[DS18B20] ERROR: cap sensor detectat");
        return false;
    }
    Serial.printf("[DS18B20] OK: %d sensor(s) detectat(s)\n", deviceCount);
    ds18b20.setResolution(DS18B20_RESOLUTION);
    return true;
}

/**
 * Llegeix la temperatura del DS18B20 en graus Celsius.
 * Retorna NaN si falla.
 */
float readTemperature() {
    ds18b20.requestTemperatures();
    float t = ds18b20.getTempCByIndex(0);
    if (t == DEVICE_DISCONNECTED_C) {
        Serial.println("[DS18B20] ERROR: lectura fallida");
        return NAN;
    }
    return t;
}

/**
 * Llegeix el sensor d'humitat del sol amb N mostres i retorna %.
 * Mapeig linial: 0% (sec) = 3500, 100% (moll) = 1500 (calibrar).
 * IMPORTANT: calibrar un cop tinguis el sensor a la ma.
 */
int readSoilMoisture() {
    long sum = 0;
    for (int i = 0; i < SOIL_SAMPLES; i++) {
        sum += analogRead(SOIL_SENSOR_PIN);
        delay(5);
    }
    int raw = sum / SOIL_SAMPLES;

    // Mapeig a % (calibrar segons el sensor)
    // Deixar al sec: ~3500
    // Submergit en aigua: ~1500
    const int RAW_DRY = 3500;
    const int RAW_WET = 1500;
    int pct = map(raw, RAW_DRY, RAW_WET, 0, 100);
    return constrain(pct, 0, 100);
}

/**
 * Llegeix la tensio de la bateria amb divisor de tensio.
 * Assumint divisor 100k/100k: Vbat = Vadc * 2
 */
float readBattery() {
    int raw = analogRead(BATTERY_PIN);
    // ESP32 ADC: 0-3.3V sobre 12 bits (0-4095)
    float v_adc = (raw / 4095.0) * 3.3;
    float v_bat = v_adc * BATTERY_DIVIDER_RATIO;
    return v_bat;
}

/**
 * Construeix el payload JSON amb les dades dels sensors.
 */
String buildPayload(float t, int soil, float vbat) {
    StaticJsonDocument<200> doc;
    doc["id"] = NODE_ID;
    doc["loc"] = NODE_LOCATION;
    doc["boot"] = bootCount;
    doc["t"] = isnan(t) ? -999 : t;  // -999 si no es pot llegir
    doc["soil"] = soil;
    doc["vbat"] = vbat;
    doc["uptime"] = millis() / 1000;  // segons des del wakeup

    String output;
    serializeJson(doc, output);
    return output;
}

/**
 * Inicialitza el modul LoRa SX1262.
 */
bool initLoRa() {
    Serial.print("[LoRa] Inicialitzant... ");
    int state = radio.begin(
        LORA_FREQUENCY,
        LORA_BANDWIDTH,
        LORA_SPREADING_FACTOR,
        5,        // Coding rate
        LORA_TX_POWER,
        8,        // Preamble length
        1.6,      // TCXO voltage (si s'escau)
        false     // Use TCXO?
    );
    if (state != RADIOLIB_ERR_NONE) {
        Serial.printf("FAIL (%d)\n", state);
        return false;
    }
    Serial.println("OK");
    return true;
}

/**
 * Envia payload per LoRa amb retry.
 */
bool sendLoRa(const String& payload, int maxRetries = 3) {
    for (int attempt = 1; attempt <= maxRetries; attempt++) {
        int state = radio.transmit(payload.c_str());
        if (state == RADIOLIB_ERR_NONE) {
            Serial.printf("[LoRa] TX OK (intent %d): %s\n", attempt, payload.c_str());
            return true;
        }
        Serial.printf("[LoRa] TX FAIL (intent %d): %d\n", attempt, state);
        if (attempt < maxRetries) {
            delay(1000 + random(500));  // Backoff aleatori
        }
    }
    txFailCount++;
    return false;
}

// ──────────── SETUP ────────────
void setup() {
    Serial.begin(115200);
    delay(100);

    bootCount++;
    Serial.printf("\n=== Boot #%d ===\n", bootCount);
    Serial.printf("[Node] %s @ %s\n", NODE_ID, NODE_LOCATION);

    // Inicialitza sensors
    initDS18B20();

    // Inicialitza LoRa
    initLoRa();
}

// ──────────── LOOP ────────────
void loop() {
    // 1. Llegir sensors
    float t = readTemperature();
    int soil = readSoilMoisture();
    float vbat = readBattery();

    if (isnan(t)) t = -999;
    Serial.printf("[Sensors] T=%.1fC Soil=%d%% Vbat=%.2fV\n", t, soil, vbat);

    // 2. Construir payload
    String payload = buildPayload(t, soil, vbat);

    // 3. Enviar per LoRa
    sendLoRa(payload);

    // 4. Deep sleep
    Serial.printf("[Sleep] %d minuts (boot #%d)\n", SLEEP_INTERVAL_MIN, bootCount);
    esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
    esp_deep_sleep_start();
}
