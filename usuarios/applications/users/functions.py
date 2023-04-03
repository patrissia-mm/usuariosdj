#funciones extra de la aplicación usuarios
import random
import string

#función que genera un código de 6 dígitos texto mayúscula y dígitos
def code_generator(size=6, chars=string.ascii_uppercase+string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
