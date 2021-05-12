from datetime import datetime, timedelta
from decimal import Decimal

class general:

    def getFechaDesde(fecha):
        #Por defecto es -2, si es lunes hago -4
        day_Diff=2
        if datetime.today().weekday() == 6:
            day_Diff=3
        if datetime.today().weekday() == 5:
            day_Diff=5
        if datetime.today().weekday() == 0:
            day_Diff=4

        fecha_desde=fecha.today()- timedelta(days=day_Diff)

        return fecha_desde

    def IsEsco(name):   
        not_esco=["Tutelar Inversora S.A.",
        "BBVA Asset Management Argentina S.A.G.F.C.I.",
        "HSBC Global Asset Management Argentina S.A.S.G.F.C.I.",
        "C y C Administradora de Fondos S.A.",
        "Mercofond S.G.F.C.I.S.A.",
        "Bayfe S.A.S.G.F.C.I.",
        "Nativa S.G.F.C.I.S.A."]

        esEsco=True

        if name in not_esco:
            esEsco=False

        return esEsco

    def FormatDecimal(number):
        dec= f'{Decimal(number):,}'
        retNumFormat=dec.replace(',', ' ').replace('.', ',').replace(' ', '.')

        return retNumFormat