#dependencias
from flask_wtf import FlaskForm
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
    nombreUsuario = StringField(label = "nombreUsuario", validators = [DataRequired()])
    claustro = SelectField(label="Claustro", choices=[("", "Seleccionar..."),
                                                      ("estudiante", "Estudiante"), 
                                                      ("docente", "Docente"),
                                                      ("no_docente", "No docente")], 
                                                      validators=[DataRequired(message="Por favor seleccioná un claustro.")])
    password = PasswordField(label='Password', validators=[DataRequired(), Length(min=4), EqualTo('confirmacion', message='Las contraseñas deben coincidir')])
    confirmacion = PasswordField(label='Repetir contraseña', validators=[DataRequired()])
    submit = SubmitField('Registrarse')

    # Validación personalizada
    def validate_claustro(self, field):
        """Valida que el claustro seleccionado no esté vacío porque es una
        casilla de selección"""
        if field.data == "":
            raise ValidationError("Debes seleccionar un claustro válido.")
        