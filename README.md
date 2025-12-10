# PiObs - Vitals Monitor for Raspberry Pi

Python software for Raspberry Pi to receive and display vitals from pysender via locally generated Access Point.

## Features

- Receives vital signs data over TCP (port 9999)
- Displays Blood Pressure, SpO2, Heart Rate, Temperature, and Respiratory Rate
- Fullscreen GUI with large, readable text
- Automatic Wi-Fi Access Point setup on Raspberry Pi
- Runs on 192.168.4.1

## Building and Installing

### Option 1: Download Pre-built AppImage (Easiest)

1. Download the latest AppImage from the [GitHub Actions artifacts](https://github.com/charlieatkinson33/piobs/actions)
2. Transfer it to your Raspberry Pi
3. Make it executable:
   ```bash
   chmod +x PiObs-Monitor-aarch64.AppImage
   ```
4. Install FUSE if needed (first time only):
   ```bash
   sudo apt-get update
   sudo apt-get install fuse libfuse2
   ```
5. Double-click the AppImage or run it from terminal:
   ```bash
   ./PiObs-Monitor-aarch64.AppImage
   ```

### Option 2: Build Locally on Raspberry Pi

1. Clone this repository:
   ```bash
   git clone https://github.com/charlieatkinson33/piobs.git
   cd piobs
   ```

2. Run the build script:
   ```bash
   chmod +x build-appimage.sh
   ./build-appimage.sh
   ```

3. The AppImage will be created as `PiObs-Monitor-aarch64.AppImage`

4. Make it executable and run:
   ```bash
   chmod +x PiObs-Monitor-aarch64.AppImage
   ./PiObs-Monitor-aarch64.AppImage
   ```

### Option 3: Run Directly with Python

If you don't want to use AppImage:

```bash
sudo apt-get install python3 python3-tk
python3 piobs.py
```

## Usage

1. **Starting the Application**: Double-click the AppImage or run it from terminal
   - The application will automatically start the Wi-Fi Access Point
   - The Pi will be accessible at `192.168.4.1`
   - The application will listen on port `9999` for incoming data

2. **Connecting from Sender**: Configure your pysender to connect to `192.168.4.1:9999`

3. **Controls**:
   - `ESC` - Minimize/restore the window
   - `Ctrl+Q` - Quit the application

4. **Data Format**: Send vitals as comma-separated key=value pairs:
   ```
   BloodPressure=120/80,SpO2=98%,HeartRate=75,Temperature=98.6,RespiratoryRate=16
   ```

## Requirements

- Raspberry Pi (any model with Wi-Fi)
- Python 3.7 or higher
- Tkinter (python3-tk)
- For AppImage: FUSE (libfuse2)

## System Setup for Access Point

The application requires the following to be configured on your Raspberry Pi:
- `hostapd` - for Wi-Fi Access Point
- `dnsmasq` - for DHCP server

The application will attempt to configure these automatically with sudo privileges.

## Troubleshooting

### AppImage won't run
- Make sure FUSE is installed: `sudo apt-get install fuse libfuse2`
- Make the AppImage executable: `chmod +x PiObs-Monitor-aarch64.AppImage`
- Try running from terminal to see error messages

### Wi-Fi Access Point doesn't start
- Ensure hostapd and dnsmasq are installed: `sudo apt-get install hostapd dnsmasq`
- Check if the wireless interface is available: `ip link show wlan0`
- The application needs sudo privileges to configure networking

### Display issues
- The application runs in fullscreen mode by default
- Press ESC to minimize if needed
- Screen size and fonts scale automatically

## License

This project is open source.
