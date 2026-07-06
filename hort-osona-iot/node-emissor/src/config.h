/**
 * config.h — Configuració per al node emissor amb ESP32-S3 + SX1262
 *
 * Adaptat per a l'hort d'Osona:
 * - ESP32-S3 (Waveshare o similar) amb LoRa SX1262 integrat
 * - Sensor humitat del sòl capacitiu (analògic, GPIO 4)
 * - Sensor temperatura DS18B20 amb sonda d'acer (1-Wire, GPIO 5)
 * - Lectura bateria amb divisor de tensió (GPIO 1, ADC)
 * - LoRa SX1262 a 868 MHz (banda UE)
 * - Deep sleep per estalvi de bateria
 *
 * NOTA: Aquest codi assumeix que el SX1262 esta connectat per SPI.
 *       Ajusta els pins segons el teu hardware especific.
 */

#ifndef CONFIG_H
#define CONFIG_H

// ──────────── DS18B20 (sensor temperatura, 1-Wire) ────────────
#define ONE_WIRE_PIN      5    // GPIO 5 (1-Wire data)
#define DS18B20_RESOLUTION 12   // 9-12 bits (12 = 0.0625°C, ~750ms conversio)

// ──────────── Sensor humitat del sol (analogic) ────────────
#define SOIL_SENSOR_PIN   4    // GPIO 4 (ADC1_CH3)
#define SOIL_SAMPLES      16   // Nombre de mostres per fer mitjana

// ──────────── Lectura bateria ────────────
#define BATTERY_PIN       1    // GPIO 1 (ADC1_CH0)
#define BATTERY_DIVIDER_RATIO 2.0  // Divisor 100k/100k

// ──────────── LoRa SX1262 (SPI) ────────────
// Ajusta aquests pins segons el teu hardware especific
#define LORA_SCK          12   // GPIO 12
#define LORA_MISO         13   // GPIO 13
#define LORA_MOSI         11   // GPIO 11
#define LORA_CS           10   // GPIO 10 (NSS)
#define LORA_RST          9    // GPIO 9
#define LORA_DIO1         8    // GPIO 8 (interrupt)
#define LORA_BUSY         7    // GPIO 7 (busy signal)
#define LORA_FREQUENCY    868.0  // MHz (Europa)
#define LORA_TX_POWER     14     // dBm (max legal UE: 14 dBm)
#define LORA_SPREADING_FACTOR 10
#define LORA_BANDWIDTH    125    // kHz

// ──────────── Sleep ────────────
#define SLEEP_INTERVAL_MIN  15  // Minuts entre lectures
#define uS_TO_S_FACTOR      1000000ULL
#define TIME_TO_SLEEP       (SLEEP_INTERVAL_MIN * 60)

// ──────────── Identificacio del node ────────────
#define NODE_ID            "hort-1"  // Identificador unic del node
#define NODE_LOCATION      "osona"   // Ubicacio (pot ser l'ID del hort)

#endif  // CONFIG_H
