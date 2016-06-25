import re
import datetime

class processor:
    example = "¿Qué día fue ayer?"

    @staticmethod
    def check_string(string, context):
        week_day_name = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        month_name = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        now = datetime.date.today()

        pidefecha_relativa = re.search(r"(qu(e|é))\s+(fecha|d(i|í)a)\s+(es|ser(a|á)|va\sa\sser|fue)\s+(?P<buscar>.+)", string, re.IGNORECASE)
        text = None
        if pidefecha_relativa:
            parameter = pidefecha_relativa.group('buscar')
            before_yesterday = re.search(r"\W*antes\s*de\s*ayer", parameter, re.IGNORECASE)
            yesterday = re.search(r"\W*ayer", parameter, re.IGNORECASE)
            tomorrow = re.search(r"\W*mañana", parameter, re.IGNORECASE)
            day_before = re.search(r"\W*pasado\s+mañana", parameter, re.IGNORECASE)

            if day_before:
                text = "Pasado mañana será"
                relative_date = now + datetime.timedelta(days=2)
            elif tomorrow:
                text = "Mañana será"
                relative_date = now + datetime.timedelta(days=1)
            elif before_yesterday:
                text = "Antes de ayer fue"
                relative_date = now + datetime.timedelta(days=-2)
            elif yesterday:
                text = "Ayer fue"
                relative_date = now + datetime.timedelta(days=-1)
            else:
                return {"text": "¿Qué dia sera mañana, pasado mañana, ayer o antes de ayer?", "confidence": 0.7, "context": {}}

            text = "{0} {1} {2} de {3} de {4}".format(text, week_day_name[relative_date.weekday()], relative_date.day, month_name[relative_date.month], relative_date.year)
            text = "{0}\nFecha estelar {1}.{2}".format(text, relative_date.year, relative_date.timetuple()[7])

            return {"text": text, "confidence": 0.7, "context": {}}
