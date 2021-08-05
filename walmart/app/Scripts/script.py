class ComunicacionWeb ():
    def __init__(self):



        self.informacion = dict (
            interfaz = 0,
            X_02 = 1,
            X_01 = 2,
            X_03 = 3,
            X_04 = 4,
            X_05 = 5,
            X_06 = 6,
            X_07 = 7,
        )



        self.variables = dict (
            monto_ingresar = 1,
            monto_ingresado = 1,
            monto_a_dispensar = 0,
            folio = 0,
            hora_entrada = 0,
            tiempo_total = "",
            interfaz = 1,
            descuento = 0,
            X_08 = 0,
            X_09 = 0,
            X_10 = 0,
            X_11 = 0,
            X_12 = 0,
            X_13 = 0,
            X_14 = 0,
            X_15 = 0,
            X_16 = 0,
            X_17 = 0,
            X_18 = 0,
            X_19 = 0,
            X_20 = 0,
            X_21 = 0,
            X_22 = 0,
        )

        print (self.informacion)
        print (self.variables)


def main():
    comunicacion = ComunicacionWeb()


if __name__ == "__main__":
    main()