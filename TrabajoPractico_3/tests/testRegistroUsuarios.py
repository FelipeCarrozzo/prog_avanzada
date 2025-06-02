import unittest
from flask import Flask
from modules.formularios import RegistroForm

class TestRegistroForm(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_campos_obligatorios(self):
        form = RegistroForm(formdata=None, meta={'csrf': False})
        self.assertFalse(form.validate())
        self.assertIn('nombre', form.errors)
        self.assertIn('apellido', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('nombreUsuario', form.errors)
        self.assertIn('claustro', form.errors)
        self.assertIn('password', form.errors)
        self.assertIn('confirmacion', form.errors)

    # def test_email_invalido(self):
    #     data = {
    #         'nombre': 'Juan',
    #         'apellido': 'Pérez',
    #         'email': 'noesemail',
    #         'nombreUsuario': 'juanp',
    #         'claustro': 'estudiante',
    #         'password': '1234',
    #         'confirmacion': '1234'
    #     }
    #     form = RegistroForm(data=data, meta={'csrf': False})
    #     self.assertFalse(form.validate())
    #     self.assertIn('email', form.errors)

    # def test_passwords_no_coinciden(self):
    #     data = {
    #         'nombre': 'Juan',
    #         'apellido': 'Pérez',
    #         'email': 'juan@mail.com',
    #         'nombreUsuario': 'juanp',
    #         'claustro': 'docente',
    #         'password': '1234',
    #         'confirmacion': '5678'
    #     }
    #     form = RegistroForm(data=data, meta={'csrf': False})
    #     self.assertFalse(form.validate())
    #     self.assertIn('password', form.errors)

    def test_claustro_vacio(self):
        data = {
            'nombre': 'Ana',
            'apellido': 'López',
            'email': 'ana@mail.com',
            'nombreUsuario': 'anal',
            'claustro': '',
            'password': 'abcd',
            'confirmacion': 'abcd'
        }
        form = RegistroForm(data=data, meta={'csrf': False})
        self.assertFalse(form.validate())
        self.assertIn('claustro', form.errors)
        print(form.errors['claustro'])
        self.assertTrue(any('Por favor seleccioná un claustro.' in err for err in form.errors['claustro']))

    def test_formulario_valido(self):
        data = {
            'nombre': 'Ana',
            'apellido': 'López',
            'email': 'ana@mail.com',
            'nombreUsuario': 'anal',
            'claustro': 'docente',
            'password': 'abcd',
            'confirmacion': 'abcd'
        }
        form = RegistroForm(data=data, meta={'csrf': False})
        self.assertTrue(form.validate())

if __name__ == '__main__':
    unittest.main()
