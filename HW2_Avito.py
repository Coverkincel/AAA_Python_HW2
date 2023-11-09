import csv
from typing import List, Dict


def read_csv_data(file_path: str) -> List[Dict[str, str]]:
    """
    Читает данные из CSV-файла и возвращает список словарей.

    Args:
        file_path: Путь к файлу CSV.

    Returns:
        Список словарей, где каждый словарь представляет строку из CSV.
    """
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file, delimiter=';')
        return list(csv_reader)


def print_departments_hierarchy(data: List[Dict[str, str]]) -> None:
    """
    Выводит иерархию команд: департаменты и входящие в них команды.

    Args:
        data: Список словарей с данными о сотрудниках.
    """
    hierarchy = {}
    for entry in data:
        department = entry['Департамент']
        team = entry['Отдел']
        hierarchy.setdefault(department, set()).add(team)

    for department, teams in sorted(hierarchy.items()):
        print(f'Департамент: {department}')
        for team in sorted(teams):
            print(f'  Команда: {team}')
        print()


# Следующую строку пришлось разделить ради PEP-8
def generate_departments_report(
        data: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Создает и возвращает сводный отчет по департаментам.

    Args:
        data: Список словарей с данными о сотрудниках.

    Returns:
        Список словарей, каждый из которых содержит информацию по департаменту.
    """
    report = {}
    for entry in data:
        department = entry['Департамент']
        salary = float(entry['Оклад'].replace(' ', ''))
        dept_data = report.setdefault(department, {
            'Численность': 0, 'Мин. зарплата': salary,
            'Макс. зарплата': salary, 'Суммарная зарплата': 0
        })
        dept_data['Численность'] += 1
        dept_data['Суммарная зарплата'] += salary
        if salary < dept_data['Мин. зарплата']:
            dept_data['Мин. зарплата'] = salary
        if salary > dept_data['Макс. зарплата']:
            dept_data['Макс. зарплата'] = salary

    return [
        {
            'Департамент': dept,
            'Численность': d['Численность'],
            'Мин. зарплата': d['Мин. зарплата'],
            'Макс. зарплата': d['Макс. зарплата'],
            'Средняя зарплата': round(
                d['Суммарная зарплата'] / d['Численность'], 2
            )
        } for dept, d in sorted(report.items())
    ]


def print_departments_report(data: List[Dict[str, str]]) -> None:
    """
    Выводит сводный отчет по департаментам.

    Args:
        data: Список словарей с данными о сотрудниках.
    """
    report = generate_departments_report(data)
    for department_info in report:
        print(f"Департамент: {department_info['Департамент']}")
        print(f"Численность: {department_info['Численность']}")
        print(
            "Вилка зарплат:",
            f"{department_info['Мин. зарплата']:.2f}",
            f"- {department_info['Макс. зарплата']:.2f}")
        print(f"Средняя зарплата: {department_info['Средняя зарплата']}")
        print()


# Следующую строку пришлось разделить ради PEP-8
def save_report_to_csv(
        report_data: List[Dict[str, str]], file_path: str) -> None:
    """
    Сохраняет в нашей директории отчет в CSV-файл.

    Args:
        report_data: Список словарей с отчетными данными.
        file_path: Путь для сохранения файла CSV.
    """
    headers = report_data[0].keys()
    with open(file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, headers, delimiter=';')
        writer.writeheader()
        writer.writerows(report_data)


def main_menu() -> None:
    """
    Главное меню для взаимодействия с пользователем.
    """
    data = read_csv_data('Corp_Summary.csv')
    while True:
        print('\nГлавное меню:')
        print('1. Вывести иерархию команд')
        print('2. Вывести сводный отчет по департаментам')
        print('3. Сохранить сводный отчет в CSV-файл')
        print('4. Выход')
        choice = input('Введите номер действия: ')
        if choice == '1':
            print_departments_hierarchy(data)
        elif choice == '2':
            print_departments_report(data)
        elif choice == '3':
            report = generate_departments_report(data)
            save_report_to_csv(report, 'Department_Report.csv')
            print('Отчет сохранен в файл: Department_Report.csv')
        elif choice == '4':
            print('Выход из программы.')
            break
        else:
            print('Неверный ввод, попробуйте еще раз.')


if __name__ == '__main__':
    main_menu()
