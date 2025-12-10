#!/bin/bash
set -e

echo "=== Building PiObs AppImage for Raspberry Pi (ARM64) ==="

# Determine architecture
ARCH=$(uname -m)
echo "Building on architecture: $ARCH"

# Check for ARM64 environment
if [ "$ARCH" != "aarch64" ] && [ "$ARCH" != "arm64" ]; then
    echo "ERROR: This build script is designed for ARM64 (aarch64) architecture."
    echo "Current architecture: $ARCH"
    echo "Please run this script on a Raspberry Pi or ARM64-capable environment."
    exit 1
fi

# Install system dependencies if needed
if command -v apt-get &> /dev/null; then
    echo "Installing dependencies via apt-get..."
    if ! apt-get update; then
        echo "Warning: apt-get update failed, continuing anyway..."
    fi
    apt-get install -y python3 python3-pip python3-tk wget fuse libfuse2 || echo "Warning: Some packages may not have installed"
elif command -v yum &> /dev/null; then
    echo "Installing dependencies via yum..."
    yum install -y python3 python3-pip python3-tkinter wget fuse fuse-libs || echo "Warning: Some packages may not have installed"
fi

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install --upgrade pip || echo "Warning: pip upgrade failed"
pip3 install pyinstaller==6.11.1

# Clean previous builds
echo "Cleaning previous builds..."
rm -rf build dist AppDir *.AppImage

# Build the Python application with PyInstaller
echo "Building application with PyInstaller..."
pyinstaller --onefile --windowed \
    --name piobs \
    --hidden-import tkinter \
    --hidden-import _tkinter \
    piobs.py

# Create AppDir structure
echo "Creating AppDir structure..."
mkdir -p AppDir/usr/bin
mkdir -p AppDir/usr/share/applications
mkdir -p AppDir/usr/share/icons/hicolor/scalable/apps
mkdir -p AppDir/usr/lib

# Copy the built executable
echo "Copying executable..."
cp dist/piobs AppDir/usr/bin/

# Copy desktop file
echo "Copying desktop file..."
cp piobs.desktop AppDir/usr/share/applications/

# Copy icon
echo "Copying icon..."
cp piobs.svg AppDir/usr/share/icons/hicolor/scalable/apps/piobs.svg

# Create symlinks for AppImage compliance
echo "Creating AppImage-compliant symlinks..."
ln -sf usr/share/applications/piobs.desktop AppDir/piobs.desktop
ln -sf usr/share/icons/hicolor/scalable/apps/piobs.svg AppDir/piobs.svg
ln -sf usr/share/icons/hicolor/scalable/apps/piobs.svg AppDir/.DirIcon

# Copy AppRun
echo "Copying AppRun script..."
cp AppRun AppDir/
chmod +x AppDir/AppRun

# Download appimagetool if not exists
echo "Downloading appimagetool..."
if [ "$ARCH" = "aarch64" ] || [ "$ARCH" = "arm64" ]; then
    APPIMAGETOOL_ARCH="aarch64"
elif [ "$ARCH" = "x86_64" ]; then
    APPIMAGETOOL_ARCH="x86_64"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

APPIMAGETOOL="appimagetool-${APPIMAGETOOL_ARCH}.AppImage"
if [ ! -f "$APPIMAGETOOL" ]; then
    wget "https://github.com/AppImage/AppImageKit/releases/download/continuous/${APPIMAGETOOL}"
    chmod +x "$APPIMAGETOOL"
fi

# Build AppImage
echo "Building AppImage..."
ARCH=$APPIMAGETOOL_ARCH ./"$APPIMAGETOOL" AppDir PiObs-Monitor-${APPIMAGETOOL_ARCH}.AppImage

echo "=== Build complete! ==="
ls -lh PiObs-Monitor-*.AppImage

echo ""
echo "To use on Raspberry Pi:"
echo "1. Make the AppImage executable: chmod +x PiObs-Monitor-*.AppImage"
echo "2. Double-click to run, or execute: ./PiObs-Monitor-*.AppImage"
echo ""
echo "Note: You may need to install FUSE on your Raspberry Pi:"
echo "  sudo apt-get install fuse libfuse2"
