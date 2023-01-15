import os
import tempfile
import uuid

__all__ = ['File']


class File:
    __folder: str = tempfile.gettempdir()
    __path_file: str = None

    def __init__(self, path_to_file: str):
        if not isinstance(path_to_file, str) or path_to_file == '':
            raise TypeError("[file_name] must be only str")

        if not os.path.exists(path_to_file):
            self.create_new_file(path_to_file)
            # print('Creating', path_to_file)

        self.__path_file = path_to_file

    def __add__(self, other):
        new_file_name = os.path.join(tempfile.gettempdir(), str(uuid.uuid4()))

        new_file = File(new_file_name)
        new_file.write(self.read() + other.read())

        return new_file

    def __iter__(self):
        self.lst_lines = self.read_lines()
        self.iterable_number = 0
        return self

    def __next__(self):

        try:
            return self.lst_lines[self.iterable_number]
        except IndexError:
            raise StopIteration
        finally:
            self.iterable_number += 1

    def __str__(self):
        return self.__path_file

    def read(self):
        with open(file=self.__path_file, mode='r', encoding="utf-8") as read_file:
            return read_file.read()

    def read_lines(self):
        with open(file=self.__path_file, mode='r', encoding="utf-8") as read_file:
            return read_file.readlines()

    def write(self, new_str: str) -> int:

        if not isinstance(new_str, str):
            print(f"new_str in {self.__class__} is not str")
            return -1

        try:
            with open(file=self.__path_file, mode='w', encoding="utf-8") as write_file:
                # print("writing", self.__path_file)
                write_file.write(new_str)
        except Exception() as e:
            print(e)
            return -1

        return len(new_str)

    @staticmethod
    def create_new_file(file_name: str) -> None:
        open(file=file_name, mode='w').close()


if __name__ == "__main__":
    file_name = os.path.join(tempfile.gettempdir(), "some_filename")

    first_file = File(file_name + '_1')
    second_file = File(file_name + '_2')

    first_file.write("line 1\n")
    second_file.write("line 2\n")

    new_file = first_file + second_file

    print(new_file.read())

    for line in new_file:
        print(line)
