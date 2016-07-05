import datetime

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        week_day_name = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        month_name = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
        now = datetime.date.today()
        text = "Hoy es {0} {1} de {2} de {3}".format(week_day_name[now.weekday()], now.day, month_name[now.month], now.year)
        text = "{0}\nFecha estelar {1}.{2}".format(text, now.year, now.timetuple()[7])
        return {"text": text }
