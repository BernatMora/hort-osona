/**
 * main.cpp — Node emissor LoRa per a l'hort d'Osona
 *
 * Cicle:
 *   1. Desperta del deep sleep
 *   2. Llegeix BME280 (T, H, P)
 *   3. Llegeix sensor humitat del sòl (capacitiu, GPIO36)
 *   4. Llegeix tensió bateria (divisor 100k/100k, GPIO35)
 *   5. Mostra dades a l'OLED 5 segons
 *   6. Envia payload CSV per LoRa 868 MHz
 *   7. Deep sleep 15 minuts
 *
 * Hardware: TTGO LoRa32 v2.1 + BME280 + sensor capacitiu v1.2
 */

#include <Arduino.h>
#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <U8g2lib.h>
#include <RadioLib.h>
#include "config.h"

// ──────────── Objectes globals ────────────
Adafruit_BME280 bme;
U8G2_SSD1306_128X64_NONAME_F_HW_I2C oled(U8G2_R0, OLED_RST, OLED_SCL, OLED_SDA);
SX1276 radio = new Module(LORA_CS, LORA_DIO0, LORA_RST, LORA_DIO1 ?? -1);

// ──────────── Variables globals ────────────
RTC_DATA_ATTR int bootCount = 0;  // Persisteix entre deep sleeps

// ──────────── Funcions auxiliars ────────────

/**
 * Llegeix el sensor d'humitat del sòl amb N mostres i retorna %.
 * Assumeix mapeig lineal: 0% (sec) = 4095, 100% (moll) = ~1500 (calibrar).
 */
int readSoilMoisture() {
    long sum = 0;
    for (int i = 0; i < SOIL_SAMPLES; i++) {
        sum += analogRead(SOIL_SENSOR_PIN);
        delay(5);
    }
    int raw = sum / SOIL_SAMPLES;

    // Mapeig a % (calibrar segons el sensor concret)
    // Ajusta aquests valors un cop tinguis el sensor a la mà:
    // - Valor en sec: ~3500
    // - Valor en aigua: ~1500
    const int RAW_DRY = 3500;
    const int RAW_WET = 1500;
    int pct = map(raw, RAW_DRY, RAW_WET, 0, 100);
    return constrain(pct, 0, 100);
}

/**
 * Llegeix tensió de la bateria amb divisor de tensió.
 */
float readBattery() {
    int raw = analogRead(BATTERY_PIN);
    // ESP32 ADC: 0-3.3V sobre 12 bits (0-4095)
    float v_adc = (raw / 4095.0) * 3.3;
    float v_bat = v_adc * BATTERY_DIVIDER_RATIO;
    return v_bat;
}

/**
 * Construeix el payload CSV.
 */
String buildPayload(float t, float h, float p, int soil, float vbat) {
    char buf[80];
    snprintf(buf, sizeof(buf), "T:%.1f,H:%.1f,P:%.1f,S:%d,BAT:%.2f", t, h, p, soil, vbat);
    return String(buf);
}

/**
 * Mostra les dades a l'OLED durant OLED_ENABLED_TIME_S segons.
 */
void showOnOLED(float t, float h, float p, int soil, float vbat) {
    oled.clearBuffer();
    oled.setFont(u8g2_font_6x10_tr);
    oled.setCursor(0, 12);
    oled.printf("Hort Osona #%d", bootCount);
    oled.setCursor(0, 26);
    oled.printf("T:%.1fC H:%.1f%%", t, h);
    oled.setCursor(0, 38);
    oled.printf("P:%.0f hPa", p);
    oled.setCursor(0, 50);
    oled.printf("Sol:%d%% Bat:%.2fV", soil, vbat);
    oled.sendBuffer();

    delay(OLED_ENABLED_TIME_S * 1000);
    oled.setPowerSave(1);  // Apaga OLED
}

/**
 * Envia payload per LoRa.
 */
bool sendLoRa(const String& payload) {
    int state = radio.transmit(payload.c_str());
    if (state == RADIOLIB_ERR_NONE) {
        Serial.printf("[LoRa] TX OK: %s\n", payload.c_str());
        return true;
    } else {
        Serial.printf("[LoRa] TX FAIL: %d\n", state);
        return false;
    }
}

// ──────────── SETUP ────────────
void setup() {
    Serial.begin(115200);
    delay(100);

    bootCount++;
    Serial.printf("\n=== Boot #%d ===\n", bootCount);

    // I2C
    Wire.begin(I2C_SDA, I2C_SCL);

    // BME280
    if (!bme.begin(BME280_I2C_ADDR)) {
        Serial.println("[BME280] ERROR: no trobat!");
        // Continuem igual — BME280 és opcional
    } else {
        Serial.println("[BME280] OK");
    }

    // OLED
    oled.begin();
    oled.setPowerSave(0);
    oled.clearBuffer();

    // LoRa
    Serial.print("[LoRa] Inicialitzant... ");
    int state = radio.begin(LORA_FREQUENCY, LORA_BANDWIDTH, LORA_SPREADING_FACTOR,
                             5, LORA_TX_POWER, 8, 1.6, false);
    if (state != RADIOLIB_ERR_NONE) {
        Serial.printf("FAIL (%d)\n", state);
    } else {
        Serial.println("OK");
    }
}

// ──────────── LOOP ────────────
void loop() {
    // 1. Llegir sensors
    float t = bme.readTemperature();
    float h = bme.readHumidity();
    float p = bme.readPressure();
    int soil = readSoilMoisture();
    float vbat = readBattery();

    Serial.printf("[Sensors] T=%.1f H=%.1f P=%.1f Soil=%d%% Vbat=%.2f\n",
                  t, h, p, soil, vbat);

    // 2. Mostrar a OLED
    showOnOLED(t, h, p, soil, vbat);

    // 3. Enviar per LoRa
    String payload = buildPayload(t, h, p, soil, vbat);
    sendLoRa(payload);

    // 4. Deep sleep
    Serial.printf("[Sleep] %d minuts\n", SLEEP_INTERVAL_MIN);
    esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);
    esp_deep_sleep_start();
}
