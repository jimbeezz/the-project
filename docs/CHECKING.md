# Как проверить работоспособность проекта

## Быстрая проверка (5 минут)

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск тестов

```bash
python -m pytest tests/ -v
```

**Ожидаемый результат:** Все 13 тестов должны пройти успешно.

### 3. Проверка анализатора на примере

```bash
python -m src.main data/students/sample_student_code.py --format text
```

**Ожидаемый результат:** Должен вывести текстовый отчет с анализом кода.

### 4. Генерация HTML отчета

```bash
python -m src.main data/students/ --format html --output reports/test_report.html
```

**Ожидаемый результат:** 
- Создается файл `reports/test_report.html`
- В консоли выводится сообщение "Analysis complete"

### 5. Проверка стиля кода (опционально)

```bash
flake8 src/ tests/ --max-line-length=79 --exclude=__pycache__
```

**Ожидаемый результат:** Могут быть небольшие предупреждения, но критических ошибок быть не должно.

## Полная проверка

### Автоматический скрипт проверки

```bash
python scripts/check_project.py
```

Скрипт проверит:
- ✅ Структуру проекта
- ✅ Импорты модулей
- ✅ Запуск тестов
- ✅ Работу анализатора
- ✅ Генерацию отчетов
- ✅ Проверку стиля кода

## Проверка CI/CD

### Локальная проверка (симуляция GitHub Actions)

1. Убедитесь, что все зависимости установлены:
   ```bash
   pip install -r requirements.txt
   ```

2. Запустите тесты с покрытием:
   ```bash
   pytest tests/ -v --cov=src --cov-report=html
   ```

3. Проверьте, что отчеты создаются:
   ```bash
   python -m src.main src/ --format html --output reports/project_report.html
   python -m src.main data/students/ --format json --output reports/student_report.json
   ```

### Проверка на GitHub

1. Закоммитьте и запушьте изменения:
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. Перейдите в раздел **Actions** на GitHub

3. Проверьте, что workflow запустился и завершился успешно (зеленый статус ✅)

4. Скачайте artifacts (отчеты) из последнего успешного запуска

## Что проверить в результатах

### Тесты
- ✅ Все 13 тестов проходят
- ✅ Нет ошибок импорта
- ✅ Нет критических исключений

### Анализ кода
- ✅ Анализ завершается без ошибок
- ✅ Генерируется итоговая оценка (0-100)
- ✅ Все метрики присутствуют:
  - PEP 8 Compliance
  - Cyclomatic Complexity
  - Docstring Coverage
  - Code Duplication

### Отчеты
- ✅ HTML отчет открывается в браузере
- ✅ JSON отчет валидный (можно проверить через `python -m json.tool reports/student_report.json`)
- ✅ Текстовый отчет читаемый

### CI/CD
- ✅ Workflow запускается автоматически при push
- ✅ Все шаги выполняются успешно
- ✅ Artifacts загружаются (отчеты доступны для скачивания)

## Возможные проблемы

### Проблема: "No module named 'src'"
**Решение:** Убедитесь, что вы запускаете команды из корневой директории проекта.

### Проблема: Тесты не находятся
**Решение:** Убедитесь, что pytest установлен: `pip install pytest pytest-cov`

### Проблема: flake8 не найден
**Решение:** Установите: `pip install flake8`

### Проблема: CI/CD не запускается
**Решение:** 
- Проверьте, что файл `.github/workflows/ci.yml` существует
- Убедитесь, что вы пушите в ветку `main` или `master`
- Проверьте синтаксис YAML файла

## Минимальные требования для проверки

- Python 3.8+
- Установленные зависимости из `requirements.txt`
- Доступ к интернету (для проверки CI/CD на GitHub)

