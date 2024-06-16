import os
import textwrap


class ConsoleApp:
    def __init__(self) -> None:
        """
        Инициализация класса ConsoleApp.
        Создание сообщений меню и запуск приложения.
        """
        self.main_menu_msg = textwrap.dedent(
            """
            Main Menu:
            1. MS
            2. PG
            3. Exit
        """
        )
        self.db_menu_msg = textwrap.dedent(
            """
            {} Menu:

            1. Загрузить данные
            2. Удалить данные
            3. Обратно в меню
        """
        )
        self.choice_msg = "Выберите вариант ответа (1-3): "
        self.wrong_answer_msg = "Неверный вариант ответа"
        self.init_app()

    def clear_screen(self):
        """Очистка экрана."""
        os.system("cls" if os.name == "nt" else "clear")

    def display_menu(self, menu_msg):
        """
        Отображение меню и получение выбора пользователя.

        :param menu_msg: Сообщение меню для отображения
        :return: Выбор пользователя
        """
        self.clear_screen()
        print(menu_msg)
        return input(self.choice_msg)

    def handle_choice(self, choice):
        """
        Обработка выбора пользователя в меню бд.

        :param choice: Выбор пользователя
        """
        if choice == "1":
            print("Данные загружены")
        elif choice == "2":
            print("Удалил данные")
        input("\nНажмите Enter чтобы продолжить...")

    def run_sub_menu(self, database):
        """
        Запуск меню бд для выбранной базы данных.

        :param database: Название базы данных
        """
        while True:
            sub_choice = self.display_menu(self.db_menu_msg.format(database))
            if sub_choice == "3":
                break
            self.handle_choice(sub_choice)

    def init_app(self):
        """
        Инициализация приложения. Запуск главного меню.
        """
        while True:
            choice = self.display_menu(self.main_menu_msg)
            if choice == "1":
                self.run_sub_menu("MS")
            elif choice == "2":
                self.run_sub_menu("PG")
            elif choice == "3":
                break
            else:
                print("Неверный вариант ответа")
                input("\nНажмите Enter чтобы продолжить...")


if __name__ == "__main__":
    ConsoleApp()
