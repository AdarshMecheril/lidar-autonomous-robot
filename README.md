# LiDAR Autonomous Robot

This repository contains a LiDAR-based autonomous robot system.
The robot uses an RPLiDAR sensor for obstacle detection and an ESP32 for motor and steering control.
A Python application processes LiDAR data in real time and sends movement commands to the ESP32 through serial communication.

---

## Repository Structure

lidar-autonomous-robot/
├── main.py
├── requirements.txt
├── README.md
├── LICENSE
├── images/
└── esp32/
└── esp32_motor_control.ino


---

## Hardware Required

- RPLiDAR (A1 / A2)
- ESP32
- DC motor with motor driver (L298N / L293D)
- Steering servo motor
- Power supply for motors
- USB cables

---

## Software Requirements

- Python 3.8 or later
- Arduino IDE (for ESP32)
- Git (optional)

Python libraries:
- numpy
- pyqtgraph
- PySide6
- pyserial
- rplidar

---

## Connections

### ESP32 Motor Driver
- ENA → ESP32 GPIO 25
- IN1 → ESP32 GPIO 26
- IN2 → ESP32 GPIO 27

### Steering Servo
- Signal → ESP32 GPIO 13
- VCC → External 5V
- GND → Common ground

### RPLiDAR
- Connect via USB to PC / Raspberry Pi

Ensure **all grounds are common**.

---

## ESP32 Firmware Installation

1. Open Arduino IDE  
2. Install ESP32 board support  
3. Install library:
   - ESP32Servo
4. Open:
5. Select correct board and COM port  
6. Upload firmware to ESP32  

---

## Python Application Installation

### Open Terminal / CMD

Navigate to project folder:

Install dependencies:

---

## Serial Port Configuration

Edit `main.py` if required:

```python
LIDAR_PORT = "/dev/ttyUSB0"
ESP32_PORT = "/dev/ttyUSB1"
COM3
COM4

Start the LiDAR navigation program:
python main.py

Start the LiDAR navigation program:
| Command | Action        |
| ------- | ------------- |
| f       | Move forward  |
| b       | Move backward |
| l       | Turn left     |
| r       | Turn right    |
| s       | Stop          |

Commands are sent automatically based on obstacle detection.
Operation Logic



If path ahead is clear → move forward

If obstacle detected in front → steering decision based on left/right clearance

If all sides blocked → reverse and turn

Stop command centers steering and halts motors
Notes

Designed for basic obstacle avoidance

Serial communication is one-way (PC → ESP32)

Speed and angle values can be adjusted in code

Tested with USB serial connections







