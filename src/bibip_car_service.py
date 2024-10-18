from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale
from datetime import datetime
from decimal import Decimal


class CarService:

    def __init__(self) -> None:
        # Указываем пути к файлам.
        self.models_file_path = "C:/Users/79035/ProjectsYandex/bibip_txt/models.txt"
        self.models_index_file_path = "C:/Users/79035/ProjectsYandex/bibip_txt/models_index.txt"
        self.cars_file_path = "C:/Users/79035/ProjectsYandex/bibip_txt/cars.txt"
        self.cars_index_file_path = "C:/Users/79035/ProjectsYandex/bibip_txt/cars_index.txt"
        self.sales_file_path = "C:/Users/79035/ProjectsYandex/bibip_txt/sales.txt"
        self.sales_index_file_path = "C:/Users/79035/ProjectsYandex/bibip_txt/sales_index.txt"

    """Приватный метод для создания файлов с данными и файлов с индексами.
    file - путь к файлу с данными
    file_index - путь к файлу с индексами
    data - список значений для файла с данными
    key_index - значение, которое используется для ключа в таблице с индекcами
    type_key_sort - тип поля, по которому будем сортировать данные в файле
    с индексами (str, int)
    """
    def __add_data(self, file, file_index, data, key_for_index, type_key_sort):
        # Добавляем новую запись в файл с данными.
        with open(file, 'a', encoding='utf-8') as f:
            result = ';'.join(data) + '\n'
            f.write(result)

        # Создаем файл с индексами, если он не существует.
        # Иначе последующий код с чтением файла выдает ошибку.
        f = open(file_index, 'a+')
        f.close()

        # Читаем файл с индексами, добавляем новую запись и сортируем данные.
        with open(file_index, 'r') as f:
            # Читаем данные из файла с индексами и записываем в список.
            index_data = [line.split(';') for line in f.read().splitlines()]
            index_data.append([key_for_index, str(len(index_data))])
            # Сортируем данные по стобцу с ключом.
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
    в файле с индексами.
    """
    def __get_row_num(self, file_index, key_value):
        with open(file_index, 'r') as f:
            for i, line in enumerate(f.read().splitlines()):
                line_list = line.split(';')
                if line_list[0] == key_value:
                    return int(line_list[1])
        # Возвращаем None, если данных нет:
        return None

    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        self.__add_data(file=self.models_file_path,
                        file_index=self.models_index_file_path,
                        data=[str(model.id), model.name, model.brand],
                        key_for_index=str(model.index()),
                        type_key_sort='int'
                        )
        return model

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        self.__add_data(file=self.cars_file_path,
                        file_index=self.cars_index_file_path,
                        data=[car.vin, str(car.model), str(car.price),
                              str(car.date_start), str(car.status)],
                        key_for_index=str(car.index()),
                        type_key_sort='str'
                        )
        return car

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        self.__add_data(file=self.sales_file_path,
                        file_index=self.sales_index_file_path,
                        data=[sale.sales_number, sale.car_vin,
                              str(sale.sales_date), str(sale.cost)],
                        key_for_index=str(sale.index()),
                        type_key_sort='str'
                        )
        
        # Поиск номера нужной строки для файла cars.txt:
        row_num_car = self.__get_row_num(file_index=self.cars_index_file_path,
                                         key_value=sale.car_vin)
        # Читаем файл cars.txt:
        with open(self.cars_file_path, 'r') as f:
            # Записываем данные в список.
            data = [line.split(';') for line in f.read().splitlines()]
            # Находим нужную строку и заменяем статус:
            data[row_num_car][4] = 'sold'
            car = Car(
                    vin=data[row_num_car][0],
                    model=int(data[row_num_car][1]),
                    price=Decimal(data[row_num_car][2]),
                    date_start=datetime.strptime(data[row_num_car][3], '%Y-%m-%d %H:%M:%S'),
                    status=CarStatus.sold
                )

        # Перезаписываем файл с данными cars.txt:
        with open(self.cars_file_path, 'w') as f:
            for item in data:
                f.write(';'.join(item) + '\n')

        return car

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        # Читаем файл с данными по машинам cars.txt.
        with open(self.cars_file_path, 'r') as f:
            # Записываем все данные в список.
            data = [line.split(';') for line in f.read().splitlines()]
            result = [] # Создаем список, куда будем записывать результат
            for item in data:
                # Если у машины нужный статус, создаем экземпляр класса Car
                # и добавляем его в список result.
                if item[4] == status:
                    car = Car(
                            vin=item[0],
                            model=int(item[1]),
                            price=Decimal(item[2]),
                            date_start=datetime.strptime(item[3], '%Y-%m-%d %H:%M:%S'),
                            status=CarStatus.available
                        )
                    result.append(car)
        return result

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        # Находим номер строки в файле cars.txt, которому соответсвует
        # значение vin.
        row_num_car = self.__get_row_num(file_index=self.cars_index_file_path,
                                         key_value=vin)

        # Открываем на чтение файл cars.txt.
        with open(self.cars_file_path, 'r') as f:
            for i, line in enumerate(f.read().splitlines()):
                # Находим нужную строку:
                if i == row_num_car:
                    line_list = line.split(';')
                    # Записываем нужные данные в переменные:
                    car_vin = line_list[0]
                    model_id = line_list[1]
                    price = Decimal(line_list[2])
                    date_start = datetime.strptime(line_list[3], '%Y-%m-%d %H:%M:%S')
                    car_status = CarStatus(line_list[4])
                    # Обрываем цикл:
                    break

        # Находим номер строки в файле models.txt, которому соответсвует
        # значение model_id из коды выше.
        row_num_model = self.__get_row_num(file_index=self.models_index_file_path,
                                           key_value=model_id)

        # Открываем на чтение файл models.txt.
        with open(self.models_file_path, 'r') as f:
            for i, line in enumerate(f.read().splitlines()):
                # Находим нужную строку:
                if i == row_num_model:
                    line_list = line.split(';')
                    # Записываем нужные данные в переменные:
                    model_name = line_list[1]
                    brand = line_list[2]
                    # Обрываем цикл:
                    break

        # Находим номер строки в файле sales.txt, которому соответсвует
        # значение vin.
        row_num_sale = self.__get_row_num(file_index=self.sales_index_file_path,
                                          key_value=vin)

        if row_num_sale == None:
            sales_date = None
            sales_cost = None
        else:
            # Открываем на чтение файл sales.txt.
            with open(self.sales_file_path, 'r') as f:
                for i, line in enumerate(f.read().splitlines()):
                    # Находим нужную строку:
                    if i == row_num_sale:
                        line_list = line.split(';')
                        # Записываем нужные данные в переменные:
                        sales_date = datetime.strptime(line_list[2], '%Y-%m-%d %H:%M:%S')
                        sales_cost = Decimal(line_list[3])
                        # Обрываем цикл:
                        break

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
                    # Сохраним нужную строку для cars.txt:
                    row_num_car = int(item[1])
            # Сортируем данные по стобцу с ключом.
            index_data_sorted = sorted(index_data, key=lambda row: row[0])

        # Перезаписываем файл с индексами cars_index.txt:
        with open(self.cars_index_file_path, 'w') as f:
            for item in index_data_sorted:
                f.write(str(item[0]) + ";" + str(item[1]) + '\n')

        # Читаем файл с данными cars.txt:
        with open(self.cars_file_path, 'r') as f:
            # Записываем данные в список.
            data = [line.split(';') for line in f.read().splitlines()]
            # Находим нужную строку и заменяем значение vin:
            data[row_num_car][0] = new_vin
            car = Car(
                    vin=new_vin,
                    model=int(data[row_num_car][1]),
                    price=Decimal(data[row_num_car][2]),
                    date_start=datetime.strptime(data[row_num_car][3], '%Y-%m-%d %H:%M:%S'),
                    status=CarStatus(data[row_num_car][4])
                )

        # Перезаписываем файл с данными cars.txt:
        with open(self.cars_file_path, 'w') as f:
            for item in data:
                f.write(';'.join(item) + '\n')
        return car

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        with open(self.sales_file_path, 'r') as f:
            # Записываем данные в список.
            data = [line.split(';') for line in f.read().splitlines()]
            for item in data:
                if item[0] == sales_number:
                    car_vin = item[1]
                    data.remove(item)
                    break

        # Перезаписываем файл с данными cars.txt:
        with open(self.sales_file_path, 'w') as f:
            for item in data:
                f.write(';'.join(item) + '\n')

        # Находим номер строки в файле cars.txt, которому соответсвует
        # значение vin.
        row_num_car = self.__get_row_num(file_index=self.cars_index_file_path,
                                         key_value=car_vin)

        # Читаем файл с данными cars.txt:
        with open(self.cars_file_path, 'r') as f:
            # Записываем данные в список.
            data = [line.split(';') for line in f.read().splitlines()]
            # Находим нужную строку и заменяем статус:
            data[row_num_car][4] = 'available'
            car = Car(
                    vin=data[row_num_car][0],
                    model=int(data[row_num_car][1]),
                    price=Decimal(data[row_num_car][2]),
                    date_start=datetime.strptime(data[row_num_car][3], '%Y-%m-%d %H:%M:%S'),
                    status=CarStatus.available
                )

        # Перезаписываем файл с данными cars.txt:
        with open(self.cars_file_path, 'w') as f:
            for item in data:
                f.write(';'.join(item) + '\n')
        return car

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        return None



# ТЕСТЫ
car_1 = Car(
        vin="KNAGM4A77D5316538",
        model=1,
        price=Decimal("2000"),
        date_start=datetime(2024, 2, 8),
        status=CarStatus.sold,
    )

car_2 = Car(
        vin="5XYPH4A10GG021831",
        model=2,
        price=Decimal("2300"),
        date_start=datetime(2024, 2, 20),
        status=CarStatus.reserve,
    )

car_3 = Car(
        vin="KNAGH4A48A5414970",
        model=1,
        price=Decimal("2100"),
        date_start=datetime(2024, 4, 4),
        status=CarStatus.available,
    )

car_4 = Car(
        vin="JM1BL1TFXD1734246",
        model=3,
        price=Decimal("2276.65"),
        date_start=datetime(2024, 5, 17),
        status=CarStatus.available,
    )

car_5 = Car(
        vin="JM1BL1M58C1614725",
        model=3,
        price=Decimal("2549.10"),
        date_start=datetime(2024, 5, 17),
        status=CarStatus.reserve,
    )

car_6 = Car(
        vin="KNAGR4A63D5359556",
        model=1,
        price=Decimal("2376"),
        date_start=datetime(2024, 5, 17),
        status=CarStatus.available,
    )

car_7 = Car(
        vin="5N1CR2MN9EC641864",
        model=4,
        price=Decimal("3100"),
        date_start=datetime(2024, 6, 1),
        status=CarStatus.available,
    )

car_8 = Car(
        vin="JM1BL1L83C1660152",
        model=3,
        price=Decimal("2635.17"),
        date_start=datetime(2024, 6, 1),
        status=CarStatus.available,
    )

car_9 = Car(
        vin="5N1CR2TS0HW037674",
        model=4,
        price=Decimal("3100"),
        date_start=datetime(2024, 6, 1),
        status=CarStatus.available,
    )

car_10 = Car(
        vin="5N1AR2MM4DC605884",
        model=4,
        price=Decimal("3200"),
        date_start=datetime(2024, 7, 15),
        status=CarStatus.available,
    )
    
car_11 = Car(
        vin="VF1LZL2T4BC242298",
        model=5,
        price=Decimal("2280.76"),
        date_start=datetime(2024, 8, 31),
        status=CarStatus.delivery,
    )

model_1 = Model(id=1, name="Optima", brand="Kia")
model_2 = Model(id=2, name="Sorento", brand="Kia")
model_3 = Model(id=3, name="3", brand="Mazda")
model_4 = Model(id=4, name="Pathfinder", brand="Nissan")
model_5 = Model(id=5, name="Logan", brand="Renault")

sale_1 = Sale(
    sales_number="20240903#JM1BL1M58C1614725",
    car_vin="JM1BL1M58C1614725",
    sales_date=datetime(2024, 9, 3),
    cost=Decimal("2399.99"),
)

service = CarService()

service.add_model(model_1)
service.add_model(model_2)
service.add_model(model_3)
service.add_model(model_4)
service.add_model(model_5)

service.add_car(car_1)
service.add_car(car_2)
service.add_car(car_3)
service.add_car(car_4)
service.add_car(car_5)
service.add_car(car_6)
service.add_car(car_7)
service.add_car(car_8)
service.add_car(car_9)
service.add_car(car_10)
service.add_car(car_11)

service.sell_car(sale_1)

print(service.get_cars(status='available'))

print('------------------------')
print(service.get_car_info(vin='KNAGM4A77D5316538'))


print(service.update_vin("KNAGM4A77D5316538", "UPDGM4A77D5316538"))