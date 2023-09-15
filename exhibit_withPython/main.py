import sys
from array import array

sys.path.append('tables')

from project_config import *
from dbconnection import *
from tables.collection_table import *
from tables.exhibit_table import *

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        ct = CollectionTable()
        et = ExhibitsTable()
        ct.create()
        et.create()
        return

    def db_insert_somethings(self):
        ct = CollectionTable()
        et = ExhibitsTable()
        ct.insert_one(["Test1", "Test1"])
        ct.insert_one(["Test2", "Test2"])
        ct.insert_one(["Test3", "Test3"])
        et.insert_one(["Test1", "Test1", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, '0'])
        et.insert_one(["Test2", "Test2", 2, 2, 2, 2, 2, 2, 2, 3, 4, 25, '1'])
        et.insert_one(["Test3", "Test1", 3, 3, 3, 3, 15, 32, 43, 17, 28, 14, '0'])

    def db_drop(self):
        ct = CollectionTable()
        et = ExhibitsTable()
        et.drop()
        ct.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать!
Основное меню (выберите цифру в соответствии с необходимым действием):
    1 - просмотр коллекции;
    2 - сброс и инициализация таблиц;
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_collections(self):
        self.colletion_id = -1
        menu = """Просмотр списка коллекции!
id\tname\tshort_describe"""
        print(menu)
        lst = CollectionTable().all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    3 - добавление нового коллекции;
    4 - удаление коллекции;
    5 - просмотр экспонатов коллекции;
    10 - Измениние коллекции;
    9 - выход."""
        print(menu)
        return

    def insert_exhibits_by_collecion(self):
        if self.colletion_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас коллекции (0 - отмена):")
                while len(num.strip()) == 0:
                    num = input(
                        "Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                if num == "0":
                    return "1"
                collection = CollectionTable().find_by_position(int(num))
                if not collection:
                    print("Введено число, неудовлетворяющее количеству коллекции!")
                else:
                    self.colletion_id = int(collection[0])
                    self.collection_obj = collection
                    break
        data = []
        data.append(input("Введите name (-1 - отмена): ").strip())
        if data[0] == "-1":
            return
        while len(data[0].strip()) == 0 or len(data[0].strip()) > 64:
            data[0] = input("Имя не может быть пустым или более 64! Введите имя заново (-1 - отмена):").strip()
            if data[0] == "-1":
                return
        data.append(input("Введите short_describe (-1 - отмена): ").strip())
        if data[1] == "-1":
            return
        while len(data[1].strip()) > 128:
            data[1] = input("Имя не может быть более 128! Введите short_describe заново (-1 - отмена):").strip()
            if data[1] == "-1":
                return

        data.append(input("Введите insurance_value (-1 - отмена): ").strip())
        if data[2] == "-1":
            return
        while len(data[2].strip())==0 or not data[2].isdecimal():
            data[2] = input("insurance_value не может быть пустым и дольжен быть числом! Введите insurance_value заново (-1 - отмена):").strip()
            if data[2] == "-1":
                return
        data[2]=int(data[2])
        data.append(input("Введите century (-1 - отмена): ").strip())
        if data[3] == "-1":
            return
        while len(data[3].strip()) == 0 or not data[3].isnumeric():
            data[3] = input(
                "century не может быть пустым и дольжен быть числом! Введите century заново (-1 - отмена):").strip()
            if data[3] == "-1":
                return
        data[3]=int(data[3])
        data.append(self.colletion_id)
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(0)
        data.append(input("Введите protec_people  1 or 0?(-1 - отмена): ").strip())
        if data[12] == '-1':
            return
        while data[12] != '1' and data[12] != '0':
            data[12] = input("protec_people дольжен быть 1 или 0! Введите protec_people заново (-1 - отмена):").strip()
            print(data[12])
            if data[12] == '-1':
                return
        print(data)
        ExhibitsTable().insert_one(data)


    def after_show_collecions(self, next_step):
        while True:
            if next_step == "4":
                self.colletion_id = input("input collection_id: ").strip()
                ct =CollectionTable()
                ct.del_collection(self.colletion_id)
                return "1"
            elif next_step == "6":
                self.insert_exhibits_by_collecion()
                next_step = "5"
            elif next_step == "7":
                a = input("input exhibits_id: ").strip()
                ExhibitsTable().del_exhibit(a)
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_exhibits_by_collection()
            elif next_step == "10":
                self.change_collection()
                next_step = "5"
            elif next_step == "11":
                self.change_exhibit()
                next_step = "5"
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"

            else:
                return next_step

    def show_add_collection(self):
        # Не реализована проверка на максимальную длину строк. Нужно доделать самостоятельно!
        data = []
        data.append(input("Введите имя (-1 - отмена): ").strip())
        if data[0] == "-1":
            return
        while len(data[0].strip()) == 0 or len(data[0].strip())>64:
            data[0] = input("Имя не может быть пустым или более 64! Введите имя заново (-1 - отмена):").strip()
            if data[0] == "-1":
                return
        data.append(input("Введите short_describe (-1 - отмена): ").strip())
        if data[1] == "-1":
            return
        while len(data[1].strip()) == 0 or len(data[1].strip()) > 128:
            data[1] = input("short_describe не может быть пустой или более 64! Введите short_describe заново (-1 - отмена):").strip()
            if data[1] == "-1":
                return
        CollectionTable().insert_one(data)
        return

    def show_exhibits_by_collection(self):
        if self.colletion_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас коллекции (0 - отмена):")
                while len(num.strip()) == 0:
                    num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                if num == "0":
                    return "1"
                collection = CollectionTable().find_by_position(int(num))
                if not collection:
                    print("Введено число, неудовлетворяющее количеству коллекции!")
                else:
                    self.colletion_id = int(collection[0])
                    self.collection_obj = collection
                    break
        print("Выбран коллекции: " + " " + self.collection_obj[1] + " " + self.collection_obj[2])
        print("Exhibits:")
        lst = ExhibitsTable().all_by_collection_id(self.colletion_id)
        print("id\tname\tshort_describe\tcollection_id\tprotec_people")
        for i in lst:
            print(str(i[0])+"\t"+i[1]+"\t"+i[2]+"\t"+str(i[5])+"\t"+str(i[13]))
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр коллекции;
    6 - добавление нового экспонаты;
    7 - удаление экспонаты;
    10 - измениние коллекции;
    11 - измениние экспонаты;
    9 - выход."""
        print(menu)
        return self.read_next_step()


    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.colletion_id=-1
                self.collection_obj= None
                self.show_collections()
                next_step = self.read_next_step()
                current_menu = self.after_show_collecions(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_collection()
                current_menu = "1"
        print("До свидания!")
        return

    def test(self):
        DbTable.dbconn.test()

    def change_collection(self):
        if self.colletion_id == -1:
            while True:
                num = input("Укажите номер строки, в которой записана интересующая Вас коллекции (0 - отмена):")
                while len(num.strip()) == 0:
                    num = input(
                        "Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас персона (0 - отмена):")
                if num == "0":
                    return "1"
                collection = CollectionTable().find_by_position(int(num))
                if not collection:
                    print("Введено число, неудовлетворяющее количеству коллекции!")
                else:
                    self.colletion_id = int(collection[0])
                    self.collection_obj = collection
                    break
        print("Do you want to change this collection?: ")
        print(self.collection_obj)
        arr = list(self.collection_obj)
        a = input("input name (-1 if don't change it) name=").strip()
        while len(a) == 0 or len(a) > 64:
            a = input("name не может быть пустой или более 64! Введите name заново (-1 if don't change it:").strip()
        if a != '-1':
            arr[1] = a

        a = input("input short_describe (-1 if don't change it) short_describe=").strip()
        while len(a) == 0 or len(a) > 128:
            a = input("short_describe не может быть пустой или более 128! Введите short_describe заново (-1 - if don't change it):").strip()
        if a != '-1':
            arr[2] = a
        CollectionTable().change_collection(arr)
        return

    def change_exhibit(self):
        if self.colletion_id == -1:
            print("не возможно!")
            return
        while True:
            num = input("Укажите номер строки, в которой записана интересующая Вас экспонаты (0 - отмена):")
            if num == "0": return
            while len(num.strip()) == 0:
                num = input("Пустая строка. Повторите ввод! Укажите номер строки, в которой записана интересующая Вас экспонаты (0 - отмена):")
                if num == "0":
                    return "1"
            exhibit = ExhibitsTable().find_by_position(int(num), self.colletion_id)
            if not exhibit:
                print("Введено число, неудовлетворяющее количеству экспонаты!")
            else:
                self.exhibit_obj = exhibit
                break
        print("Do you want to change this exhibit?: ")
        print(self.exhibit_obj)
        arr = list(self.exhibit_obj)
        a = input("input name (-1 if don't change it) name=").strip()
        while len(a) == 0 or len(a) > 64:
            a = input("name не может быть пустой или более 64! Введите name заново (-1 if don't change it:").strip()
        if a != '-1':
            arr[1] = a

        a = input("input short_describe (-1 if don't change it) short_describe=").strip()
        while len(a) > 128:
            a = input("short_describe не может быть более 128! Введите short_describe заново (-1 - if don't change it):").strip()
        if a != '-1':
            arr[2] = a

        a = input("input protec_people 0 or 1 (-1 if don't change it) protec_people=").strip()
        while a != '1' and a != '0' and a != '-1':
            a = input("protec_people дольжен быть 1 или 0! Введите protec_people заново (-1 - don't change it):").strip()
        if a != '-1':
            arr[13] = a
        ExhibitsTable().change_exhibit(arr)
        return

m = Main()
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
# m.test()
m.main_cycle()

