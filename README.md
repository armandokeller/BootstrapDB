This library create Model classes based on database structure (it reads all the tables and columns)

Those Model classes allow an easy manipulation of the database with almost none SQL.

## Instalation

```bash
python -m pip install --index-url https://test.pypi.org/simple/ --no-deps BootstrapDB-armandokeller
````

## Generating the classes

First you need to import the Bootstrap and Base classes and your connector for the database, then you can call Bootstrap() using the cursor as parameter, the same cursor must be set to Base.cursor.

Example:
```python
import mysql.connector
from BootstrapDB import Base, Bootstrap

db = mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            database = "sample",
            auth_plugin = 'mysql_native_password',
            passwd = "supersecretpassword"
        )

Base.cursor = db.cursor()
Bootstrap(Base.cursor)  
```
 The files will be at "out" folder
 
 ## Using the generated files
 
 ```python
 from ExampleBase
 ```
