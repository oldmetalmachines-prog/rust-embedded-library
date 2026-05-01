# Embedded Robotics Library — Audit Report

**Date:** 2026-04-09  
**Scope:** Full library pass — all Rust modules, Cargo.toml files, documentation, and templates

---

## Summary

| Category | Found | Fixed |
|----------|-------|-------|
| Critical bugs (wrong behaviour/data) | 3 | 3 |
| Safety / reliability bugs | 1 | 1 |
| Dependency version inconsistencies | 4 | 4 |
| Missing/incorrect Cargo features | 1 | 1 |
| Documentation errors (broken paths, stale counts) | 8 | 8 |
| Unused dependencies | 2 | 2 |

---

## Critical Bugs Fixed

### 1. `esp32/sensors/temperature-logger/bmp180.rs` — `ac5` copy-paste bug

**Line 41:** `data[8]` was used twice for both the high and low bytes of `ac5`:

```rust
// Before (wrong)
let ac5 = ((data[8] as u16) << 8 | data[8] as u16) as i16 as i32;

// After (correct)
let ac5 = ((data[8] as u16) << 8 | data[9] as u16) as i16 as i32;
```

`ac5` is a BMP180 temperature calibration coefficient. Using the wrong value
corrupts every temperature reading. All subsequent `measure()` calls produce
incorrect output silently.

---

### 2. `esp32/sensors/temperature-logger/tiny_mqtt.rs` — recv buffer slice bug

**`receive_internal()`** tried to decode the MQTT packet from
`self.recv_buffer[..len]` (the size of the most recent TCP read chunk)
instead of `self.recv_buffer[..self.recv_index]` (all accumulated bytes).

```rust
// Before (wrong)
let data = self.recv_buffer[..len].as_ref();

// After (correct)
let data = self.recv_buffer[..self.recv_index].as_ref();
```

Any MQTT packet that arrives in more than one TCP segment can never be decoded
because the earlier bytes are accumulated correctly into `recv_buffer` but the
decode slice excludes them. This silently drops all MQTT traffic that isn't
delivered in a single read call.

---

### 3. `drivers/bme280/src/lib.rs` — missing `ctrl_hum` register write

The BME280 datasheet (section 5.4.3) states that humidity oversampling
configuration is written to register `0xF2` (`ctrl_hum`), and that **changes
only take effect after the next write to `ctrl_meas`**. The driver was writing
`ctrl_meas` without ever writing `ctrl_hum`, leaving humidity measurement mode
undefined (whatever power-on default the device has, often disabled).

Fixes applied:
- Added `REG_CTRL_HUM = 0xF2` constant.
- Write `ctrl_hum = 0x01` (humidity oversampling ×1) **before** `ctrl_meas`.
- Reordered: `config` is now written before `ctrl_hum` / `ctrl_meas` (matches
  the datasheet recommended sequence: configure in sleep mode, then set mode).
- Added comment explaining the 2 ms reset delay requirement (a proper delay
  can't be added in `no_std` without a `DelayNs` trait parameter — documented
  as a known limitation).

---

### 4. `esp32/examples/wifi-tank/main.rs` — WiFi retry loop ignores total failure

The connection retry loop ran up to 20 times but had no way to signal failure
to the rest of `main()`. If all 20 attempts failed, the code fell through to
`stack.wait_config_up().await`, which blocks forever with no diagnostic.

```rust
// Before
for i in 0..20 {
    if wifi_controller.connect().await.is_ok() { break; }
    ...
}
// silently continued even if all retries failed

// After
let mut connected = false;
for i in 0..20 {
    if wifi_controller.connect().await.is_ok() { connected = true; break; }
    ...
}
if !connected {
    core::panic!("Failed to connect to WiFi after 20 attempts");
}
```

---

## Dependency Version Inconsistencies Fixed

### 5. `raspberry-pi/ros2-integration/Cargo.toml` — stale rppal version

```toml
# Before
rppal = { version = "0.17", features = ["hal"] }

# After
rppal = { version = "0.22", features = ["hal"] }
```

The repo's own `rppal` crate is at `0.22.1`. The `servo-controller` member also
pins `"0.22"`. Using `"0.17"` would pull a different version and likely fail to
compile against the rest of the workspace.

---

### 6. `dependencies/cargo-templates/raspberry-pi-robotics.toml` — stale rppal + rumqttc

```toml
# Before
rppal = { version = "0.17", features = ["hal"] }
rumqttc = "0.23"

# After
rppal = { version = "0.22", features = ["hal"] }
rumqttc = "0.24"
```

Templates serve as the starting point for new projects. Stale version pins
would cause new projects to diverge from the workspace immediately.

