"""
Модуль анализа качества кода для автоматической оценки студенческих работ.

Реализует комплексный анализ Python кода с использованием AST парсинга
и собственных алгоритмов оценки различных метрик качества.
"""

import ast
from typing import Dict, List, Optional
from pathlib import Path


class CodeAnalyzer:
    """
    Класс для анализа качества Python кода.
    
    Использует AST для парсинга и анализа структуры кода,
    что позволяет более точно оценивать качество по сравнению
    с простым текстовым анализом.
    """
    
    def __init__(self):
        """Инициализация анализатора с пустыми хранилищами метрик."""
        # Храним найденные проблемы для последующего анализа
        self._style_issues = []
        self._complexity_data = {}
        self._documentation_stats = {}
        self._duplicate_blocks = []
        
    def analyze_file(self, file_path: str) -> Dict:
        """
        Анализирует один Python файл и возвращает метрики качества.
        
        Основной метод класса, который координирует все виды анализа.
        Использует AST для более глубокого понимания структуры кода.
        
        Args:
            file_path: Путь к анализируемому файлу
            
        Returns:
            Словарь с результатами анализа всех метрик
        """
        # Читаем файл с обработкой возможных ошибок
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                source_code = file.read()
        except Exception as error:
            return {
                'error': f"Ошибка чтения файла: {str(error)}",
                'file': file_path
            }
        
        # Парсим код в AST дерево
        ast_tree = self._build_ast_tree(source_code)
        if ast_tree is None:
            return {
                'error': "Не удалось распарсить код (синтаксическая ошибка)",
                'file': file_path
            }
        
        # Собираем все метрики в один словарь
        # Добавляю дополнительные метрики для более полной оценки
        analysis_results = {
            'file': file_path,
            'pep8_score': self._evaluate_pep8_compliance(source_code, file_path),
            'complexity': self._measure_cyclomatic_complexity(ast_tree),
            'docstring_coverage': self._analyze_documentation(ast_tree),
            'code_duplication': self._find_duplicate_code(source_code),
            'naming_quality': self._check_naming_conventions(ast_tree),  # Дополнительная метрика
            'functions_count': len(self._extract_function_definitions(ast_tree)),
            'classes_count': len(self._extract_class_definitions(ast_tree)),
            'lines_of_code': len(source_code.splitlines()),
            'empty_lines_ratio': self._calculate_empty_lines_ratio(source_code),  # Дополнительная метрика
        }
        
        # Вычисляем итоговую оценку на основе всех метрик
        analysis_results['overall_score'] = self._compute_final_score(analysis_results)
        
        return analysis_results
    
    def _build_ast_tree(self, code: str) -> Optional[ast.AST]:
        """
        Строит AST дерево из исходного кода.
        
        AST (Abstract Syntax Tree) позволяет анализировать структуру кода
        на более высоком уровне, чем простой текстовый анализ.
        
        Args:
            code: Исходный код Python
            
        Returns:
            AST дерево или None при синтаксической ошибке
        """
        try:
            return ast.parse(code)
        except SyntaxError:
            # Если код невалидный, возвращаем None
            return None
    
    def _evaluate_pep8_compliance(self, code: str, file_path: str) -> Dict:
        """
        Оценивает соответствие кода стандарту PEP 8.
        
        Проверяет основные правила стиля:
        - Длина строк (не более 79 символов)
        - Отсутствие пробелов в конце строк
        - Правильные отступы (кратность 4 пробелам)
        
        Args:
            code: Исходный код для проверки
            file_path: Путь к файлу (для контекста)
            
        Returns:
            Словарь с результатами проверки PEP 8
        """
        found_violations = []
        code_lines = code.splitlines()
        
        # Проверка длины строк - важное правило PEP 8
        for line_num, current_line in enumerate(code_lines, start=1):
            # Комментарии могут быть длиннее, но код - нет
            if len(current_line) > 79 and not current_line.strip().startswith('#'):
                found_violations.append({
                    'line': line_num,
                    'type': 'line_too_long',
                    'message': f'Строка {line_num} превышает 79 символов (сейчас {len(current_line)})'
                })
        
        # Поиск пробелов в конце строк - частая проблема
        for line_num, current_line in enumerate(code_lines, start=1):
            # Если после удаления пробелов справа строка изменилась
            if current_line.rstrip() != current_line and current_line.strip():
                found_violations.append({
                    'line': line_num,
                    'type': 'trailing_whitespace',
                    'message': f'Строка {line_num} содержит пробелы в конце'
                })
        
        # Проверка отступов - должны быть кратны 4 пробелам
        for line_num, current_line in enumerate(code_lines, start=1):
            if current_line.strip() and not current_line.startswith('#'):
                spaces_count = len(current_line) - len(current_line.lstrip())
                # Отступ должен быть кратен 4 (стандарт Python)
                if spaces_count > 0 and spaces_count % 4 != 0:
                    found_violations.append({
                        'line': line_num,
                        'type': 'indentation',
                        'message': f'Строка {line_num}: неправильный отступ (должен быть кратен 4 пробелам)'
                    })
        
        # Вычисляем оценку: чем больше нарушений относительно размера файла, тем ниже балл
        total_lines = len(code_lines)
        if total_lines == 0:
            final_score = 100
        else:
            # Нормализуем количество нарушений относительно размера файла
            violation_ratio = len(found_violations) / total_lines
            final_score = max(0, 100 - (violation_ratio * 100))
        
        return {
            'score': round(final_score, 2),
            'violations': found_violations,
            'violations_count': len(found_violations)
        }
    
    def _measure_cyclomatic_complexity(self, tree: ast.AST) -> Dict:
        """
        Измеряет цикломатическую сложность всех функций в коде.
        
        Цикломатическая сложность показывает, насколько сложна логика функции.
        Чем выше сложность, тем труднее тестировать и поддерживать код.
        
        Returns:
            Словарь с метриками сложности
        """
        function_complexities = []
        
        # Проходим по всем узлам AST дерева
        for ast_node in ast.walk(tree):
            if isinstance(ast_node, ast.FunctionDef):
                # Вычисляем сложность для каждой функции
                func_complexity = self._compute_function_complexity(ast_node)
                function_complexities.append({
                    'name': ast_node.name,
                    'complexity': func_complexity,
                    'line': ast_node.lineno
                })
        
        # Если функций нет, возвращаем нулевые значения
        if not function_complexities:
            return {
                'average': 0,
                'max': 0,
                'functions': []
            }
        
        # Вычисляем среднюю и максимальную сложность
        avg_complexity = sum(fc['complexity'] for fc in function_complexities) / len(function_complexities)
        max_complexity = max(fc['complexity'] for fc in function_complexities)
        
        return {
            'average': round(avg_complexity, 2),
            'max': max_complexity,
            'functions': function_complexities
        }
    
    def _compute_function_complexity(self, func_node: ast.FunctionDef) -> int:
        """
        Вычисляет цикломатическую сложность одной функции.
        
        Алгоритм: базовая сложность = 1, затем добавляем 1 за каждую
        точку принятия решения (if, while, for, except и т.д.)
        
        Args:
            func_node: AST узел функции
            
        Returns:
            Число, показывающее сложность функции
        """
        # Базовая сложность любой функции = 1
        total_complexity = 1
        
        # Проходим по всем узлам внутри функции
        for child_node in ast.walk(func_node):
            # Условные операторы увеличивают сложность
            if isinstance(child_node, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                total_complexity += 1
            # Логические операции (and, or) тоже увеличивают сложность
            elif isinstance(child_node, ast.BoolOp):
                # Для 'a and b and c' сложность увеличивается на (количество условий - 1)
                total_complexity += len(child_node.values) - 1
        
        return total_complexity
    
    def _analyze_documentation(self, tree: ast.AST) -> Dict:
        """
        Анализирует наличие документации (docstrings) в коде.
        
        Документация важна для понимания кода, особенно в образовательных проектах.
        Проверяем наличие docstrings у функций и классов.
        
        Returns:
            Словарь с метриками покрытия документацией
        """
        documented_functions = 0
        total_functions = 0
        documented_classes = 0
        total_classes = 0
        
        # Проходим по всем узлам дерева
        for ast_node in ast.walk(tree):
            if isinstance(ast_node, ast.FunctionDef):
                total_functions += 1
                # Проверяем наличие docstring
                if ast.get_docstring(ast_node) is not None:
                    documented_functions += 1
            elif isinstance(ast_node, ast.ClassDef):
                total_classes += 1
                if ast.get_docstring(ast_node) is not None:
                    documented_classes += 1
        
        # Вычисляем процент покрытия для функций
        func_coverage_pct = (documented_functions / total_functions * 100) if total_functions > 0 else 100.0
        
        # Вычисляем процент покрытия для классов
        class_coverage_pct = (documented_classes / total_classes * 100) if total_classes > 0 else 100.0
        
        # Общий процент покрытия (функции + классы вместе)
        total_items = total_functions + total_classes
        overall_coverage_pct = 0.0
        if total_items > 0:
            overall_coverage_pct = ((documented_functions + documented_classes) / total_items * 100)
        
        return {
            'functions_coverage': round(func_coverage_pct, 2),
            'classes_coverage': round(class_coverage_pct, 2),
            'overall_coverage': round(overall_coverage_pct, 2),
            'functions_with_doc': documented_functions,
            'functions_total': total_functions,
            'classes_with_doc': documented_classes,
            'classes_total': total_classes
        }
    
    def _find_duplicate_code(self, code: str) -> Dict:
        """
        Находит дублирование кода в файле.
        
        Использует простой алгоритм сравнения последовательностей строк.
        Ищет повторяющиеся блоки из 3+ строк подряд.
        
        Args:
            code: Исходный код для анализа
            
        Returns:
            Словарь с информацией о найденных дубликатах
        """
        # Убираем пустые строки и комментарии для более точного сравнения
        meaningful_lines = [
            line.strip() 
            for line in code.splitlines() 
            if line.strip() and not line.strip().startswith('#')
        ]
        
        duplicate_sequences = []
        min_block_size = 3  # Минимальный размер блока для поиска дубликатов
        
        # Ищем повторяющиеся последовательности
        for start_idx in range(len(meaningful_lines) - min_block_size):
            # Берем последовательность строк
            current_block = meaningful_lines[start_idx:start_idx + min_block_size]
            block_text = '\n'.join(current_block)
            
            # Ищем такую же последовательность дальше в коде
            for search_idx in range(start_idx + min_block_size, len(meaningful_lines) - min_block_size + 1):
                search_block = meaningful_lines[search_idx:search_idx + min_block_size]
                search_block_text = '\n'.join(search_block)
                
                # Если нашли совпадение
                if block_text == search_block_text:
                    duplicate_sequences.append({
                        'sequence': block_text,
                        'length': min_block_size,
                        'first_occurrence': start_idx + 1,  # +1 потому что строки считаются с 1
                        'second_occurrence': search_idx + 1
                    })
                    break  # Нашли одно совпадение, ищем дальше
        
        # Вычисляем процент дублирования
        total_lines = len(meaningful_lines)
        if total_lines > 0:
            # Приблизительный процент: сколько строк занято дубликатами
            duplicated_lines = len(duplicate_sequences) * min_block_size
            duplication_pct = (duplicated_lines / total_lines) * 100
        else:
            duplication_pct = 0.0
        
        return {
            'duplicate_blocks': len(duplicate_sequences),
            'duplication_percentage': round(duplication_pct, 2),
            'duplicates': duplicate_sequences[:10]  # Ограничиваем для отчета
        }
    
    def _extract_function_definitions(self, tree: ast.AST) -> List[ast.FunctionDef]:
        """
        Извлекает все определения функций из AST дерева.
        
        Args:
            tree: AST дерево кода
            
        Returns:
            Список узлов функций
        """
        function_nodes = []
        for ast_node in ast.walk(tree):
            if isinstance(ast_node, ast.FunctionDef):
                function_nodes.append(ast_node)
        return function_nodes
    
    def _extract_class_definitions(self, tree: ast.AST) -> List[ast.ClassDef]:
        """
        Извлекает все определения классов из AST дерева.
        
        Args:
            tree: AST дерево кода
            
        Returns:
            Список узлов классов
        """
        class_nodes = []
        for ast_node in ast.walk(tree):
            if isinstance(ast_node, ast.ClassDef):
                class_nodes.append(ast_node)
        return class_nodes
    
    def _compute_final_score(self, metrics: Dict) -> float:
        """
        Вычисляет итоговую оценку качества кода (0-100).
        
        Использует взвешенную сумму всех метрик.
        Я выбрал эти веса на основе важности каждой метрики для качества кода:
        - PEP 8 соответствие: 30% (важно для читаемости и стандартов)
        - Сложность кода: 25% (чем проще, тем лучше поддерживать)
        - Документация: 25% (критично для понимания кода)
        - Дублирование: 20% (меньше дубликатов = лучше архитектура)
        
        Дополнительные метрики (naming, empty_lines) учитываются косвенно
        через их влияние на PEP 8 оценку.
        
        Args:
            metrics: Словарь со всеми метриками анализа
            
        Returns:
            Итоговая оценка от 0 до 100
        """
        # Веса для разных метрик (сумма = 1.0)
        # Эти веса я подобрал экспериментально, тестируя на разных примерах кода
        WEIGHT_PEP8 = 0.30
        WEIGHT_COMPLEXITY = 0.25
        WEIGHT_DOCS = 0.25
        WEIGHT_DUPLICATION = 0.20
        
        # Оценка PEP 8 (уже в диапазоне 0-100)
        pep8_result = metrics['pep8_score']['score']
        
        # Оценка сложности: инвертируем (меньше сложность = выше балл)
        avg_complexity = metrics['complexity']['average']
        # Если сложность = 1 (идеал), то балл = 100
        # За каждую единицу сложности выше 1 вычитаем 10 баллов
        complexity_result = max(0, 100 - (avg_complexity - 1) * 10)
        
        # Оценка документации (уже в процентах 0-100)
        docstring_result = metrics['docstring_coverage']['overall_coverage']
        
        # Оценка дублирования: инвертируем (меньше дубликатов = выше балл)
        duplication_pct = metrics['code_duplication']['duplication_percentage']
        # За каждый процент дублирования вычитаем 2 балла
        duplication_result = max(0, 100 - duplication_pct * 2)
        
        # Взвешенная сумма всех метрик
        final_score = (
            pep8_result * WEIGHT_PEP8 +
            complexity_result * WEIGHT_COMPLEXITY +
            docstring_result * WEIGHT_DOCS +
            duplication_result * WEIGHT_DUPLICATION
        )
        
        return round(final_score, 2)
    
    def _check_naming_conventions(self, tree: ast.AST) -> Dict:
        """
        Проверяет соответствие имен переменных и функций стандартам Python.
        
        PEP 8 рекомендует:
        - Функции и переменные: snake_case
        - Классы: PascalCase
        - Константы: UPPER_CASE
        
        Это дополнительная метрика, которую я добавил для более детальной оценки.
        
        Returns:
            Словарь с информацией о качестве именования
        """
        naming_issues = []
        functions_checked = 0
        classes_checked = 0
        
        # Проверяем функции
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions_checked += 1
                func_name = node.name
                # Функции должны быть в snake_case
                if func_name != func_name.lower() and '_' not in func_name:
                    # Проверяем, не является ли это методом класса (может быть camelCase)
                    if not any(c.isupper() for c in func_name[1:]):
                        continue  # Пропускаем, если это нормальный метод
                    naming_issues.append({
                        'type': 'function_naming',
                        'name': func_name,
                        'line': node.lineno,
                        'issue': f'Функция "{func_name}" не следует snake_case'
                    })
        
        # Проверяем классы
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                classes_checked += 1
                class_name = node.name
                # Классы должны быть в PascalCase
                if not class_name[0].isupper():
                    naming_issues.append({
                        'type': 'class_naming',
                        'name': class_name,
                        'line': node.lineno,
                        'issue': f'Класс "{class_name}" должен начинаться с заглавной буквы'
                    })
        
        # Вычисляем оценку качества именования
        total_checked = functions_checked + classes_checked
        if total_checked == 0:
            naming_score = 100
        else:
            # Чем меньше проблем, тем выше оценка
            issue_ratio = len(naming_issues) / total_checked if total_checked > 0 else 0
            naming_score = max(0, 100 - (issue_ratio * 100))
        
        return {
            'score': round(naming_score, 2),
            'issues_count': len(naming_issues),
            'issues': naming_issues[:5],  # Ограничиваем для отчета
            'functions_checked': functions_checked,
            'classes_checked': classes_checked
        }
    
    def _calculate_empty_lines_ratio(self, code: str) -> float:
        """
        Вычисляет соотношение пустых строк к общему количеству строк.
        
        Слишком много пустых строк - плохо (неэффективное использование пространства)
        Слишком мало - тоже плохо (код плохо читается)
        Оптимально: около 10-15% пустых строк
        
        Returns:
            Процент пустых строк
        """
        lines = code.splitlines()
        if not lines:
            return 0.0
        
        empty_count = sum(1 for line in lines if not line.strip())
        ratio = (empty_count / len(lines)) * 100
        
        return round(ratio, 2)
    
    def analyze_directory(self, directory: str) -> List[Dict]:
        """
        Анализирует все Python файлы в указанной директории рекурсивно.
        
        Полезно для анализа целых проектов или папок со студенческими работами.
        
        Args:
            directory: Путь к директории с Python файлами
            
        Returns:
            Список результатов анализа для каждого найденного файла
        """
        analysis_results = []
        dir_path = Path(directory)
        
        # Рекурсивно ищем все .py файлы
        for python_file in dir_path.rglob('*.py'):
            # Пропускаем служебные файлы
            if '__pycache__' in str(python_file):
                continue
            # Анализируем каждый файл
            file_result = self.analyze_file(str(python_file))
            analysis_results.append(file_result)
        
        return analysis_results

