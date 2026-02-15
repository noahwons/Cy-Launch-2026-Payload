# =========================================================================================
# Developer: Noah Wons
# Contact: wons123@iastate.edu
# Date: 2/14
# =========================================================================================


# Init. commands:
# sudo apt-get update
# sudo apt-get install -y python3-pip i2c-tools
# sudo raspi-config   # enable I2C, reboot

# sudo pip3 install adafruit-blinka adafruit-circuitpython-bno055
# i2cdetect -y 1      # you should see 28 (or 29)

# python3 bno055_test.py



"""
Raspberry Pi 3B + Adafruit Absolute Orientation 9-DOF IMU (BNO055) test script.

Reads:
- Euler angles (heading/roll/pitch)
- Quaternion
- Accel / Gyro / Mag
- Linear accel / Gravity
- Temperature + calibration status

Wiring (I2C):
- VIN -> 3.3V (recommended) or 5V (check your breakout)
- GND -> GND
- SDA -> SDA (GPIO2, pin 3)
- SCL -> SCL (GPIO3, pin 5)

Enable I2C:
sudo raspi-config  # Interface Options -> I2C -> Enable
"""

import time
import sys

try:
    import board
    import busio
    from adafruit_bno055 import BNO055_I2C
except ImportError as e:
    print("Missing libraries. Install with:")
    print("  sudo pip3 install adafruit-blinka adafruit-circuitpython-bno055")
    sys.exit(1)


def fmt_tuple(t, precision=2):
    if t is None:
        return "None"
    return "(" + ", ".join(f"{x:.{precision}f}" if x is not None else "None" for x in t) + ")"


def main():
    # I2C init (Pi uses /dev/i2c-1)
    i2c = busio.I2C(board.SCL, board.SDA)

    # Some breakouts allow addr 0x28 or 0x29 depending on ADR pin; library auto-tries 0x28.
    try:
        sensor = BNO055_I2C(i2c)
    except ValueError:
        print("Could not find BNO055 at default I2C address (0x28).")
        print("If your ADR pin is set, it may be 0x29. Try wiring ADR differently or use an I2C scanner.")
        sys.exit(1)

    print("BNO055 detected.")
    time.sleep(1)

    # Optional: show basic IDs (may be None on some boards/firmware)
    try:
        print(f"Chip ID: {sensor.chip_id}")
    except Exception:
        pass

    print("\nReading sensor... Press Ctrl+C to stop.\n")

    # Print header every N lines
    header_every = 10
    line = 0

    try:
        while True:
            # Orientation
            euler = sensor.euler            # (heading, roll, pitch) in degrees
            quat = sensor.quaternion        # (w, x, y, z)

            # Motion
            accel = sensor.acceleration     # m/s^2
            gyro = sensor.gyro              # rad/s
            mag = sensor.magnetic           # microtesla

            # Fusion outputs
            lin_accel = sensor.linear_acceleration  # m/s^2
            gravity = sensor.gravity                # m/s^2

            temp = sensor.temperature

            # Calibration status: (sys, gyro, accel, mag) each 0-3
            cal = sensor.calibration_status

            if line % header_every == 0:
                print("time    euler(h,r,p)deg           quat(w,x,y,z)              "
                      "accel(m/s^2)           gyro(rad/s)            mag(uT)        "
                      "lin_accel(m/s^2)       grav(m/s^2)          tempC  cal(s,g,a,m)")
            line += 1

            ts = time.strftime("%H:%M:%S")
            print(
                f"{ts}  "
                f"{fmt_tuple(euler, 1):<26} "
                f"{fmt_tuple(quat, 3):<28} "
                f"{fmt_tuple(accel, 2):<22} "
                f"{fmt_tuple(gyro, 3):<22} "
                f"{fmt_tuple(mag, 1):<14} "
                f"{fmt_tuple(lin_accel, 2):<20} "
                f"{fmt_tuple(gravity, 2):<20} "
                f"{str(temp):<5}  "
                f"{cal}"
            )

            time.sleep(0.2)

    except KeyboardInterrupt:
        print("\nStopped.")
        return


if __name__ == "__main__":
    main()
