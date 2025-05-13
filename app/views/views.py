from flask import Blueprint, render_template
import paramiko
import re

main_views = Blueprint("main_views", __name__)

def obtener_dispositivos_via_ssh():
    host = "192.168.1.1"  # IP del switch central
    username = "cisco"     # Usuario SSH
    password = "cisco"     # Contraseña SSH

    dispositivos = []

    try:
        # Establecer conexión SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, look_for_keys=False)

        # Ejecutar comando CDP
        stdin, stdout, stderr = ssh.exec_command("show cdp neighbors detail")
        output = stdout.read().decode("utf-8")
        ssh.close()

        # Parsear resultados
        bloques = output.strip().split("Device ID:")
        for bloque in bloques[1:]:
            nombre = bloque.split("\n")[0].strip()
            ip_match = re.search(r"IP address: (\d+\.\d+\.\d+\.\d+)", bloque)
            tipo_match = re.search(r"Platform: (.*?),", bloque)

            ip = ip_match.group(1) if ip_match else "Desconocido"
            tipo = tipo_match.group(1) if tipo_match else "Desconocido"

            dispositivos.append({
                'tipo': tipo,
                'nombre': nombre,
                'ip': ip,
                'estado': "Activo",
                'id': ip.replace(".", "")
            })

    except Exception as e:
        print("Error SSH:", e)

    return dispositivos


@main_views.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@main_views.route("/discovery", methods=["GET"])
def discovery_index():
    dispositivos = obtener_dispositivos_via_ssh()
    return render_template("discovery.html", dispositivos=dispositivos)


@main_views.route("/control_center/<device_id>", methods=["GET"])
def control_center_index(device_id):
    return render_template("device_console.html")
