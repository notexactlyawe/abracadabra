from setuptools import setup, find_packages

setup(
    name="abracadabra",
    version="0.1",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "numpy",
        "PyAudio",
        "pydub",
        "scipy",
        "tinytag"
    ],
    entry_points='''
        [console_scripts]
        song_recogniser=abracadabra.scripts.song_recogniser:cli
    ''',
)
