# MQTT Telemetry Sender

ESP32 project to send telemetry to Sigma rack MQTT broker.

## Configuration

Set at build time via environment variables or `sdkconfig`:

| Variable | Description | Default |
|----------|-------------|---------|
| `MQTT_USER` | MQTT broker username | (empty) |
| `MQTT_PASS` | MQTT broker password | (empty) |

The broker address is hardcoded to `mqtt://192.168.50.1:1883`. Change the
`broker` constant in `src/main.rs` for a different host.

## Prerequisites

This crate targets `esp-idf-svc` (the ESP-IDF std runtime). You must configure
WiFi connectivity separately before MQTT will work. The recommended approach is
to add `EspWifi` setup in `main()` before calling `EspMqttClient::new()`, or
provision WiFi via the ESP-IDF NVS/WiFi provisioning stack. See the ESP-IDF
documentation for `esp_wifi_init` / `esp_wifi_connect`.

## Feature Flags

- `sigma-rack`: Enables additional sigma-rack specific telemetry paths
