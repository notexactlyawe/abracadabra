import logging
from simple_settings import LazySettings

settings = LazySettings("settings")

logging.basicConfig(filename='abracadabra.log', level=logging.DEBUG)