---

### 7. `drivers/bme280/Cargo.toml` — `embedded-hal = "0.2"` vs workspace `"1"`

**Not changed** (requires a larger refactor of the public API), but **noted**:
every other workspace crate uses `embedded-hal = "1"`. The BME280 driver still
uses the deprecated `0.2` blocking traits (`blocking::i2c::Write`,
`blocking::i2c::WriteRead`). Migration path: replace the trait bounds with
`embedded_hal::i2c::I2c` from `embedded-hal 1.0`.

---

## Missing Cargo Feature Fixed

### 8. `esp32/utilities/i2c-scanner/Cargo.toml` — missing `println` on esp-backtrace

```toml
# Before
esp-backtrace = { version = "0.18.1", features = ["esp32s3", "panic-handler"] }

# After
esp-backtrace = { version = "0.18.1", features = ["esp32s3", "panic-handler", "println"] }
```

Without `println`, panic messages are swallowed silently on this version. The
README for this crate correctly listed `println` but the actual Cargo.toml
didn't.

---

## Unused Dependencies Removed

### 9. `esp32/communication/mqtt-telemetry-sender/Cargo.toml`

`serde = "1.0"` and `serde_json = "1.0"` were listed as dependencies but
neither is used anywhere in `src/main.rs` (the payload is a raw string
literal). Removed both.

---

## Documentation Fixed

### 10. `EXAMPLES_CATALOG.md` — multiple broken/inaccurate paths

