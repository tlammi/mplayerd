import datetime
import os
import logging

_FORMAT = "%d.%m %H:%M:%S"


class _Handler(logging.Handler):

    def __init__(self, outdir: str, log_name: str):
        super().__init__()
        self._l = os.path.join(outdir, log_name + ".log")
        self._w = os.path.join(outdir, log_name + ".warn")
        self._e = os.path.join(outdir, log_name + ".err")

        for path in (self._l, self._w, self._e):
            with open(path, "a") as f:
                msg = f"Start time: {datetime.datetime.now().strftime(_FORMAT)}"
                f.write("#" * len(msg) + "\n")
                f.write(msg + "\n")
                f.write("#" * len(msg) + "\n")

    def emit(self, record: logging.LogRecord) -> None:
        t = datetime.datetime.now()
        datestr = t.strftime(_FORMAT)
        msg = f"{datestr} >  {record.getMessage()}\n"
        if record.levelno >= logging.ERROR:
            with open(self._e, "a") as f:
                f.write(msg)
        elif record.levelno >= logging.WARN:
            with open(self._w, "a") as f:
                f.write(msg)
        with open(self._l, "a") as f:
            f.write(msg)
        print(msg, end="")


def init(outdir: str, level=logging.INFO, log_name="mplayerd"):
    root = logging.getLogger("")
    root.setLevel(level)
    root.addHandler(_Handler(outdir, log_name))
