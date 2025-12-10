import tkinter as tk
from threading import Thread
import socket
import time
import os
import subprocess
from queue import Queue

# --- Vital placeholders
vitals = {
    "BloodPressure": "--/--",
    "SpO2": "--%",
    "HeartRate": "--",
    "Temperature": "--",
    "RespiratoryRate": "--"
}

update_queue = Queue()

# --- Start Wi-Fi Access Point (if not running)
def start_wifi_ap():
    try:
        subprocess.run(["sudo", "systemctl", "unmask", "hostapd"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "hostapd"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", "dnsmasq"], check=True)
        subprocess.run(["sudo", "systemctl", "restart", "hostapd"], check=True)
        subprocess.run(["sudo", "systemctl", "restart", "dnsmasq"], check=True)

        # Force wlan0 to static IP
        subprocess.run(["sudo", "ip", "addr", "flush", "dev", "wlan0"], check=True)
        subprocess.run(["sudo", "ip", "addr", "add", "192.168.4.1/24", "dev", "wlan0"], check=True)
        subprocess.run(["sudo", "ip", "link", "set", "wlan0", "up"], check=True)

        print("[Pi] AP started at 192.168.4.1.")
        return True
    except subprocess.CalledProcessError as e:
        print("[Pi] Failed to start AP or set static IP:", e)
        return False

# --- Stop Wi-Fi Access Point
def stop_wifi_ap():
    try:
        subprocess.run(["sudo", "systemctl", "stop", "hostapd"], check=True)
        subprocess.run(["sudo", "systemctl", "stop", "dnsmasq"], check=True)
        print("[Pi] Wi-Fi Access Point stopped.")
    except subprocess.CalledProcessError as e:
        print("[Pi] Failed to stop AP:", e)

# --- TCP Server Thread
def tcp_server():
    HOST = "0.0.0.0"
    PORT = 9999
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                s.bind((HOST, PORT))
                s.listen(1)
                print(f"[Pi] Listening on {HOST}:{PORT}")
                conn, addr = s.accept()
                print(f"[Pi] Connected to {addr}")
                with conn:
                    while True:
                        data = conn.recv(1024).decode()
                        if not data:
                            break
                        print("[Pi] Received:", data.strip())
                        try:
                            parts = data.strip().split(",")
                            local_vitals = vitals.copy()
                            for part in parts:
                                if '=' in part:
                                    key, value = part.split("=", 1)
                                    key = key.strip()
                                    value = value.strip()
                                    if key in local_vitals:
                                        local_vitals[key] = value
                            update_queue.put(local_vitals)
                        except Exception as e:
                            print("[Pi] Parse error:", e)
        except OSError as e:
            print(f"[Pi] Socket error: {e}. Retrying in 5 seconds...")
            time.sleep(5)

Thread(target=tcp_server, daemon=True).start()

# --- GUI Setup
def start_gui():
    if not start_wifi_ap():
        print("[Pi] Failed to start AP. Exiting GUI.")
        return

    root = tk.Tk()
    root.title("Vitals Monitor")
    root.configure(bg="black")
    root.overrideredirect(True)
    root.attributes("-fullscreen", True)
    root.lift()
    root.focus_force()
    root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    font_large_size = int(screen_height * 0.12)
    font_med_size = int(screen_height * 0.09)
    font_large = ("Helvetica", font_large_size, "bold")
    font_med = ("Helvetica", font_med_size, "bold")

    bp_label = tk.Label(root, text=vitals["BloodPressure"], fg="#e74c3c", bg="black", font=font_large)
    bp_label.pack(pady=int(screen_height * 0.05))

    row1 = tk.Frame(root, bg="black")
    row1.pack(pady=int(screen_height * 0.03), fill='x')
    spo2_label = tk.Label(row1, text=vitals["SpO2"], fg="yellow", bg="black", font=font_med)
    spo2_label.pack(side="left", expand=True)
    hr_label = tk.Label(row1, text=vitals["HeartRate"], fg="lime", bg="black", font=font_med)
    hr_label.pack(side="right", expand=True)

    row2 = tk.Frame(root, bg="black")
    row2.pack(pady=int(screen_height * 0.03), fill='x')
    temp_label = tk.Label(row2, text=vitals["Temperature"], fg="white", bg="black", font=font_med)
    temp_label.pack(side="left", expand=True)
    rr_label = tk.Label(row2, text=vitals["RespiratoryRate"], fg="white", bg="black", font=font_med)
    rr_label.pack(side="right", expand=True)

    def update_display():
        bp_label.config(text=vitals["BloodPressure"])
        spo2_label.config(text=vitals["SpO2"])
        hr_label.config(text=vitals["HeartRate"])
        temp_label.config(text=vitals["Temperature"])
        rr_label.config(text=vitals["RespiratoryRate"])

    def poll_queue():
        try:
            new_data = update_queue.get_nowait()
            for key in vitals:
                vitals[key] = new_data.get(key, vitals[key])
            update_display()
        except:
            pass
        root.after(100, poll_queue)

    poll_queue()

    minimized = [False]

    def toggle_minimize(event=None):
        if minimized[0]:
            root.deiconify()
            root.overrideredirect(True)
            root.attributes("-fullscreen", True)
            minimized[0] = False
        else:
            root.overrideredirect(False)
            root.withdraw()
            root.after(200, root.iconify)
            minimized[0] = True

    def on_close():
        stop_wifi_ap()
        root.destroy()

    root.bind("<Escape>", toggle_minimize)
    root.bind("<Control-q>", lambda e: on_close())
    root.protocol("WM_DELETE_WINDOW", on_close)

    root.mainloop()

if __name__ == "__main__":
    start_gui()