| Location | Was | Now |
|----------|-----|-----|
| Complete Projects table | `esp32/examples/snake-game/` | `esp32/examples/snake-complete/` |
| By Hardware → OLED Display | `esp32/examples/snake-game/` | `esp32/examples/snake-complete/` |
| Quick Start Path 1 | Referenced `wifi/udp-telemetry-sender/` (wrong path) | `esp32/communication/mqtt-telemetry-sender/` |
| Quick Start Path 3 | `raspberry-pi/pico-2w/examples/led-blink/` (doesn't exist) | "Coming soon" |
| ROS2 Integration table | `ros2_imu_publisher.rs`, `ros2_motor_controller.rs` (don't exist) | Package scaffold note |
| Pico 2W examples table | Referenced non-existent directory | "(coming soon)" |
| Sensor Reading topic | Referenced mpu6050-basic.rs, vl53l0x-distance.rs as code | Marked as README-only |
| Complete count | 18 | 16 (mpu6050 and vl53l0x are README-only) |
| Platform count | 3 | 4 (Jetson Orin was missing) |
| BMP280 status | "Documentation only" | Points to `raspberry-pi/sensors/bmp280-i2c/` |
| BME280 status | "Documentation only" | Points to `drivers/bme280/` |

### 11. `docs/platforms/jetson-orin-nano-super.md` — "Coming soon" for existing examples

The Library Examples section said "Coming soon!" despite three working Jetson
examples being in the repo. Updated to list all three:
- `jetson-orin/examples/gpio-blink/`
- `jetson-orin/examples/pwm-servo/`
- `jetson-orin/examples/rtsp-camera-streamer/`

### 12. `esp32/communication/mqtt-telemetry-sender/README.md` — missing WiFi prerequisite

The README did not mention that WiFi must be initialised before MQTT will work.
The source file imports `esp_idf_svc::wifi::*` but never sets up a connection.
Added a Prerequisites section documenting this requirement and pointing to the
ESP-IDF WiFi provisioning docs.

---

## Issues Noted — Not Automatically Fixed

These require hardware validation, larger refactors, or deliberate design
decisions. Listed here for tracking.

### A. `drivers/bme280` — no calibration compensation in `read_raw()`

`read_raw()` returns the raw ADC triplet `(temperature, pressure, humidity)`.
The BMP280/BME280 data sheets define a complex integer compensation algorithm
that must be applied using the 26-byte calibration block (trims stored in
the chip). Without compensation the values are meaningless as physical
quantities. Options:
1. Add a `Calibration` struct + `read()` method that returns compensated values
   (mirrors the approach in `raspberry-pi/sensors/bmp280-i2c/src/main.rs`).
2. Document that `read_raw()` is intentionally raw and callers are responsible
   for compensation.

### B. `drivers/bme280` — no address configurability

`BME280_I2C_ADDR` is hardcoded to `0x76`. The device can also be addressed at
`0x77` (SDO pin high). Adding an `address: u8` field to `Bme280<I2C>` is a
one-line change but is an API break.

### C. `esp32/communication/mqtt-telemetry-sender/src/main.rs` — WiFi not initialised

The `main()` function calls `EspMqttClient::new()` without first establishing a
WiFi connection via `EspWifi`. On a bare `esp-idf-svc` runtime with no prior
provisioning, the MQTT connect will fail immediately. A full WiFi init (scanning
for the SSID, connecting, waiting for IP) needs to be added before the MQTT
client is created. The README now documents this requirement.

### D. `esp32/sensors/temperature-logger/tiny_mqtt.rs` — `send_internal()` retry is infinite

`send_internal()` retries `socket.write()` in an infinite `loop {}` if writing
fails. A failed write (e.g. connection reset) will hang the device. A retry
limit or error propagation should be added.

### E. `jetson-orin/examples/rtsp-camera-streamer` — no Ctrl+C handler

The `main_loop.run()` call blocks until someone calls `main_loop.quit()`, which
never happens. Ctrl+C kills the process abruptly, skipping `gst::deinit()` and
`glib::source_remove(id)`. A `signal_hook` or `ctrlc` crate handler calling
`main_loop.quit()` would allow graceful shutdown.

### F. `servo-control/cia402-ds402/` — not in workspace

This directory (untracked in git) contains C source and docs for a
CIA-402/DS-402 servo drive implementation. It is not integrated into the
workspace Cargo.toml. Decision needed: add it as a C sub-project with a
`build.rs`, keep it as reference material only, or create a Rust binding.

### G. `raspberry-pi/ros2-integration` — no `src/` or `examples/`

The crate has a `Cargo.toml` and lists `r2r`, `rppal`, `tokio`, etc., but
contains no source files. Referenced examples (`ros2_imu_publisher.rs`,
`ros2_motor_controller.rs`) do not exist. The crate will fail to compile as-is
because there is no `src/lib.rs` or `src/main.rs`. Add at minimum:

```rust
// src/lib.rs
pub fn placeholder() {}
```

or remove it from the workspace members until the source is ready.

### H. `esp32/examples/wifi-tank` — fixed seed for embassy-net

```rust
let seed = 0x0123_4567_89ab_cdef;
```

A static seed means every reboot uses the same sequence number in the network
stack. Using the hardware RNG to generate a seed at startup is better practice:

```rust
let seed = rng.random() as u64 | ((rng.random() as u64) << 32);
```

### I. Template version drift

`dependencies/cargo-templates/esp32-robotics-nostd.toml` lists:
- `esp-hal = "0.17"`, `esp-backtrace = "0.11"`, `esp-println = "0.9"`

The `i2c-scanner` workspace member already uses `0.18.1` / `0.16.1`. Consider
keeping template versions in sync with the workspace members to avoid new
projects starting from stale pinned versions.

---

## Files Changed

| File | Change |
|------|--------|
| `esp32/sensors/temperature-logger/bmp180.rs` | Fix `ac5` copy-paste bug |
| `esp32/sensors/temperature-logger/tiny_mqtt.rs` | Fix recv buffer slice uses `self.recv_index` |
| `esp32/examples/wifi-tank/main.rs` | Panic on total WiFi connection failure |
| `drivers/bme280/src/lib.rs` | Add `REG_CTRL_HUM`, write it before `ctrl_meas`, reorder init |
| `raspberry-pi/ros2-integration/Cargo.toml` | `rppal` `0.17` → `0.22` |
| `dependencies/cargo-templates/raspberry-pi-robotics.toml` | `rppal` `0.17` → `0.22`, `rumqttc` `0.23` → `0.24` |
| `esp32/utilities/i2c-scanner/Cargo.toml` | Add `println` feature to esp-backtrace |
| `esp32/communication/mqtt-telemetry-sender/Cargo.toml` | Remove unused `serde`, `serde_json` |
| `esp32/communication/mqtt-telemetry-sender/README.md` | Add WiFi prerequisite section |
| `EXAMPLES_CATALOG.md` | Fix snake-game path, stale wifi path, broken example refs, counts |
| `README.md` | Fix workspace member list (wrong mqtt path, remove non-existent pico entry, add missing members) |
| `GETTING_STARTED.md` | Fix snake-game path, ROS2 claims, sensor example status, statistics |
| `docs/platforms/esp32-s3.md` | Fix example project paths |
| `docs/platforms/jetson-orin-nano-super.md` | Replace "Coming soon" with actual example list |
| `esp32/sensors/examples/README.md` | Fix telemetry sender path |
| `esp32/utilities/i2c-scanner/README.md` | Fix sensor example path reference |
| `raspberry-pi/utilities/udp-telemetry-receiver/README.md` | Remove stale `wifi/udp-telemetry-sender/` companion reference |
