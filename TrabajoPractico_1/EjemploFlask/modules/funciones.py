import random

def crear_lista_usuarios(n_usuarios):
    lista_usuarios = []
    for i in range(n_usuarios):
        usuario = {
            'nombre': f'usuario_{i+1}', # usuario_1, usuario_2, usuario_3, ...
            'edad': random.randint(18, 60) 
        }
        lista_usuarios.append(usuario)
    
    return lista_usuarios