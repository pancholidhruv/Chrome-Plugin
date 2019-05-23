

class ImageMatch(object):

    def __init__(self, name, input_label, output_label,
                 expected_label):
        self.name = name
        self.input_label = input_label
        self.output_label = output_label
        self.expected_label = expected_label

    def serialize(self):
        return {
            'name': self.name,
            'input_label': self.input_label,
            'output_label': self.input_label,
            'expected_label': self.input_label,
        }
