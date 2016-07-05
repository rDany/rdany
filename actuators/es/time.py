import datetime

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        now = datetime.datetime.now()
        if now.hour == 1:
            text = "Es la {0:02d}:{1:02d}".format(now.hour, now.minute)
        else:
            text = "Son las {0:02d}:{1:02d}".format(now.hour, now.minute)
        return {"text": text }
