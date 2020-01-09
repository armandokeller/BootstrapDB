
BOOTSTRAP_DIR = "out"
IMPORTS = """import mysql.connector
import json
from BootstrapDB import Base
"""

def sqlRender(value):
    if value is None:
        return "'NULL'"
    elif type(value) ==  str:
        return f"'{value}'"
    return value
