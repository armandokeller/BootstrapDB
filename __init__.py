import json
import os
import sys
import shutil
from BootstrapDB.utils import sqlRender, BOOTSTRAP_DIR, IMPORTS



class Bootstrap:
    """
    Create model classes for every table available on selected database

    Arguments
    ---------
    :param cursor: Cursor to database
    """

    def __init__(self, cursor):
        self.cursor = cursor
        self._tables = []
        self._clearBootstrapDir()
        self._createBootstrapDir()
        self._getTables()

        for table in self._tables:
            self._createClass(table)
    
    def _clearBootstrapDir(self):
        """
        Remove output directory and all files and folders inside
        """
        if BOOTSTRAP_DIR in os.listdir():
            shutil.rmtree(BOOTSTRAP_DIR)
    
    def _createBootstrapDir(self):
        """
        Create an empty output directory
        """
        os.mkdir(BOOTSTRAP_DIR)
    
    def _getTables(self):
        """
        Get all available table names from database
        """
        self.cursor.execute("show tables")
        self._tables = [str(table[0]) for table in self.cursor.fetchall()]

    def _createClass(self,table):
        """
        Create class file for a given table name
        
        :param table: Table's name
        :type table: str
        """
        pk = None
        textfile = open(f"{BOOTSTRAP_DIR}/{self.__safeName(table)}Base.py","a+")
        textfile.write(IMPORTS)
        textfile.write(f"\nclass {self.__safeName(table)}Base(Base):\n    def __init__(self, pk = None, obj = None):\n    ")
        self.cursor.execute(f"describe {table}")
        column_list = []
        for column in self.cursor.fetchall():
            if str(column[3]).upper() == "PRI":
                pk = column[0]
            textfile.write(f"    self.{column[0]} = None\n    ")
            column_list.append(f"'{column[0]}'")
        if pk:
            textfile.write(f"    self._pk = '{pk}'\n    ")
        textfile.write(f"    self._table_name = '{table}'\n    ")
        textfile.write(f"    self._column_list = [{', '.join(column_list)}]\n    ")
        textfile.write(f"    super().__init__(pk, obj)\n    ")
        textfile.close()

    def __safeName(self,text):
        """
        Format a string to a safe class name

        Parameters:
        -------
            text (str): text to be formatted
        """
        res = str(text).strip()
        res = res.replace(' ','_')
        return res.replace(res[0],res[0].upper(),1)


class Base:
    """
        Base class for database objects

        Parameters:
        -------
        pk (str) : Primary Key field name (default None)

        obj (object): Python object (default None)
    """

    cursor = None

    def __init__(self,pk=None,obj=None):
        
        if not hasattr(self,"_table_name"):
            self._table_name = None
        if not hasattr(self,"_pk"):
            self._pk = None

        if pk:
            self.getByPk(pk)
        elif obj:
            self.fromObject(obj)
    
    def updateColumns(self):
        """
        Update the attributes based on database columns
        """
        if self._table_name:
            Base.cursor.execute(f"describe {self._table_name}")
            results = Base.cursor.fetchall()
            if Base.cursor.rowcount>0:
                self._column_list = []
                for column  in results:
                    self._column_list.append(column[0])
                    if column[3] == "PRI":
                        self.pk = column[0]
                    setattr(self,column[0],None)
            else:
                raise Exception(f"Table {self._table_name} has no columns")
    
    def getByPk(self,pk):
        """
        Query element by PrimaryKey value

        Parameters:
        -------
            pk: Primary key value
        """
        Base.cursor.execute(f"SELECT * FROM {self._table_name} WHERE {self._pk} = {sqlRender(pk)}")
        result = Base.cursor.fetchone()
        data = zip(self._column_list, result)
        for item in data:
            setattr(self,item[0],item[1])
    
    def query(self,condition = None):
        """
        Return a list of elements based on query condition

        Parameters:
        -------
            condition (str): condition to WHERE statement
        """
        if condition:
            query_string = f"SELECT * FROM {self._table_name} WHERE {condition}"
            print(query_string)
        else:
            query_string = f"SELECT * FROM {self._table_name}"
        Base.cursor.execute(query_string)
        results = list()
        for result in Base.cursor.fetchall():
            element = self.__class__()
            element.fromValues(result)
            results.append(element)
        return results


    def save(self):
        """
        Save or update the object on database
        If the PrimaryKey value is defined the object will be updated, if not a new row will be inserted
        """
        values = [str(prop)+" = "+str(sqlRender(getattr(self,prop))) for prop in self._column_list]
        
        if getattr(self,self.pk):
            Base.cursor.execute(f"UPDATE {self._table_name} SET {', '.join(values)} WHERE {self.pk}={sqlRender(self.pk)}")
            Base.cursor.commit()
            Base.cursor.fetchall()
        else:
            list_without_pk = self._column_list.copy()
            list_without_pk.remove(self.pk)
            values = [getattr(self,item) if getattr(self,item) else "NULL" for item in list_without_pk]
            Base.cursor.execute(f"INSERT INTO {self._table_name} ({', '.join(list_without_pk)}) VALUES ( { ', '.join([str(sqlRender(value)) for value in values])}")
            Base.cursor.commit()
            Base.cursor.fetchall()
    
    def toObject(self):
        """
        Returns a python object of the instance, where the keys are the the column names.
        """
        obj = {}
        for item in self._column_list:
            obj[item] = getattr(self,item)
        return obj
    
    def fromObject(self,obj):
        """
        Populate the attributes based on object, using the object keys as column names
        """
        self._column_list = list(obj.keys())
        for key in self._column_list:
            setattr(self,key,obj[key])

    def fromValues(self,values):
        """
        Populate the attributes based on values, using the positional order to associate with column names 
        """
        if len(values) == len(self._column_list):
            obj = {campo:valor for (campo,valor) in zip(self._column_list,values)}
            self.fromObject(obj=obj)
        else:
            raise Exception(f"values must have the same length of column_list ({len(self._column_list)}):{self._column_list}")

    def toJSON(self):
        """
        Return JSON version of instance
        """
        return json.dumps(self.toObject())
