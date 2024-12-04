from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

ListaUsuarios = {}

class Usuario:
    def __init__(self, alias, nombre):
        self.alias = alias
        self.nombre = nombre
        self.contactos = []
        self.mensajes_enviados = []
        self.mensajes_recibidos = []

    def ver_contactos(self):
        return jsonify([c.alias for c in self.contactos])

    def agregar_contacto(self, alias_contacto):
        if alias_contacto not in ListaUsuarios:
            return jsonify({"error": "El usuario no existe"}), 404
        contacto = ListaUsuarios[alias_contacto]
        if contacto not in self.contactos:
            self.contactos.append(contacto)
            return jsonify({"mensaje": f"Contacto {alias_contacto} agregado con éxito"}), 201
        return jsonify({"error": "El contacto ya existe"}), 400

    def enviar_mensaje(self, alias_destinatario, contenido):
        if alias_destinatario not in [c.alias for c in self.contactos]:
            return jsonify({"error": "El destinatario no está en la lista de contactos"}), 400
        mensaje = Mensaje(self.alias, alias_destinatario, contenido)
        destinatario = ListaUsuarios[alias_destinatario]
        self.mensajes_enviados.append(mensaje)
        destinatario.mensajes_recibidos.append(mensaje)
        return jsonify({"mensaje": "Mensaje enviado con éxito"}), 200

    def ver_mensajes_recibidos(self):
        return jsonify([vars(m) for m in self.mensajes_recibidos])


class Mensaje:
    def __init__(self, remitente, destinatario, contenido):
        self.remitente = remitente
        self.destinatario = destinatario
        self.contenido = contenido
        self.fecha_envio = datetime.now()


@app.route('/mensajeria/contactos/<alias>', methods=['GET'])
def ver_contactos(alias):
    if alias in ListaUsuarios:
        return ListaUsuarios[alias].ver_contactos()
    return jsonify({"error": "Usuario no encontrado"}), 404


@app.route('/mensajeria/contactos/<alias>', methods=['POST'])
def agregar_contacto(alias):
    if alias not in ListaUsuarios:
        return jsonify({"error": "Usuario no encontrado"}), 404
    data = request.json
    return ListaUsuarios[alias].agregar_contacto(data['contacto'])


@app.route('/mensajeria/enviar', methods=['POST'])
def enviar_mensaje():
    data = request.json
    alias = data['usuario']
    if alias not in ListaUsuarios:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return ListaUsuarios[alias].enviar_mensaje(data['contacto'], data['mensaje'])


@app.route('/mensajeria/recibidos/<alias>', methods=['GET'])
def mensajes_recibidos(alias):
    if alias in ListaUsuarios:
        return ListaUsuarios[alias].ver_mensajes_recibidos()
    return jsonify({"error": "Usuario no encontrado"}), 404


@app.route('/')
def index():
    return "Hello, World!"


# Creación de usuarios iniciales
ListaUsuarios["camotito"] = Usuario("camotito", "Camilo")
ListaUsuarios["pikachu"] = Usuario("pikachu", "José")
ListaUsuarios["luis"] = Usuario("luis", "Luis")

if __name__ == "__main__":
    app.run(debug=True)
