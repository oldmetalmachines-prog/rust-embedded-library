# Examples Catalog

Complete index of all working examples in this library, organized by platform and function.

**Last Updated:** 2026-04-09

---

## 🎯 Quick Start Paths

### Path 1: ESP32 Beginner (Start Here!)
1. `esp32/utilities/i2c-scanner/` - Verify I2C wiring works
2. `esp32/sensors/examples/` - MPU6050 README (code pending)
3. `esp32/communication/mqtt-telemetry-sender/` - Send data wirelessly

### Path 2: Raspberry Pi Beginner
1. `raspberry-pi/gpio/rppal-examples/gpio_blinkled.rs` - Blink an LED
2. `raspberry-pi/utilities/udp-telemetry-receiver/` - Receive ESP32 data
3. `raspberry-pi/ros2-integration/` - Connect to ROS2

### Path 3: Pico 2W Beginner
1. Coming soon: Pico 2W examples are planned (see `docs/platforms/pi-pico-2w.md` for setup)
2. Coming soon: GPIO sensor examples

---

## 📱 By Platform

### ESP32-S3 / ESP32-C3

#### 🔧 Utilities (Start with these!)
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| `esp32/utilities/i2c-scanner/` | Find I2C device addresses | ESP32, breadboard | ⭐ Beginner |

#### 📡 Communication
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| `esp32/communication/mqtt-telemetry-sender/` | Send telemetry via MQTT over WiFi | ESP32, WiFi network | ⭐⭐ Intermediate |

#### 📊 Sensors
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| `esp32/sensors/examples/` (README only) | MPU6050 IMU — code pending | ESP32, MPU6050, pull-ups | ⭐⭐ Intermediate |
| `esp32/sensors/examples/` (README only) | VL53L0X ToF distance — code pending | ESP32, VL53L0X | ⭐⭐ Intermediate |
| `esp32/sensors/temperature-logger/` | MQTT temperature logger | ESP32, BMP180, WiFi | ⭐⭐⭐ Advanced |

#### 🎮 Complete Projects
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| `esp32/examples/snake-complete/` | OLED snake game | ESP32, OLED, joystick | ⭐⭐⭐ Advanced |
| `esp32/examples/wifi-tank/` | WiFi controlled rover | ESP32, motors, driver | ⭐⭐⭐ Advanced |
| `esp32/examples/std-demo/` | WiFi + HTTP + LED | ESP32, LED screen | ⭐⭐⭐ Advanced |

---

### Raspberry Pi (Pi 5, Pi Zero 2W)

#### 🔧 Utilities
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| `raspberry-pi/utilities/udp-telemetry-receiver/` | Receive ESP32 telemetry | Pi, network | ⭐ Beginner |

#### 🔌 GPIO Examples (RPPAL)
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| `raspberry-pi/gpio/rppal-examples/gpio_blinkled.rs` | Blink LED | Pi, LED, resistor | ⭐ Beginner |
| `raspberry-pi/gpio/rppal-examples/gpio_status.rs` | Button input | Pi, button | ⭐ Beginner |
| `raspberry-pi/gpio/rppal-examples/pwm_blinkled.rs` | PWM LED fade | Pi, LED, resistor | ⭐⭐ Intermediate |
| `raspberry-pi/gpio/rppal-examples/pwm_servo.rs` | Control servo | Pi, servo motor | ⭐⭐ Intermediate |
| `raspberry-pi/gpio/servo-controller/` | Servo controller CLI (angle→pulse) | Pi, servo, external 5V | ⭐⭐ Intermediate |
| `raspberry-pi/gpio/rppal-examples/i2c_ds3231.rs` | I2C RTC clock | Pi, DS3231, pull-ups | ⭐⭐ Intermediate |
| `raspberry-pi/gpio/rppal-examples/spi_25aa1024.rs` | SPI EEPROM | Pi, 25AA1024 chip | ⭐⭐⭐ Advanced |
| `raspberry-pi/gpio/rppal-examples/uart_blocking_read.rs` | Serial communication | Pi, UART device | ⭐⭐ Intermediate |

#### 🤖 ROS2 Integration
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| `raspberry-pi/ros2-integration/` | ROS2 package scaffold (examples planned) | Pi, ROS2 Humble | ⭐⭐⭐ Advanced |

---

### Raspberry Pi Pico 2W

#### 💡 Basic Examples
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| (coming soon) | Blink onboard LED | Pico 2W, USB cable | ⭐ Beginner |

See `docs/platforms/pi-pico-2w.md` for toolchain setup and project templates.

---

### Jetson Orin Nano Super

