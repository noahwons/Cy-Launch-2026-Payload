Here’s a clean, **professional README.md** you can drop straight into your CyLaunch repo. I wrote it like a real flight-hardware project (NASA SLI-style documentation tone since that fits your payload work).

---

# 🚀 CyLaunch 2026 Payload Device

## Overview

The **CyLaunch 2026 Payload Device** is a hybrid avionics and telemetry system designed for high-reliability data collection and motor actuation during rocket flight operations. The payload integrates a Raspberry Pi–based processing unit with Feather-class microcontrollers and LoRa radios to enable sensor acquisition, motor control, and long-range wireless communication.

This system supports:

* Real-time telemetry transmission
* Absolute orientation sensing
* Remote command capability
* Multi-motor actuation
* Redundant communication pathways

---

## System Architecture

### Primary Components

* **Raspberry Pi 3B**

  * Main processing computer
  * Handles telemetry, high-level logic, and radio communication

* **Adafruit Feather M4 Express**

  * Real-time microcontroller
  * Responsible for precise timing and hardware control tasks

* **3 × Bigfoot25 Motors**

  * Controlled via ESC/PWM outputs
  * Used for mechanical deployment or actuation mechanisms

* **2 × Adafruit RFM9x LoRa FeatherWing (433 MHz)**

  * Radio #1 mounted on Feather M4
  * Radio #2 connected to Raspberry Pi
  * Enables bidirectional payload communication

* **Adafruit Absolute Orientation 9-DOF IMU (BNO055)**

  * Provides:

    * Orientation (Euler/quaternion)
    * Acceleration
    * Gyroscope data
    * Magnetometer readings

---

## Hardware Layout

### Raspberry Pi Connections

* SPI → RFM9x FeatherWing
* I2C → BNO055 IMU
* Power distribution bus

### Feather M4 Connections

* RFM9x FeatherWing (stacked)
* PWM outputs → Motor ESCs

### Communication Flow

```
IMU → Raspberry Pi → LoRa (RFM9x)
                 ↕
         Feather M4 + RFM9x
                 ↓
              Motors
```

The Pi and Feather communicate over LoRa to allow command relay and redundancy.

---

## Features

* 📡 Long-range LoRa telemetry (433 MHz)
* 🧭 Absolute orientation tracking
* ⚙️ Independent microcontroller for deterministic control
* 🔁 Dual-radio architecture for redundancy
* 🚀 Designed for CyLaunch/NASA SLI payload constraints

---

## Software Stack

### Raspberry Pi

* Python 3
* CircuitPython libraries
* SPI + I2C interfaces
* Adafruit RFM9x Library
* Adafruit BNO055 Library

### Feather M4

* CircuitPython firmware
* PWM motor control scripts
* LoRa communication handler

---

## Dependencies

Install on Raspberry Pi:

```bash
pip install adafruit-circuitpython-rfm9x
pip install adafruit-circuitpython-bno055
pip install adafruit-blinka
```

Enable interfaces:

```bash
sudo raspi-config
# Enable SPI
# Enable I2C
```

---

## Wiring Summary

### IMU (BNO055 → Raspberry Pi)

* VIN → 3.3V
* GND → GND
* SDA → SDA
* SCL → SCL

### RFM9x (Pi Side)

* SCK → SPI SCLK
* MOSI → SPI MOSI
* MISO → SPI MISO
* CS → GPIO8 (example)
* RST → GPIO25 (example)
* G0 (IRQ) → GPIO24

### Feather M4 + FeatherWing

* FeatherWing stacks directly onto Feather M4
* No external wiring required for radio

### Motors

* ESC Signal → Feather M4 PWM pin
* External power supply required
* Common ground between ESCs and Feather

---

## Power Requirements

⚠️ **Important**

* Motors must use a dedicated power source.
* Do NOT power motors from Raspberry Pi or Feather 5V rail.
* All grounds must be shared across systems.

Recommended architecture:

```
Battery → ESC Power
        → 5V Regulator → Raspberry Pi
        → Feather M4 USB/BAT input
```

---

## Repository Structure

```
TODO
```

---

## Flight Safety Notes

* Verify Li-Ion battery storage compliance.
* Secure all connectors against vibration.
* Use strain relief for SPI/I2C wiring.
* Confirm LoRa frequencies comply with launch regulations.

---

## Future Improvements

* Hardware watchdog between Pi and Feather
* Redundant IMU integration
* Custom PCB replacing breadboard prototype
* CAN/UART backup communication channel

---

## Contributors

CyLaunch 2026 Payload Team
* Noah Wons

