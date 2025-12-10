# PiObs - Patient Vitals Monitor for Raspberry Pi

Python software for Raspberry Pi OS to receive and display vitals from pysender via a locally generated Access Point on Raspberry Pi.

## Features

- Fullscreen vitals display (Blood Pressure, SpO2, Heart Rate, Temperature, Respiratory Rate)
- Automatic Wi-Fi Access Point setup (192.168.4.1)
- TCP server listening on port 9999 for vital signs data
- Touch-friendly GUI built with Tkinter

## Installation

### Option 1: Download Pre-built Executable (Recommended)

1. Go to the [Actions](../../actions) tab in this repository
2. Click on the latest successful build workflow run
3. Download the `piobs-arm64-executable` artifact
4. Extract the artifact and transfer the `piobs` file to your Raspberry Pi
5. Make it executable (if not already):
   ```bash
   chmod +x piobs
   ```
6. Run it:
   ```bash
   sudo ./piobs
   ```
   Note: `sudo` is required for Access Point setup

### Option 2: Run from Source

```bash
# Install dependencies
sudo apt-get install python3-tk

# Run the application
sudo python3 piobs.py
```

## Usage

- Press `Escape` to minimize/restore the window
- Press `Ctrl+Q` to quit
- The application automatically starts a Wi-Fi Access Point on `wlan0`
- Connect to the AP and send vitals data to port 9999 in the format:
  ```
  BloodPressure=120/80,SpO2=98%,HeartRate=72,Temperature=98.6,RespiratoryRate=16
  ```

## Requirements

- Raspberry Pi with Raspberry Pi OS
- ARM64/aarch64 architecture (Raspberry Pi 3, 4, or 5)
- sudo privileges (for Access Point setup)
- hostapd and dnsmasq installed (for Access Point functionality)

## License

This is open source software for monitoring patient vitals on Raspberry Pi devices.
