from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime

ListaUsuarios=[]

now = datetime.now() #para la fecha de envío


app = Flask(__name__)

class usuario: 
    
    def __init__(self, alias, nombre, ListaContactos):
        self.alias = alias
        self.nombre = nombre
        self.ListaContactos = ListaContactos
        self.MensajesEnviados = []
        self.MensajesRecibidos = []
        ListaUsuarios.append(self)
    
    def verContactos(self):
        return jsonify(self.ListaContactos)
    
    def agregarContacto(self, alias, nombre_real):
        nuevo = contacto(alias, now)
        user = usuario(alias, nombre_real, []) 
        if user not in ListaUsuarios:
            ListaUsuarios.append(user)
        if nuevo not in self.ListaContactos:
            self.ListaContactos.append(nuevo)
            return jsonify(nuevo)
        else:
            return "Ya existe el contacto"


    def enviarMensaje(self, destinatario, mensaje):
        message = mensaje(self.alias, destinatario, mensaje, now)
        if destinatario not in self.ListaContactos:
            return "No existe el contacto"
        self.MensajesEnviados[destinatario].append(message)
        return jsonify(self.MensajesEnviados)
    
    def verHistorialMensajes(self):
        return jsonify(self.MensajesRecibidos)

class mensaje:
    def __init__(self,remitente, destinatario,contenido, fechaEnvio):
        self.remitente = remitente
        self.destinatario = destinatario 
        self.contenido = contenido
        self.fechaEnvio = fechaEnvio
    
class contacto:
    def __init__(self, alias, fechaRegistro):
        self.alias = alias
        self.fechaRegistro = fechaRegistro



@app.route('/mensajeria/contactos?mialias={alias} GET')
def contactos(alias):
    print("holaaa")
    return ListaUsuarios[alias].verContactos()

@app.route('/mensajeria/contactos/{alias} POST')
def agregar_contacto(alias):
    alias = request.json['contacto']
    nombre_real = request.json['nombre']
    return ListaUsuarios[alias].agregarContacto(alias, nombre_real)

@app.route('/mensajeria/enviar POST')
def enviar():
    usuario = request.json['usuario']
    destinatario = request.json['contacto']
    mensaje = request.json['mensaje']
    return ListaUsuarios[usuario].enviarMensaje(destinatario, mensaje)

@app.route('/mensajeria/recibidos?mialias={alias} GET')
def mensajes(alias):
    return ListaUsuarios[alias].verHistorialMensajes()

@app.route('/')
def index():
    return "Hello, World!"

usuario_1 = usuario(alias="camotito",nombre="camilo",ListaContactos=["luis"])     
usuario_2 = usuario(alias="pikachu",nombre="jose",ListaContactos=["camotito"])
usuario_3 = usuario(alias="luis",nombre="luis",ListaContactos=[])

if __name__ == "__main__":
    app.run(debug=True)


