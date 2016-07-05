import datetime

class actuator:

    @staticmethod
    def generate_string(parameters, context):
        now = datetime.datetime.now()
        text = "It is {0:02d}:{1:02d}".format(now.hour, now.minute)
        return {"text": text }
