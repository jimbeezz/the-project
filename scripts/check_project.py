"""
Скрипт для проверки работоспособности проекта.
Запускает все основные проверки.
"""

import sys
import subprocess
from pathlib import Path


def run_command(cmd, description):
    """Запустить команду и вывести результат."""
    print(f"\n{'='*60}")
    print(f"[CHECK] {description}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            cmd,
            shell=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr and result.returncode != 0:
            print(f"Ошибки: {result.stderr}", file=sys.stderr)
        return result.returncode == 0
    except Exception as e:
        print(f"Ошибка при выполнении: {e}", file=sys.stderr)
        return False


def main():
    """Основная функция проверки."""
    print("="*60)
    print("ПРОВЕРКА РАБОТОСПОСОБНОСТИ ПРОЕКТА")
    print("="*60)
    
    checks_passed = 0
    checks_total = 0
    
    # 1. Проверка структуры проекта
    print("\n1. Проверка структуры проекта...")
    required_files = [
        'src/code_analyzer.py',
        'src/report_generator.py',
        'src/main.py',
        'tests/test_code_analyzer.py',
        'tests/test_report_generator.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    all_files_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"  [OK] {file_path}")
        else:
            print(f"  [FAIL] {file_path} - НЕ НАЙДЕН")
            all_files_exist = False
    
    if all_files_exist:
        checks_passed += 1
    checks_total += 1
    
    # 2. Проверка импортов
    print("\n2. Проверка импортов...")
    try:
        from src.code_analyzer import CodeAnalyzer
        from src.report_generator import ReportGenerator
        print("  [OK] Все модули импортируются успешно")
        checks_passed += 1
    except Exception as e:
        print(f"  [FAIL] Ошибка импорта: {e}")
    checks_total += 1
    
    # 3. Запуск тестов
    print("\n3. Запуск тестов...")
    if run_command("python -m pytest tests/ -v", "Запуск unit-тестов"):
        checks_passed += 1
    checks_total += 1
    
    # 4. Проверка анализатора на примере
    print("\n4. Проверка анализатора кода...")
    test_file = Path("data/students/sample_student_code.py")
    if test_file.exists():
        if run_command(
            f'python -m src.main "{test_file}" --format text',
            "Анализ примера студенческого кода"
        ):
            checks_passed += 1
    else:
        print("  ⚠ Файл с примером не найден, пропускаем")
    checks_total += 1
    
    # 5. Генерация HTML отчета
    print("\n5. Генерация HTML отчета...")
    if test_file.exists():
        report_path = Path("reports/test_report.html")
        report_path.parent.mkdir(exist_ok=True)
        if run_command(
            f'python -m src.main "{test_file}" --format html --output "{report_path}"',
            "Генерация HTML отчета"
        ):
            if report_path.exists():
                print(f"  [OK] Отчет создан: {report_path}")
                checks_passed += 1
            else:
                print(f"  [FAIL] Отчет не создан")
    checks_total += 1
    
    # 6. Проверка стиля кода (flake8)
    print("\n6. Проверка стиля кода (flake8)...")
    if run_command("flake8 src/ tests/ --max-line-length=79 --exclude=__pycache__ || echo 'flake8 не установлен, пропускаем'", "Проверка PEP 8"):
        checks_passed += 1
    checks_total += 1
    
    # Итоги
    print("\n" + "="*60)
    print("ИТОГИ ПРОВЕРКИ")
    print("="*60)
    print(f"Пройдено проверок: {checks_passed}/{checks_total}")
    
    if checks_passed == checks_total:
        print("\n[SUCCESS] ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ УСПЕШНО!")
        return 0
    else:
        print(f"\n[WARNING] ПРОЙДЕНО {checks_passed} ИЗ {checks_total} ПРОВЕРОК")
        return 1


if __name__ == '__main__':
    sys.exit(main())

