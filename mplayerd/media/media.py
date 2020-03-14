import abc


class Media:

    def __init__(self, file: str, options: dict = None):
        options = options or {}
        self._file = file
        self._options = []
        for option, value in options.items():
            self._options.append(f"{option}={value}")

    @property
    def file(self):
        return self._file

    @property
    def options(self):
        return self._options

