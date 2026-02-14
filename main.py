#!/usr/bin/env python
import os
import subprocess
import sys

def start_server():
    # Fixed server directory in home to avoid multiple installs
    server_dir = os.path.expanduser("~/LMA_Server")
    jar_path = os.path.join(server_dir, "server.jar")

    if not os.path.exists(jar_path) or os.path.getsize(jar_path) == 0:
        print("Required files missing. Starting setup...")
        
        # Environment Setup
        check_repo = subprocess.run(["pkg", "list-installed", "tur-repo"], capture_output=True, text=True)
        if "tur-repo" not in check_repo.stdout:
            os.system("pkg install tur-repo -y")
        os.system("pkg update -y && pkg install openjdk-21 cloudflared -y")

        if not os.path.exists(f"{server_dir}/plugins"):
            os.makedirs(f"{server_dir}/plugins")
        
        with open(f"{server_dir}/eula.txt", "w") as f:
            f.write("eula=true")

        # Downloads
        os.system(f"wget https://api.papermc.io/v2/projects/paper/versions/1.20.1/builds/196/downloads/paper-1.20.1-196.jar -O {jar_path}")
        
        plugins = {
            "Geyser.jar": "https://download.geysermc.org/v2/projects/geyser/versions/latest/builds/latest/downloads/spigot",
            "Floodgate.jar": "https://download.geysermc.org/v2/projects/floodgate/versions/latest/builds/latest/downloads/spigot"
        }
        for name, url in plugins.items():
            p_path = f"{server_dir}/plugins/{name}"
            os.system(f"wget {url} -O {p_path}")

    # Execution Phase
    print(f"Starting minecraft Server...")
    os.chdir(server_dir)
    os.system("java -Xms512M -Xmx1024M -jar server.jar nogui")

if __name__ == "__main__":
    start_server()
