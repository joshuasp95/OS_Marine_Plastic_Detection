from gestion_archivos.acolite import test


if __name__ == '__main__':
    file = "S2A_12_12_34_14_95_39_34"
    nombre = test.obtener_fecha(file)
    print(nombre)