#### 🔌 GPIO Examples
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| `jetson-orin/examples/gpio-blink/` | GPIO LED blink | Jetson, LED, resistor | ⭐ Beginner |

#### 🎥 Computer Vision
| Example | Purpose | Hardware Needed | Difficulty |
|---------|---------|-----------------|------------|
| `jetson-orin/examples/rtsp-camera-streamer/` | GStreamer RTSP camera server (USB + CSI) | Jetson, CSI/USB camera | ⭐⭐ Intermediate |
| `jetson-orin/examples/pwm-servo/` | Sysfs PWM servo (with MQTT telemetry) | Jetson, servo motor | ⭐⭐ Intermediate |

#### 🎥 Computer Vision (Coming Soon)
- Camera capture with opencv-rust
- CUDA-accelerated object detection
- ROS2 vision integration

---

## 🎓 By Learning Topic

### First Steps (Absolute Beginners)
1. **Blink LED** - `raspberry-pi/gpio/rppal-examples/gpio_blinkled.rs` (Pi) or Pico 2W examples (coming soon)
2. **I2C Scanner** - `esp32/utilities/i2c-scanner/` (ESP32)
3. **Read Button** - `raspberry-pi/gpio/rppal-examples/gpio_status.rs` (Pi)

### Sensor Reading
1. **I2C IMU** - `esp32/sensors/examples/` (MPU6050 README; code pending)
2. **I2C RTC** - `raspberry-pi/gpio/rppal-examples/i2c_ds3231.rs`
3. **Pressure/Temp** - `raspberry-pi/sensors/bmp280-i2c/`
4. **Distance Sensor** - `esp32/sensors/examples/` (VL53L0X README; code pending)

---

## 📚 By Hardware Component

### Sensors

#### IMU (Motion/Orientation)
- **MPU6050** (6-axis): `esp32/sensors/examples/` (README only, code pending)
- **BNO055** (9-axis): Documentation only

#### Distance
- **VL53L0X** (ToF laser): `esp32/sensors/examples/` (README only, code pending)
- **VL53L1X** (4m range): Documentation only

#### Environment
- **BMP180** (pressure/temp): `esp32/sensors/temperature-logger/`
- **BMP280**: `raspberry-pi/sensors/bmp280-i2c/` (working, with MQTT telemetry)
- **BME280** (humidity): `drivers/bme280/` (no_std driver library)

#### Time
- **DS3231** (RTC): `raspberry-pi/gpio/rppal-examples/i2c_ds3231.rs`

### Actuators

#### LEDs
- **Simple LED**: `raspberry-pi/gpio/rppal-examples/gpio_blinkled.rs`
- **PWM LED**: `raspberry-pi/gpio/rppal-examples/pwm_blinkled.rs`
- **OLED Display**: `esp32/examples/snake-complete/`

#### Motors
- **Servo**: `raspberry-pi/gpio/rppal-examples/pwm_servo.rs`
- **DC Motors**: `esp32/examples/wifi-tank/`

### Communication

#### Wireless
- **WiFi + MQTT**: `esp32/communication/mqtt-telemetry-sender/`
- **UDP receiver**: `raspberry-pi/utilities/udp-telemetry-receiver/`
- **MQTT over WiFi**: `esp32/sensors/temperature-logger/` (BMP180 temperature logger)

#### Wired
- **I2C**: Multiple sensor examples
- **SPI**: `raspberry-pi/gpio/rppal-examples/spi_25aa1024.rs`
- **UART**: `raspberry-pi/gpio/rppal-examples/uart_blocking_read.rs`

---

## 🏗️ By Project Complexity

### ⭐ Beginner (1-2 hours, <50 lines code)
- I2C Scanner
- LED Blink (Pi or Pico 2W)
- Button Input
- UDP Receiver (Pi)

### ⭐⭐ Intermediate (2-4 hours, 50-200 lines)
- MPU6050 IMU Reading
- VL53L0X Distance
- UDP Sender (ESP32)
- Servo Control
- I2C RTC

### ⭐⭐⭐ Advanced (4+ hours, 200+ lines)
- WiFi Tank Robot
- Snake Game
- Temperature Logger (MQTT)
- ROS2 Integration
- SPI EEPROM

---

## 🛠️ Template & Reference Documents

### Templates
- `docs/templates/EXAMPLE_CONTRACT_TEMPLATE.md` - Copy this for every new example

### Platform Profiles
- `docs/platforms/esp32-s3.md` - ESP32-S3 pin maps, toolchain, troubleshooting
- `docs/platforms/pi-pico-2w.md` - Pico 2W pin maps, WiFi setup, flashing

