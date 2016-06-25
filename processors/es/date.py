import re
import datetime

class processor:
    example = "¿Qué día es?"
    keywords = ["qué", "que", "día", "día", "fecha", "es"]

    @staticmethod
    def check_string(string, context):
        week_day_name = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        month_name = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        now = datetime.date.today()

        confidence = 0
        pidefecha = re.search(r"(fecha|qu(e|é)\s+d(i|á­)a\s+es)", string, re.IGNORECASE)
        confidence = 0.7
        if not pidefecha:
            pidefecha = re.search(r"cu(a|á)l\s+es\s+(la|el)\s+(fecha|d(i|í)a\s+de\s+\s+hoy)", string, re.IGNORECASE)
            confidence = 1


        text = None
        if pidefecha:
            text = "Hoy es {0} {1} de {2} de {3}".format(week_day_name[now.weekday()], now.day, month_name[now.month], now.year)
            text = "{0}\nFecha estelar {1}.{2}".format(text, now.year, now.timetuple()[7])

            return {"text": text, "confidence": confidence, "context": {} }

        return None
