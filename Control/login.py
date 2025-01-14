from Modelo import database

def iniciar_sesion(matricula, password):
    usuario = database.validar_login(matricula, password)
    if usuario:
        return f"¡Bienvenido {matricula}!"
    else:
        return "Matrícula o contraseña incorrecta."

