from datetime import datetime, timedelta

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