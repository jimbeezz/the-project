"""
Точка входа для инструмента оценки качества кода.

Этот модуль предоставляет CLI интерфейс для запуска анализа кода.
Можно анализировать как отдельные файлы, так и целые директории.

Примеры использования:
    python -m src.main file.py --format html
    python -m src.main directory/ --format json --output report.json
"""

import argparse
import sys
from pathlib import Path
from .code_analyzer import CodeAnalyzer
from .report_generator import ReportGenerator


def main():
    """
    Главная функция для запуска инструмента оценки качества кода.
    
    Обрабатывает аргументы командной строки, запускает анализ
    и генерирует отчеты в выбранном формате.
    """
    parser = argparse.ArgumentParser(
        description='Инструмент оценки качества Python кода - автоматический анализ и отчеты'
    )
    parser.add_argument(
        'target',
        help='Путь к Python файлу или директории для анализа'
    )
    parser.add_argument(
        '--output',
        '-o',
        help='Путь для сохранения отчета (по умолчанию: stdout для text, report.html/json для других форматов)',
        default=None
    )
    parser.add_argument(
        '--format',
        '-f',
        choices=['text', 'html', 'json'],
        default='text',
        help='Формат отчета: text (текст), html (веб-страница), json (для автоматической обработки)'
    )
    
    args = parser.parse_args()
    
    # Создаем экземпляры анализатора и генератора отчетов
    code_analyzer = CodeAnalyzer()
    report_gen = ReportGenerator()
    
    # Проверяем существование указанного пути
    target_path = Path(args.target)
    if not target_path.exists():
        print(f"Ошибка: путь '{args.target}' не существует", file=sys.stderr)
        sys.exit(1)
    
    # Анализируем файл или директорию
    if target_path.is_file():
        # Один файл
        analysis_results = [code_analyzer.analyze_file(str(target_path))]
    else:
        # Вся директория рекурсивно
        analysis_results = code_analyzer.analyze_directory(str(target_path))
    
    if not analysis_results:
        print("Не найдено Python файлов для анализа", file=sys.stderr)
        sys.exit(1)
    
    # Генерируем отчет в выбранном формате
    if args.format == 'html':
        generated_report = report_gen.generate_html_report(
            analysis_results, 
            args.output or 'report.html'
        )
        if not args.output:
            print(generated_report)
    elif args.format == 'json':
        generated_report = report_gen.generate_json_report(
            analysis_results, 
            args.output or 'report.json'
        )
        if not args.output:
            print(generated_report)
    else:  # text format
        generated_report = report_gen.generate_text_report(analysis_results, args.output)
        if not args.output:
            print(generated_report)
    
    # Выводим краткую сводку
    successful_analyses = [r for r in analysis_results if 'overall_score' in r]
    if successful_analyses:
        average_score = sum(r['overall_score'] for r in successful_analyses) / len(successful_analyses)
        print(f"\nАнализ завершен. Средняя оценка: {average_score:.2f}/100", file=sys.stderr)


if __name__ == '__main__':
    main()

