import logging
from typing import List

import aiosqlite


class AsyncSession:
    def __init__(self, db_name: str):
        self.db_name = db_name + ".db" if db_name[-3:] != ".db" else db_name
        self.__conn: None | aiosqlite.Connection = None

    async def create_table(self, table_name: str, table_columns: dict[str: str]) -> None | int:
        """
        Creates a table in the database
        Example table_columns: {'id': 'INTEGER PRIMARY KEY', 'name': 'TEXT', 'age': 'INTEGER'}
        :param table_name:
        :param table_columns:
        :return:
        """
        self.__conn = await aiosqlite.connect(self.db_name)
        query = f"CREATE TABLE {table_name} ({', '.join(f'{k} {v}' for k, v in table_columns.items())})"
        await self.__conn.execute(query)
        await self.__conn.commit()
        logging.debug(f"Created table {table_name}. No errors.")
        return 0

    @property
    def conn(self):
        return self.__conn

    async def select(self, table_name: str, count: int, where: dict[str: str] = None):
        """
        Selects the first element from the given table if exists
        :param table_name:
        :param count:
        :param where:
        :return:
        """
        self.__conn = await aiosqlite.connect(self.db_name)
        if where is not None:
            where = await self._validate_params(where)
            selection = await self.__conn.execute(
                f"SELECT * FROM {table_name} WHERE {' AND '.join(f'{k} = {v}' for k, v in where[0].items())}")
        else:
            selection = await self.__conn.execute(f"SELECT * FROM {table_name}")
        return await selection.fetchmany(count)

    async def save(self, table_name: str, values: List) -> None:
        """
        Inserts a new row into the given table
        :param table_name:
        :param values:
        :return:
        """
        self.__conn = await aiosqlite.connect(self.db_name)
        values = await self._validate_params(values)
        try:
            await self.__conn.execute(f"INSERT INTO {table_name} VALUES ({', '.join(values[0])})")
            await self.__conn.commit()
        except aiosqlite.IntegrityError as e:
            raise aiosqlite.IntegrityError(
                "Tried to modify a primary key {}".format(e.__str__()[e.__str__().find(":"):]))

    async def update(self, table_name: str, values: dict[str: str], where: dict) -> None:
        """
        Updates a row in the given table
        :param table_name:
        :param values:
        :param where:
        :return:
        """
        self.__conn = await aiosqlite.connect(self.db_name)
        values, where = await self._validate_params(values, where)
        for k, v in values.items():
            query = f"UPDATE {table_name} SET {k} = {v} WHERE {' AND '.join(f'{q} = {x}' for q, x in where.items())}"
            await self.__conn.execute(query)
            await self.__conn.commit()

    async def delete(self, table_name: str, where: dict[str: str]) -> None:
        """
        Deletes a row from the given table
        :param table_name:
        :param where:
        :return:
        """
        self.__conn = await aiosqlite.connect(self.db_name)
        where = await self._validate_params(where)
        await self.__conn.execute(
            f"DELETE FROM {table_name} WHERE {' AND '.join(f'{k} = {v}' for k, v in where[0].items())}")
        await self.__conn.commit()

    async def close(self) -> None:
        """
        Closes the connection to the database
        :return:
        """
        return await self.__conn.close()

    def __repr__(self):
        return f"<DB: {self.db_name}>"

    @staticmethod
    async def _validate_params(*args):
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
