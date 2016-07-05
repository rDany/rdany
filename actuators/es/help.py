
class actuator:

    @staticmethod
    def generate_string(parameters, context):
        text = "Algunas cosas que podés preguntarme:{0}".format(\
            context["general.processors_examples"]["es"]
        )
        return {"text": text }
