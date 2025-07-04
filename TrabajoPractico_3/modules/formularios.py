#dependencias
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SelectField,ValidationError, SubmitField
from wtforms.validators import DataRequired, Length
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    """"Formulario de inicio de sesión."""

    username = StringField('Usuario', validators=[DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Iniciar sesión') # Botón de envío del formulario

class RegistroForm(FlaskForm):
    """Formulario de registro de usuario.
    Contiene campos para nombre, apellido, email, nombre de usuario, claustro,
    contraseña y confirmación de contraseña.
    !!! SE DEJA AFUERA EL ROL Y EL DEPARTAMENTO PORQUE NO SON NECESARIOS PARA EL USUARIO FINAL
    """
    nombre = StringField(label = "Nombre",  validators = [DataRequired()])
    apellido = StringField(label = "Apellido", validators = [DataRequired()])
    email = StringField(label = "Email", validators = [DataRequired(), Email()])
    nombreUsuario = StringField(label = "Nombre de usuario", validators = [DataRequired()])
    rol = "UsuarioFinal"
    password = PasswordField(label='Contraseña', validators=[DataRequired(), Length(min=4), EqualTo('confirmacion', message='Las contraseñas deben coincidir')])
    confirmacion = PasswordField(label='Repetir contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    # Validación personalizada
    def validarRol(self, field):
        """Valida que el rol seleccionado no esté vacío porque es una
        casilla de selección"""
        if field.data == "":
            raise ValidationError("Debes seleccionar un rol válido.")

class ReclamosForm(FlaskForm):
    """Formulario para crear un nuevo reclamo."""
    
    descripcion = StringField(label="Descripción del reclamo", validators=[DataRequired(), Length(max=500)])
    imagen = FileField(label="Imagen (opcional)", validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo se permiten imágenes en formato JPG, PNG o JPEG.')])
    submit = SubmitField('Crear Reclamo')  # Botón de envío del formulario