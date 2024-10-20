from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from datetime import datetime
from decimal import Decimal
from pathlib import Path
import os
import time


"""Класс CarService реализует основные методы для работы
с данными автосалона «Бибип»:
cохранение автомобилей и моделей;
cохранение продаж;
вывод машин, доступных к продаже;
вывод детальной информации по машине;
обновление ключевого поля;
удаление продажи;
вывод самых продаваемых моделей.
"""
class CarService:

    def __init__(self) -> None:
        # Для каждого экземпляра класса CarService
        # будем создавать отдельную папку в родительской папке data.
        # Название папок: bibip + текущая временная метка.
        ct = str(time.time()).replace('.', '')
        dir = f'data/bibip_{ct}'
        Path(dir).mkdir(parents=True, exist_ok=True)
        # Указываем пути к файлам.
        self.models_file_path = f'{dir}/models.txt'
        self.models_index_file_path = f'{dir}/models_index.txt'
        self.cars_file_path = f'{dir}/cars.txt'
        self.cars_index_file_path = f'{dir}/cars_index.txt'
        self.sales_file_path = f'{dir}/sales.txt'
        self.sales_index_file_path = f'{dir}/sales_index.txt'
        # Создадим списки для машин, моделей и продаж.
        # В них будут храниться добавленные в базу экземпляры классов:
        self.cars: list = []
        self.models: list = []
        self.sales: list = []


    """Приватный метод для создания файлов с данными и файлов с индексами:
    file - путь к файлу с данными;
    file_index - путь к файлу с индексами;
    data - список значений для файла с данными;
    key_index - значение, которое используется для ключа в таблице с индекcами;
    type_key_sort - тип поля, по которому будем сортировать данные в файле
    с индексами (например: str, int).
    """
    def __add_data(self, file: str, file_index: str, data: list,
                   key_for_index: str, type_key_sort: str) -> None:
        # Добавляем новую запись в файл с данными.
        with open(file, 'a', encoding='utf-8') as f:
            result = ';'.join(data) + '\n'
            f.write(result)

        # Создаем файл с индексами, если он не существует.
        f = open(file_index, 'a+')
        f.close()

        # Читаем файл с индексами, добавляем новую запись и сортируем данные.
        with open(file_index, 'r') as f:
            # Читаем данные из файла с индексами и записываем в список.
            index_data = [line.split(';') for line in f.read().splitlines()]
            # Расчет номера строки для нового значения:
            row_num = len(index_data)
            # Добавляем новое значение и номер строки в index_data:
            index_data.append([key_for_index, row_num])
            # Сортируем данные по стобцу с ключом:
            if type_key_sort == 'str':
                index_data_sorted = sorted(index_data, key=lambda row: row[0])
            elif type_key_sort == 'int':
                index_data_sorted = sorted(index_data,
                                           key=lambda row: int(row[0]))

        # Перезаписываем файл с индексами.
        with open(file_index, 'w') as f:
            for item in index_data_sorted:
                f.write(str(item[0]) + ';' + str(item[1]) + '\n')

    """Приватный метод для поиска номера строки по ключу
    в таблице с индексами.
    """
    def __get_row_num(self, file_index: str, key_value: str) -> int:
        with open(file_index, 'r') as f:
            for i, line in enumerate(f.read().splitlines()):
                line_list = line.split(';')
                if line_list[0] == key_value:
                    return int(line_list[1])
        # Возвращаем None, если данных нет:
        return None

    """Приватный метод для полной перезаписи файла cars.
    """
    def __rewrite_cars(self):
        # Переписываем файл cars.txt:
        with open(self.cars_file_path, 'w', encoding='utf-8') as f:
            for car in self.cars:
                result = ';'.join([car.vin, str(car.model), str(car.price),
                                   str(car.date_start), str(car.status)]) + '\n'
                f.write(result)

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        # Воспользуемся приватным методом __add_data
        # для добавления данных о моделях машин:
        self.__add_data(file=self.models_file_path,
                        file_index=self.models_index_file_path,
                        data=[str(model.id), model.name, model.brand],
                        key_for_index=str(model.index()),
                        type_key_sort='int'
                        )
        # Добавляем модель в список models:
        self.models.append(model)
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        # Воспользуемся приватным методом __add_data
        # для добавления данных о машине:
        self.__add_data(file=self.cars_file_path,
                        file_index=self.cars_index_file_path,
                        data=[car.vin, str(car.model), str(car.price),
                              str(car.date_start), str(car.status)],
                        key_for_index=str(car.index()),
                        type_key_sort='str'
                        )
        # Добавляем машину в список cars:
        self.cars.append(car)
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        # Воспользуемся приватным методом __add_data
        # для добавления данных о продаже:
        self.__add_data(file=self.sales_file_path,
                        file_index=self.sales_index_file_path,
                        data=[sale.sales_number, sale.car_vin,
                              str(sale.sales_date), str(sale.cost)],
                        key_for_index=str(sale.index()),
                        type_key_sort='str'
                        )
        # Добавляем продажу в список sales:
        self.sales.append(sale)

        # Поиск индекса нужного элемента в списке cars
        # через файл с индексами cars_index.txt:
        row_num_car = self.__get_row_num(file_index=self.cars_index_file_path,
                                         key_value=sale.car_vin)
        # Меняем статус нужной машины на sold:
        self.cars[row_num_car].status = CarStatus.sold

        # Перезаписываем файл cars.txt:
        self.__rewrite_cars()
        return self.cars[row_num_car]

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        # Создаем список, куда будем добавлять машины с нужным статусом:
        result = []
        # Перебираем машины из cars и проверяем статус:
        for car in self.cars:
            if car.status == status:
                result.append(car)
        return result

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # Поиск индекса нужного элемента в списке cars
        # через файл с индексами cars_index.txt:
        row_num_car = self.__get_row_num(file_index=self.cars_index_file_path,
                                         key_value=vin)

        # Если в таблице нет данных по машине, возвращаем None:
        if row_num_car is None:
            return None

        car = self.cars[row_num_car]
        # Записываем нужные данные в переменные:
        car_vin = car.vin
        model_id = car.model
        price = car.price
        date_start = car.date_start
        car_status = car.status

        # Поиск индекса нужного элемента в списке models
        # через файл с индексами models_index.txt:
        row_num_model = self.__get_row_num(file_index=self.models_index_file_path,
                                           key_value=str(model_id))

        # Записываем нужные данные в переменные:
        model_name = self.models[row_num_model].name
        brand = self.models[row_num_model].brand

        # Если файл sales.txt существует:
        if os.path.isfile(self.sales_file_path):
            # Поиск индекса нужного элемента в списке sales
            # через файл с индексами sales_index.txt:
            row_num_sale = self.__get_row_num(file_index=self.sales_index_file_path,
                                              key_value=vin)

            if row_num_sale is None:
                sales_date = None
                sales_cost = None
            else:
                # Записываем нужные данные в переменные:
                sales_date = self.sales[row_num_sale].sales_date
                sales_cost = self.sales[row_num_sale].cost
        else:
            sales_date = None
            sales_cost = None

        # Создаем экземпляр класса CarFullInfo с нужными атрибутами:
        full_info = CarFullInfo(
            vin=car_vin,
            car_model_name=model_name,
            car_model_brand=brand,
            price=price,
            date_start=date_start,
            status=car_status,
            sales_date=sales_date,
            sales_cost=sales_cost
        )
        return full_info

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        # Читаем файл с индексами cars_index.txt:
        with open(self.cars_index_file_path, 'r') as f:
            # Записываем данные в список.
            index_data = [line.split(';') for line in f.read().splitlines()]
            for item in index_data:
                # Находим и заменяем нужный ключ vin:
                if item[0] == vin:
                    item[0] = new_vin
                    # Сохраняем номер строки:
                    row_num_car = int(item[1])
                    # Обрываем цикл:
                    break
            # Сортируем данные по стобцу с ключом.
            index_data_sorted = sorted(index_data, key=lambda row: row[0])

        # Перезаписываем файл с индексами cars_index.txt:
        with open(self.cars_index_file_path, 'w') as f:
            for item in index_data_sorted:
                f.write(str(item[0]) + ";" + str(item[1]) + '\n')

        # Меняем vin у нужной машины из списка cars:
        self.cars[row_num_car].vin = new_vin

        # Перезаписываем файл cars.txt:
        self.__rewrite_cars()
        return self.cars[row_num_car]

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        # Удалим продажу из списка sales:
        for sale in self.sales:
            if sale.sales_number == sales_number:
                # Сохраняем номер машины, по которой была неверная продажа:
                car_vin = sale.car_vin
                self.sales.remove(sale)
                break

        # Очистим файлы sales.txt и sales_index.txt
        # для того, чтобы перезаписать данные.
        with open(self.sales_file_path, 'w'):
            pass

        with open(self.sales_index_file_path, 'w'):
            pass

        # Перезаписываем данные в файлы sales.txt и sales_index.txt:
        for sale in self.sales:
            self.__add_data(file=self.sales_file_path,
                            file_index=self.sales_index_file_path,
                            data=[sale.sales_number, sale.car_vin,
                                  str(sale.sales_date), str(sale.cost)],
                            key_for_index=str(sale.index()),
                            type_key_sort='str'
                            )

        # Поиск индекса нужного элемента в списке cars
        # через файл с индексами cars_index.txt:
        row_num_car = self.__get_row_num(file_index=self.cars_index_file_path,
                                         key_value=car_vin)

        # Меняем статус машины на available:
        self.cars[row_num_car].status = CarStatus.available

        # Перезаписываем файл cars.txt:
        self.__rewrite_cars()
        return self.cars[row_num_car]

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        # Создаем список, куда будем записывать топ 3 продаваемых модели:
        result = []
        # Создадим список, где каждый элемент будет списком
        # с параметрами продаж:
        data_sales = []
        for sale in self.sales:
            data_sales.append([sale.sales_number, sale.car_vin, sale.cost])

        # Для каждой продажи добавим модель и бренд машины.
        for sale in data_sales:
            # Поиск индекса нужного элемента в списке cars
            # через файл с индексами cars_index.txt:
            row_num_car = self.__get_row_num(file_index=self.cars_index_file_path,
                                             key_value=sale[1])

            # Находим ID модели:
            model_id = self.cars[row_num_car].model

            # Поиск индекса нужного элемента в списке models
            # через файл с индексами models_index.txt:
            row_num_model = self.__get_row_num(file_index=self.models_index_file_path,
                                               key_value=str(model_id))

            model = self.models[row_num_model]
            # Добавляем нужные значения в список sale:
            sale += [model.name, model.brand]

        # Создаем словарь, где для каждой модели будем записать
        # число продаж и максимальную цену продажи.
        sales_dict: dict = {}
        for sale in data_sales:
            (sales_number, car_vin, cost, model_name, brand_name) = sale
            if (model_name, brand_name) not in sales_dict.keys():
                # Если модели нет в словаре, добавляем данные по ней:
                # число продаж = 1, стоимость cost:
                sales_dict[(model_name, brand_name)] = [1, Decimal(cost)]
            else:
                # Если модель есть в словаре, то увеличиваем число продаж на 1:
                sales_dict[(model_name, brand_name)][0] += 1
                # Сохраняем в словаре максимальную цену для модели:
                if Decimal(cost) > sales_dict[(model_name, brand_name)][1]:
                    sales_dict[(model_name, brand_name)][1] = Decimal(cost)
        # Сортируем словарь по убыванию числа продаж и стоимости модели:
        sales_list_sorted = sorted(sales_dict.items(),
                                   key=lambda x: (x[1][0], x[1][1]),
                                   reverse=True)
        # Топ 3 модели по продажам:
        top_3_models = sales_list_sorted[:3]
        for model in top_3_models:
            # Добавляем информацию о продаже модели в result:
            result.append(ModelSaleStats(
                                    car_model_name=model[0][0],
                                    brand=model[0][1],
                                    sales_number=model[1][0]
                                    ))
        return result
