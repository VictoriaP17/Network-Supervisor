from flask import Blueprint, render_template
import paramiko

# Fixed the Blueprint initialization with proper string for __name__
main_views = Blueprint("main_views", __name__)

def obtener_dispositivos_via_ssh():
    host = "192.168.1.1"  # IP del Router R1 conectado a tu laptop
    username = "cisco"
    password = "cisco"
    dispositivos = []
    try:
        # Conexión SSH
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=username, password=password, look_for_keys=False)
        
        # Ejecutar comando CDP detail
        stdin, stdout, stderr = ssh.exec_command("show cdp neighbors detail")
        output = stdout.read().decode("utf-8")
        ssh.close()
        print("Salida CDP detail:\n", output)
        
        # Procesar bloques de dispositivos
        bloques = output.strip().split("Device ID: ")[1:]
        for bloque in bloques:
            lineas = bloque.strip().splitlines()
            nombre = lineas[0].strip()
            ip = "Desconocido"
            plataforma = "Desconocido"
            
            for linea in lineas:
                if "IP address:" in linea:
                    ip = linea.split("IP address:")[1].strip()
                elif "Platform:" in linea:
                    plataforma = linea.split("Platform:")[1].split(",")[0].strip()
            
            dispositivos.append({
                'nombre': nombre,
                'ip': ip,
                'tipo': plataforma,
                'estado': "Activo",
                'id': nombre.replace(".", "")
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
    print(dispositivos)
    return render_template("discovery.html", dispositivos=dispositivos)

@main_views.route("/control_center/<device_id>", methods=["GET"])
def control_center_index(device_id):
    dispositivos = obtener_dispositivos_via_ssh()
    dispositivo = next((d for d in dispositivos if d['id'] == device_id), None)
    if not dispositivo:
        return "Dispositivo no encontrado", 404
    return render_template("device_console.html", dispositivo=dispositivo)