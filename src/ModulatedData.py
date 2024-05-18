import numpy as np

class ModulatedData:
    def __init__(self, config=None):
        config = config or {}

        self._supported_modulation_format = ['ook']

        self._modulation_format = None
        self._samples = None
        self._data = None

        self.modulation_format = config.get("modulation_format", None)
        self.samples = config.get("samples", None)

        self.data = None

    @property
    def modulation_format(self):
        return self._modulation_format

    @modulation_format.setter
    def modulation_format(self, value):
        if value in self._supported_modulation_format:

            self._modulation_format = value
        else:
            raise ValueError(f"Unsupported modulation format: {value}...")

    @property
    def samples(self):
        return self._samples

    @samples.setter
    def samples(self, value):
        self._samples = value

    @property
    def data(self):
        return self._data
    
    @data.setter
    def data(self, value):
        self._data = value

    def generate_data(self):
        if self.modulation_format.lower() == "ook":
            self._generate_ook()

    def _generate_ook(self):
        self.data = np.random.choice([0, 1], self.samples)
