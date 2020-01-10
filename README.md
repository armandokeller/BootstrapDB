This library create Model classes based on database structure (it reads all the tables and columns)

Those Model classes allow an easy manipulation of the database with almost none SQL.

## Installation

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
 #### Getting all the rows of "example" table
```python
import mysql.connector
from BootstrapDB import Base
from ExampleBase import ExampleBase
 
db = mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            database = "sample",
            auth_plugin = 'mysql_native_password',
            passwd = "supersecretpassword"
        )
        
all_examples = ExampleBase().query()
print(all_examples)
 ```
 
#### Getting all the rows of "example" table where the value of column size is equal to 22
Equivalent of the folowing SQL
```SQL
SELECT * FROM example WHERE size = 22
```
```python
import mysql.connector
from BootstrapDB import Base
from ExampleBase import ExampleBase
 
db = mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            database = "sample",
            auth_plugin = 'mysql_native_password',
            passwd = "supersecretpassword"
        )
        
size22 = ExampleBase().query("size = 22")
print(size22)
 ```
 
 #### Quering for single element by his private key value (like index)
```python
import mysql.connector
from BootstrapDB import Base
from ExampleBase import ExampleBase
 
db = mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            database = "sample",
            auth_plugin = 'mysql_native_password',
            passwd = "supersecretpassword"
        )
        
desired_object = ExampleBase(102)
print(desired_object)
 ```

#### Creating a new row in "example" table
```python
import mysql.connector
from BootstrapDB import Base
from ExampleBase import ExampleBase
 
db = mysql.connector.connect(
            host = "127.0.0.1",
            user = "root",
            database = "sample",
            auth_plugin = 'mysql_native_password',
            passwd = "supersecretpassword"
        )
new_item_obj = {"name":"Test object", "size":30}
new_item_row = ExampleBase(obj = new_item_obj)
new_item_row.save()
 ```
