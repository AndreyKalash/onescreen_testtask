import pandas as pd


class DataExtractor:
    def __init__(self, file_path: str) -> None:
        """
        Инициализация класса DataExtractor

        :param file_path: Путь к файлу в формате JSON
        """
        self.file_path = file_path
        self.df = pd.read_json(file_path)

    def extract_data(self) -> None:
        """
        Основной метод для извлечения и обработки данных из JSON-файла.
        """
        # получаем количество айтемов
        self.df["count_item"] = self.df["items"].apply(lambda x: len(x))
        # разбиваем коллекции
        self.df = self.df.explode("items").explode("services", True)
        # переименовываем столбец
        self.df.rename(columns={"operation_type": "type_operation"}, inplace=True)
        # меняем NaN на пустые словари для дальнейшего удобства
        self.df["services"] = self.fillna_dicts("services")
        self.df["items"] = self.fillna_dicts("items")
        # получаем нужные значения из столбцов хранящих в себе словари
        self.df["posting_number"] = self.get_from_dict_col("posting", "posting_number")
        self.df["delivery_schema"] = self.get_from_dict_col("posting", "delivery_schema")
        self.df["name"] = self.get_from_dict_col("services", "name")
        self.df["price"] = self.get_from_dict_col("services", "price")
        self.df["article"] = self.get_from_dict_col("items", "name")
        self.df["sku"] = self.get_from_dict_col("items", "sku")
        # расчитываем total_price
        self.df["total_price"] = self.df.apply(self.get_total_price, axis=1)
        # расчитываем количество уникальных sku
        # делаем группировку по operation_id и находим количество уникальных sku
        unique_sku_counts = (
            self.df.groupby("operation_id")["sku"].nunique().reset_index()
        )
        unique_sku_counts.columns = ["operation_id", "quantity"]
        # объединяем полученый датафрейм с основным
        self.df = self.df.merge(unique_sku_counts, on="operation_id", how="left")
        # оставляем только нужные столбцы
        self.df = self.df[
            [
                "operation_id",
                "operation_date",
                "type_operation",
                "posting_number",
                "sku",
                "article",
                "type_operation",
                "delivery_schema",
                "name",
                "price",
                "count_item",
                "total_price",
                "quantity",
            ]
        ]

    def get_from_dict_col(self, col: str, get: str) -> pd.Series:
        """
        Извлечение значения из словаря в столбце

        :param col: Имя столбца, содержащего словарь
        :param get: Ключ, по которому нужно получить значение
        :return: Серия с извлеченными значениями
        """
        return self.df[col].apply((lambda x: x.get(get)))

    def fillna_dicts(self, col: str) -> pd.Series:
        """
        Замена NaN значений в столбце на пустые словари

        :param col: Имя столбца для обработки
        :return: Серия с замененными значениями
        """
        return self.df[col].apply(lambda x: x if isinstance(x, dict) else {})

    @staticmethod
    def get_total_price(x: pd.Series) -> float:
        """
        Расчет общей цены

        :param x: Строка датафрейма
        :return: Общая цена
        """
        price = x["price"]
        count_item = x["count_item"]
        if not count_item:
            return 0.0
        return price / count_item

    def to_excel(self, *args, **kwargs) -> None:
        """
        Экспорт датафрейма в Excel

        :param args: Позиционные аргументы для pd.to_excel
        :param kwargs: Именованные аргументы для pd.to_excel
        """
        self.df.to_excel(*args, **kwargs)

    def to_csv(self, *args, **kwargs) -> None:
        """
        Экспорт датафрейма в CSV

        :param args: Позиционные аргументы для pd.to_csv
        :param kwargs: Именованные аргументы для pd.to_csv
        """
        self.df.to_csv(*args, **kwargs)


def main() -> None:
    file_path = "data\\data_json.json"
    de = DataExtractor(file_path)
    de.extract_data()
    de.to_excel("task1_output.xlsx", index=False, header=True)


if __name__ == "__main__":
    main()
