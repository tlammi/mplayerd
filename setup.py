
from setuptools import setup


setup(
    name="mplayerd",
    version="0.0.1",
    author="Toni Lammi",
    packages=["mplayerlib", "mplayerlib.conf", "mplayerlib.media",
        "mplayerlib.sched", "mplayer"],
    scripts=["bin/mplayerd"],
    description="Media player daemon",
    install_requires=["python-vlc >= 3.0.0", "jsonschema >= 4.6.0"]
)
