import datetime

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        week_day_name = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        month_name = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        now = datetime.date.today()

        if parameters["day_before"]:
            text = "Pasado mañana será"
            relative_date = now + datetime.timedelta(days=2)
        elif parameters["tomorrow"]:
            text = "Mañana será"
            relative_date = now + datetime.timedelta(days=1)
        elif parameters["before_yesterday"]:
            text = "Antes de ayer fue"
            relative_date = now + datetime.timedelta(days=-2)
        elif parameters["yesterday"]:
            text = "Ayer fue"
            relative_date = now + datetime.timedelta(days=-1)
        else:
            return {"text": "¿Qué dia sera mañana, pasado mañana, ayer o antes de ayer?", "confidence": 0.7, "context": {}}

        text = "{0} {1} {2} de {3} de {4}".format(text, week_day_name[relative_date.weekday()], relative_date.day, month_name[relative_date.month], relative_date.year)
        text = "{0}\nFecha estelar {1}.{2}".format(text, relative_date.year, relative_date.timetuple()[7])

        return {"text": text }
