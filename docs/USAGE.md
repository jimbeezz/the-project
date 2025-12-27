# Руководство по использованию

## Быстрый старт

### 1. Установка

```bash
pip install -r requirements.txt
```

### 2. Базовое использование

Анализ одного файла:
```bash
python -m src.main path/to/file.py
```

Анализ директории:
```bash
python -m src.main path/to/directory/
```

## Примеры использования

### Пример 1: Анализ студенческого кода

```bash
# Анализ всех Python файлов в папке студентов
python -m src.main data/students/ --format html --output reports/student_report.html
```

### Пример 2: Текстовый отчет

```bash
python -m src.main data/students/ --format text --output reports/student_report.txt
```

### Пример 3: JSON отчет для дальнейшей обработки

```bash
python -m src.main data/students/ --format json --output reports/student_report.json
```

### Пример 4: Анализ собственного проекта

```bash
python -m src.main src/ --format html --output reports/project_report.html
```

## Интерпретация результатов

### Оценка качества

- **90-100**: Отличный код
- **70-89**: Хороший код с небольшими замечаниями
- **50-69**: Средний код, требует улучшений
- **0-49**: Низкое качество, требуется рефакторинг

### Метрики

#### PEP 8 Compliance
- Проверяет соответствие стандартам Python
- Рекомендуется: ≥80 баллов

#### Cyclomatic Complexity
- Средняя сложность: рекомендуется ≤5
- Максимальная сложность: рекомендуется ≤10

#### Docstring Coverage
- Рекомендуется: ≥80% покрытия

#### Code Duplication
- Рекомендуется: ≤10% дублирования

## Интеграция в CI/CD

Проект автоматически анализирует код при каждом push через GitHub Actions.

Отчеты доступны в разделе Actions → Artifacts.

