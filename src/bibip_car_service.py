from models import Car, CarFullInfo, CarStatus, Model, ModelSaleStats, Sale


class CarService:

    def __init__(self) -> None:
        self.models_file_path = "./models.txt"
        self.models_index_file_path = "./models_index.txt"
        self.cars_file_path = "./cars.txt"
        self.cars_index_file_path = "./cars_index.txt"


    # Общая функция для Задании 1-2.
    def add_data(self, file, file_index, fields_list, field_index):
        # Открываем файл для добавления нового содержимого.
        with open(file, 'a', encoding='utf-8') as f:
            result = ';'.join(fields_list) + '\n'
            f.write(result)
        
        # Создаем файл с индексами, если он не существует.
        f = open(file_index, 'a+')
        
        # Читаем файл с индексами, добавляем и сортируем записи.
        with open(file_index, 'r') as f:
            index_data = [line.split(';') for line in f.read().splitlines()]
            index_data.append([field_index, str(len(index_data) + 1)])
            index_data_sorted = sorted(index_data, key=lambda row: row[0])
            print(index_data)
        
        # Перезаписываем файл с индексами.
        with open(file_index, 'w') as f:
            for item in index_data_sorted:
                f.write(str(item[0]) + ";" + str(item[1]) + '\n')
    
    
    # Задание 1. Сохранение автомобилей и моделей
    def add_model(self, model: Model) -> Model:
        self.add_data(file=self.models_file_path,
                      file_index=self.models_index_file_path,
                      fields_list=[str(model.id), model.name, model.brand],
                      field_index=str(model.index())
                )

    # Задание 1. Сохранение автомобилей и моделей
    def add_car(self, car: Car) -> Car:
        self.add_data(file=self.cars_file_path,
                      file_index=self.cars_index_file_path,
                      fields_list=[car.vin, str(car.model), str(car.price),
                            str(car.date_start), str(car.status)],
                      field_index=str(car.index())
                )


        raise NotImplementedError

    # Задание 2. Сохранение продаж.
    def sell_car(self, sale: Sale) -> Car:
        raise NotImplementedError

    # Задание 3. Доступные к продаже
    def get_cars(self, status: CarStatus) -> list[Car]:
        raise NotImplementedError

    # Задание 4. Детальная информация
    def get_car_info(self, vin: str) -> CarFullInfo | None:
        raise NotImplementedError

    # Задание 5. Обновление ключевого поля
    def update_vin(self, vin: str, new_vin: str) -> Car:
        raise NotImplementedError

    # Задание 6. Удаление продажи
    def revert_sale(self, sales_number: str) -> Car:
        raise NotImplementedError

    # Задание 7. Самые продаваемые модели
    def top_models_by_sales(self) -> list[ModelSaleStats]:
        raise NotImplementedError
