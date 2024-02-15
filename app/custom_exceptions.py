# Create a custom exception class named GradioUrlNotFound

class GradioUrlNotFound(Exception):
    def __init__(self,instance_id=None):
        self.message = "NOT_FOUND"
        self.instance_id = instance_id
        super().__init__(self.message)

    def __str__(self):
        base_msg = super().__str__()
        if self.instance_id:
            return f"{base_msg} (instance_id: {self.instance_id})"
        return base_msg


class GradioUrlWrong(Exception):
    def __init__(self,instance_id):
        self.message = "WRONG_GRADIO_URL"
        self.instance_id = instance_id
        super().__init__(self.message)

    def __str__(self):
        base_msg = super().__str__()
        if self.instance_id:
            return f"{base_msg} (instance_id: {self.instance_id})"
        return base_msg