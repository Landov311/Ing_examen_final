import unittest
from unittest.mock import patch, Mock
from app import app, usuario, contacto, now
#primer caso de error agregar como contacto a un contacto ya agregado
#segundo caso de error enviar un mensaje a un contacto inexistente
#tercer caso de error usuario inexistente genera un mensaje a un contacto 
class TestApp(unittest.TestCase):

    usuario_1 = usuario(alias="camotito",nombre="camilo",ListaContactos=["luis"])     

    usuario_2 = usuario(alias="pikachu",nombre="jose",ListaContactos=[])

    usuario_3 = usuario(alias="luis",nombre="luis",ListaContactos=[])

    @classmethod
    def setUpClass(cls):
        # Set up a Flask test client for the entire test class
        cls.client = app.test_client()
        app.config['TESTING'] = True
    
    #primer caso error crear un contacto ya creado
    def test_agregar_contacto(self):
        response = self.client.post("/mensajeria/contactos/{usuario_1.alias}", json={"contacto":"luis","nombre":"luis"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, "Ya existe el contacto")

    #segundo caso error enviar mensaje a un contacto inexistente
    def test_enviar_mensaje(self):
        response = self.client.post("/mensajeria/enviar", json={"remitente":"camotito","destinatario":"pikachu","contenido":"hola"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data, "No existe el contacto") 

    #tercer caso error usuario inexistente genera un mensaje a un contacto 
    def test_enviar_mensaje(self):
        response = self.client.post("/mensajeria/enviar", json={"remitente":"camotito","destinatario":"pikachu","contenido":"hola"})
        self.assertEqual(response.status_code, 200)

    #Mostrar contactos de un usuario
    def test_contactos(self):
        response = self.client.get("/mensajeria/contactos?mialias={usuario_1.alias}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

    #Mostrar Historial de Mensajes de un usuario
    def test_historial_mensajes(self):
        response = self.client.get("/mensajeria/recibidos?mialias={usuario_1.alias}")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)

# Run the test suite
if __name__ == '__main__':
    unittest.main()