### Protocols
- `common/protocols/telemetry_v1.json` - Standard message format for device communication
- `common/protocols/README.md` - Implementation guide (Rust & Python)

### Algorithms
- `common/ALGORITHMS.md` - Robotics crates: Kalman filters, PID, pathfinding

### Cargo Templates
- `dependencies/cargo-templates/esp32-robotics-nostd.toml` - ESP32 no_std robotics
- `dependencies/cargo-templates/esp32-robotics-std.toml` - ESP32 with WiFi/MQTT
- `dependencies/cargo-templates/esp32p4-robotics.toml` - ESP32-P4 dual-core
- `dependencies/cargo-templates/raspberry-pi-robotics.toml` - Pi with ROS2

---

## 📦 Example Status

| Status | Count | Description |
|--------|-------|-------------|
| ✅ Complete | 16 | Full code + README following contract |
| 📝 Documented | 2 | README only, code pending (MPU6050, VL53L0X) |
| 🚧 Planned | 12 | On roadmap |

### ✅ Complete Examples (16)

**ESP32:**
1. I2C Scanner
2. UDP Telemetry Sender
3. Temperature Logger
4. Snake Game (`esp32/examples/snake-complete/`)
5. WiFi Tank
6. STD Demo

**Raspberry Pi:**
7. UDP Telemetry Receiver
8. GPIO LED Blink
9. GPIO Button
10. GPIO Multithreaded
11. PWM LED Fade
12. PWM Servo
13. I2C DS3231
14. SPI EEPROM
15. UART Blocking Read
16. BMP280 I2C Sensor

### 📝 README Only — Code Pending (2)

**ESP32:**
- MPU6050 Basic (README in `esp32/sensors/examples/`)
- VL53L0X Distance (README in `esp32/sensors/examples/`)

### 🚧 Planned Examples

**ESP32:**
- Motor driver (L298N, TB6612FNG)
- Brushless motor ESC
- Stepper motor
- GPS module
- Camera integration (ESP32-P4)

**Raspberry Pi:**
- GPIO interrupt examples
- Multi-sensor fusion
- Complete rover project

**Pico 2W:**
- External GPIO LED
- WiFi connection
- I2C sensors
- Button input

---

## 🔍 How to Find What You Need

### "I want to learn [X]"
1. Check **By Learning Topic** section above
2. Start with ⭐ Beginner examples
3. Follow the Quick Start Paths

### "I have [Hardware Component]"
1. Check **By Hardware Component** section
2. Look for your specific sensor/motor
3. Follow the example README

### "I want to build [Project]"
1. Check **Complete Projects** section
2. Review difficulty rating
3. Start with simpler examples first

### "I'm debugging [Problem]"
1. Check platform profile: `docs/platforms/`
2. Run I2C scanner if sensor issue
3. Check example's Troubleshooting section

---

## 📊 Statistics

- **Total Examples:** 16 complete (2 README-only)
- **Platforms:** 4 (ESP32, Raspberry Pi, Pico 2W, Jetson Orin)
- **Communication Protocols:** I2C, SPI, UART, WiFi, UDP, MQTT
- **Sensors Supported:** 7+ types
- **Lines of Example Code:** ~3000+
- **Documentation Pages:** 25+

---

## 🎯 Recommended Learning Order

### Week 1: Basics
1. Blink LED on your platform
2. Run I2C scanner (if using ESP32)
3. Read one sensor successfully

### Week 2: Communication
4. Send data via UDP (ESP32 → Pi)
5. Receive and display data (Pi)
6. Log to file

### Week 3: Integration
7. Add second sensor
8. Multi-device communication
9. Simple autonomous behavior

### Week 4: Advanced
10. ROS2 integration (if using Pi)
11. Complete rover project
12. Add your own example to library!

---

## 🤝 Contributing Your Examples

After building something that works:
```bash
# 1. Copy the template
cp docs/templates/EXAMPLE_CONTRACT_TEMPLATE.md your-project/README.md

# 2. Fill in all sections
# - Purpose, wiring, code, troubleshooting

# 3. Add to library
git add your-project/
git commit -m "Add [name] example"
git push

# 4. Update this catalog!
```

---

## 📝 Notes

- All examples follow the Example Contract template
- Wiring diagrams use ASCII art for clarity
- Troubleshooting sections include common issues
- Code is tested and working (marked with ✅)
- See `GETTING_STARTED.md` for detailed setup

---

**Need help finding something? This catalog is your map!**  
**Start with Quick Start Paths, then explore by topic or hardware.**

