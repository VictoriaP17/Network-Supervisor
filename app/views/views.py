from flask import Blueprint, render_template, request
import nmap  

main_views = Blueprint("main_views", __name__)


@main_views.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@main_views.route("/discovery", methods=["GET"])
def discovery_index():
    scanner = nmap.PortScanner()
    dispositivos = []

    try:
        
        scanner.scan(hosts='192.168.1.0/24', arguments='-sn')

        for host in scanner.all_hosts():
            estado = scanner[host].state()
            dispositivos_host = scanner[host]['hostnames']
            nombre = dispositivos_host[0]['name'] if dispositivos_host else "Desconocido"

            dispositivos.append({
                'tipo': 'Desconocido',  # Luego se puede mejorar
                'nombre': nombre if nombre else 'Sin nombre',
                'ip': host,
                'estado': 'Activo' if estado == 'up' else 'Inactivo',
                'id': host.replace('.', '')  # Simula un ID único
            })

    except Exception as e:
        print("Error durante el escaneo:", e)

    return render_template("discovery.html", dispositivos=dispositivos)


@main_views.route("/control_center/<device_id>", methods=["GET"])
def control_center_index(device_id):
    return render_template("device_console.html")
