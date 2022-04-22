import logging
import sqlite3
from typing import Iterable, List, Optional, Tuple


class Session:
    def __init__(self, db_name: str):
        self.db_name = db_name + ".db" if db_name[-3:] != ".db" else db_name
        self.__conn = sqlite3.connect(self.db_name)
        self.__c = self.__conn.cursor()

    def create_table(self, table_name: str, table_columns: dict[str: str]) -> None | int:
        """
        Creates a table in the database
        Example table_columns: {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT', 'age': 'INTEGER'}
        :param table_name:
        :param table_columns:
        :return:
        """
        query = f"CREATE TABLE {table_name} ({', '.join(f'{k} {v}' for k, v in table_columns.items())})"
        self.__c.execute(query)
        self.__conn.commit()
        logging.debug(f"Created table {table_name}. No errors.")
        return 0

    @property
    def cursor(self):
        return self.__c

    @property
    def conn(self):
        return self.__conn

    def save(self, table_name: str, count: int, where: dict[str: str] = None) -> List[Tuple]:
        """
        Selects the first element from the given table if exists
        :param table_name:
        :param count:
        :param where:
        :return:
        """
        if where is not None:
            where = self._validate_params(where)
        if where is not None:
            self.__c.execute(
                f"SELECT * FROM {table_name} WHERE {' AND '.join(f'{k} = {v}' for k, v in where[0].items())}")
        else:
            self.__c.execute(f"SELECT * FROM {table_name}")
        return self.__c.fetchmany(count)

    def insert(self, table_name: str, values: List) -> None:
        """
        Inserts a new row into the given table
        :param table_name:
        :param values:
        :return:
        """
        values = self._validate_params(values)
        try:
            self.__c.execute(f"INSERT INTO {table_name} VALUES ({', '.join(values[0])})")
            self.__conn.commit()
        except sqlite3.IntegrityError as e:
            raise sqlite3.IntegrityError("Tried to modify a primary key {}".format(e.__str__()[e.__str__().find(":"):]))

    def update(self, table_name: str, values: dict[str: str], where: dict) -> None:
        """
        Updates a row in the given table
        :param table_name:
        :param values:
        :param where:
        :return:
        """
        values, where = self._validate_params(values, where)
        for k, v in values.items():
            query = f"UPDATE {table_name} SET {k} = {v} WHERE {' AND '.join(f'{q} = {x}' for q, x in where.items())}"
            self.__c.execute(query)
            self.__conn.commit()

    def delete(self, table_name: str, where: dict[str: str]) -> None:
        """
        Deletes a row from the given table
        :param table_name:
        :param where:
        :return:
        """
        where = self._validate_params(where)
        self.__c.execute(
            f"DELETE FROM {table_name} WHERE {' AND '.join(f'{k} = {v}' for k, v in where[0].items())}")
        self.__conn.commit()

    def close(self) -> None:
        """
        Closes the connection to the database
        :return:
        """
        self.__conn.close()

    def __del__(self):
        self.__conn.commit()
        self.__conn.close()

    def __repr__(self):
        return f"<DB: {self.db_name}>"

    @staticmethod
    def _validate_params(*args):
        for arg in args:
            try:
                for _, v in arg.items():
                    if isinstance(v, str):
                        arg[_] = f"'{v}'"
            except AttributeError:
                for i, v in enumerate(arg):
                    if isinstance(v, str):
                        arg[i] = f"'{v}'"

        return args
