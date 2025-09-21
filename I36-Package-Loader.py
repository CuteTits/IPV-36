import subprocess
import sys

def install_packages(packages):
    for package in packages:
        try:
            subprocess.check_output([sys.executable, "-m", "pip", "install", package])
            print(f"{package} installed successfully.")
        except subprocess.CalledProcessError:
            print(f"{package} already installed.")

if __name__ == "__main__":
    required_packages = [
        "PySocks",
        "beautifulsoup4",
        "scapy",
        "geocoder",
        "psutil",
        "speedtest-cli",
        "ping3",
        "requests",
        "speedtest",

"cryptography.hazmat.primitives.asymmetric",
"pymobiledevice3.cli.remote",
"pymobiledevice3.remote.core_device_tunnel_service",
"pymobiledevice3.remote.remote_service_discovery",
"pymobiledevice3.services.dvt.dvt_secure_socket_proxy",
"pymobiledevice3.services.dvt.instruments.location_simulation",


    ]

    print("Installing required packages...")

    try:
        install_packages(required_packages)
        print("All packages installed successfully.")
    except Exception as e:
        print("An error occurred during installation:", e)
