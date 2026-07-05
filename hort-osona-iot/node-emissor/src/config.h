/**
 * config.h — Pins i configuració del TTGO LoRa32 v2.1
 *
 * Adaptat per a l'hort d'Osona:
 * - BME280 (I2C) per temperatura, humitat, pressió
 * - OLED integrat per feedback visual
 * - Sensor capacitiU del sòl (analògic, GPIO36)
 * - Lectura bateria amb divisor de tensió (GPIO35)
 * - LoRa SX1276 integrat a 868 MHz
 */

#ifndef CONFIG_H
#define CONFIG_H

// ──────────── I2C (BME280 + OLED comparteixen bus) ────────────
#define I2C_SDA       21
#define I2C_SCL       22
#define BME280_I2C_ADDR  0x76  // CSB lligat a VCC

// ──────────── OLED SSD1306 (integrat) ────────────
#define OLED_SDA       I2C_SDA
#define OLED_SCL       I2C_SCL
#define OLED_ADDR      0x3C
#define OLED_RST       16  // RST del OLED al TTGO
#define SCREEN_WIDTH   128
#define SCREEN_HEIGHT  64

// ──────────── LoRa SX1276 (integrat al TTGO) ────────────
#define LORA_SCK       5
#define LORA_MISO      19
#define LORA_MOSI      27
#define LORA_CS        18
#define LORA_RST       23
#define LORA_DIO0      26
#define LORA_FREQUENCY 868.0  // MHz (Europa)
#define LORA_TX_POWER  17     // dBm
#define LORA_SPREADING_FACTOR 10
#define LORA_BANDWIDTH 125    // kHz

// ──────────── Sensors analògics ────────────
#define SOIL_SENSOR_PIN   36  // VP (ADC1_CH0)
#define BATTERY_PIN       35  // ADC1_CH7 (amb divisor 100k/100k)
#define SOIL_SAMPLES      16  // Nombre de mostres per fer mitjana
#define BATTERY_DIVIDER_RATIO 2.0  // 100k/100k = 0.5, Vbat = Vadc * 2

// ──────────── Sleep ────────────
#define SLEEP_INTERVAL_MIN  15  // Minuts entre lectures
#define uS_TO_S_FACTOR      1000000ULL
#define TIME_TO_SLEEP       (SLEEP_INTERVAL_MIN * 60)

// ──────────── OLED ────────────
#define OLED_ENABLED_TIME_S  5  // Segons que l'OLED queda encès

#endif  // CONFIG_H
