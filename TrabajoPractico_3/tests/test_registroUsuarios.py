import unittest
from flask import Flask
from modules.formularios import RegistroForm

class TestRegistroForm(unittest.TestCase):
    """
    Clase de prueba para el formulario de registro de usuarios.
    Verifica que los campos obligatorios estén presentes y que las validaciones funcionen correctamente.
    """
    def setUp(self):
        """Inicializa la aplicación Flask y el contexto de la aplicación para las pruebas."""
        self.app = Flask(__name__)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        """Limpia el contexto de la aplicación después de las pruebas."""
        self.app_context.pop()

    def test_campos_obligatorios(self):
        """Test para verificar que todos los campos obligatorios están presentes en el formulario."""
        form = RegistroForm(formdata=None, meta={'csrf': False})
        self.assertFalse(form.validate())
        self.assertIn('nombre', form.errors)
        self.assertIn('apellido', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('nombreUsuario', form.errors)
        self.assertIn('password', form.errors)
        self.assertIn('confirmacion', form.errors)

    def test_email_invalido(self):
        """Test para verificar que el campo de email es válido."""
        data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'email': 'noesemail',
            'nombreUsuario': 'juanp',
            'password': '1234',
            'confirmacion': '1234'
        }
        form = RegistroForm(data=data, meta={'csrf': False})
        self.assertFalse(form.validate())
        self.assertIn('email', form.errors)

    def test_passwords_no_coinciden(self):
        """Test para verificar que las contraseñas coinciden."""
        data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'email': 'juan@mail.com',
            'nombreUsuario': 'juanp',
            'password': '1234',
            'confirmacion': '5678'
        }
        form = RegistroForm(data=data, meta={'csrf': False})
        self.assertFalse(form.validate())
        self.assertIn('password', form.errors)


    def test_formulario_valido(self):
        """Test para verificar que el formulario es válido con datos correctos."""
        data = {
            'nombre': 'Ana',
            'apellido': 'López',
            'email': 'ana@mail.com',
            'nombreUsuario': 'anal',
            'password': 'abcd',
            'confirmacion': 'abcd'
        }
        form = RegistroForm(data=data, meta={'csrf': False})
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
