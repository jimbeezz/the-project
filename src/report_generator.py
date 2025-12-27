"""
Модуль генерации отчетов о качестве кода.

Создает отчеты в различных форматах (текст, HTML, JSON) на основе
результатов анализа кода. Отчеты включают детальную информацию
и рекомендации по улучшению.
"""

from typing import List, Dict
from datetime import datetime
import json


class ReportGenerator:
    """
    Класс для генерации отчетов о качестве кода.
    
    Поддерживает несколько форматов вывода для удобства использования
    в разных сценариях (просмотр, автоматическая обработка и т.д.).
    """
    
    def __init__(self):
        """Инициализация генератора с текущей датой и временем."""
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_text_report(self, results: List[Dict], output_path: str = None) -> str:
        """
        Generate a text report from analysis results.
        
        Args:
            results: List of analysis results
            output_path: Optional path to save report
            
        Returns:
            Report as string
        """
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("ОТЧЕТ О КАЧЕСТВЕ КОДА")
        report_lines.append("=" * 80)
        report_lines.append(f"Сгенерировано: {self.timestamp}")
        report_lines.append("")
        
        # Сводная статистика
        if results:
            valid_scores = [r.get('overall_score', 0) for r in results if 'overall_score' in r]
            if valid_scores:
                avg_score = sum(valid_scores) / len(valid_scores)
            else:
                avg_score = 0
            report_lines.append(f"Проанализировано файлов: {len(results)}")
            report_lines.append(f"Средняя итоговая оценка: {avg_score:.2f}/100")
            report_lines.append("")
        
        # Detailed results for each file
        for result in results:
            if 'error' in result:
                report_lines.append(f"\nFile: {result.get('file', 'Unknown')}")
                report_lines.append(f"ERROR: {result['error']}")
                continue
            
            report_lines.append("-" * 80)
            report_lines.append(f"Файл: {result['file']}")
            report_lines.append("-" * 80)
            
            # Итоговая оценка
            report_lines.append(f"\nИтоговая оценка: {result.get('overall_score', 0):.2f}/100")
            
            # PEP 8
            pep8_metrics = result.get('pep8_score', {})
            report_lines.append(f"\nСоответствие PEP 8: {pep8_metrics.get('score', 0):.2f}/100")
            report_lines.append(f"  Нарушений: {pep8_metrics.get('violations_count', 0)}")
            if pep8_metrics.get('violations'):
                report_lines.append("  Проблемы:")
                for violation in pep8_metrics['violations'][:5]:  # Показываем первые 5
                    report_lines.append(f"    - Строка {violation['line']}: {violation['message']}")
            
            # Сложность
            complexity_metrics = result.get('complexity', {})
            report_lines.append(f"\nЦикломатическая сложность:")
            report_lines.append(f"  Средняя: {complexity_metrics.get('average', 0):.2f}")
            report_lines.append(f"  Максимальная: {complexity_metrics.get('max', 0)}")
            if complexity_metrics.get('functions'):
                report_lines.append("  Функции:")
                for func in complexity_metrics['functions'][:5]:  # Показываем первые 5
                    report_lines.append(f"    - {func['name']} (строка {func['line']}): {func['complexity']}")
            
            # Документация
            doc_metrics = result.get('docstring_coverage', {})
            report_lines.append(f"\nПокрытие документацией: {doc_metrics.get('overall_coverage', 0):.2f}%")
            report_lines.append(f"  Функции: {doc_metrics.get('functions_with_doc', 0)}/{doc_metrics.get('functions_total', 0)}")
            report_lines.append(f"  Классы: {doc_metrics.get('classes_with_doc', 0)}/{doc_metrics.get('classes_total', 0)}")
            
            # Дублирование
            dup_metrics = result.get('code_duplication', {})
            report_lines.append(f"\nДублирование кода: {dup_metrics.get('duplication_percentage', 0):.2f}%")
            report_lines.append(f"  Дублирующихся блоков: {dup_metrics.get('duplicate_blocks', 0)}")
            
            # Качество именования (дополнительная метрика)
            naming_metrics = result.get('naming_quality', {})
            if naming_metrics:
                report_lines.append(f"\nКачество именования: {naming_metrics.get('score', 0):.2f}/100")
                report_lines.append(f"  Проверено функций: {naming_metrics.get('functions_checked', 0)}")
                report_lines.append(f"  Проверено классов: {naming_metrics.get('classes_checked', 0)}")
                if naming_metrics.get('issues_count', 0) > 0:
                    report_lines.append(f"  Проблем с именованием: {naming_metrics.get('issues_count', 0)}")
            
            # Статистика кода
            report_lines.append(f"\nСтатистика кода:")
            report_lines.append(f"  Строк кода: {result.get('lines_of_code', 0)}")
            report_lines.append(f"  Функций: {result.get('functions_count', 0)}")
            report_lines.append(f"  Классов: {result.get('classes_count', 0)}")
            empty_ratio = result.get('empty_lines_ratio', 0)
            if empty_ratio > 0:
                report_lines.append(f"  Процент пустых строк: {empty_ratio:.2f}%")
            
            report_lines.append("")
        
        # Рекомендации
        report_lines.append("=" * 80)
        report_lines.append("РЕКОМЕНДАЦИИ")
        report_lines.append("=" * 80)
        
        for result in results:
            if 'error' in result or 'overall_score' not in result:
                continue
            
            score = result.get('overall_score', 0)
            recommendations = self._generate_recommendations(result)
            
            if recommendations:
                report_lines.append(f"\n{result.get('file', 'Unknown')}:")
                for rec in recommendations:
                    report_lines.append(f"  - {rec}")
        
        report_text = "\n".join(report_lines)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(report_text)
        
        return report_text
    
    def generate_html_report(self, results: List[Dict], output_path: str = None) -> str:
        """
        Generate an HTML report from analysis results.
        
        Args:
            results: List of analysis results
            output_path: Optional path to save report
            
        Returns:
            Report as HTML string
        """
        html = []
        html.append("<!DOCTYPE html>")
        html.append("<html>")
        html.append("<head>")
        html.append("<meta charset='utf-8'>")
        html.append("<title>Code Quality Assessment Report</title>")
        html.append("<style>")
        html.append("""
            body { font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }
            .container { max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
            h1 { color: #333; }
            h2 { color: #555; border-bottom: 2px solid #ddd; padding-bottom: 10px; }
            .file-section { margin: 20px 0; padding: 15px; background: #f9f9f9; border-radius: 5px; }
            .score { font-size: 24px; font-weight: bold; }
            .score-high { color: #28a745; }
            .score-medium { color: #ffc107; }
            .score-low { color: #dc3545; }
            .metric { margin: 10px 0; }
            .violation { padding: 5px; margin: 5px 0; background: #fff3cd; border-left: 3px solid #ffc107; }
            table { width: 100%; border-collapse: collapse; margin: 10px 0; }
            th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }
            th { background-color: #4CAF50; color: white; }
        """)
        html.append("</style>")
        html.append("</head>")
        html.append("<body>")
        html.append("<div class='container'>")
        html.append("<h1>Code Quality Assessment Report</h1>")
        html.append(f"<p><strong>Generated:</strong> {self.timestamp}</p>")
        
        # Summary
        if results:
            avg_score = sum(r.get('overall_score', 0) for r in results if 'overall_score' in r) / len(results)
            html.append(f"<p><strong>Files analyzed:</strong> {len(results)}</p>")
            html.append(f"<p><strong>Average overall score:</strong> {avg_score:.2f}/100</p>")
        
        # Detailed results
        for result in results:
            if 'error' in result:
                html.append(f"<div class='file-section'><h3>{result.get('file', 'Unknown')}</h3>")
                html.append(f"<p style='color: red;'>ERROR: {result['error']}</p></div>")
                continue
            
            score = result.get('overall_score', 0)
            score_class = 'score-high' if score >= 70 else 'score-medium' if score >= 50 else 'score-low'
            
            html.append("<div class='file-section'>")
            html.append(f"<h2>{result['file']}</h2>")
            html.append(f"<div class='score {score_class}'>Overall Score: {score:.2f}/100</div>")
            
            # PEP 8
            pep8 = result.get('pep8_score', {})
            html.append("<div class='metric'>")
            html.append(f"<h3>PEP 8 Compliance: {pep8.get('score', 0):.2f}/100</h3>")
            html.append(f"<p>Violations: {pep8.get('violations_count', 0)}</p>")
            if pep8.get('violations'):
                html.append("<table><tr><th>Line</th><th>Issue</th></tr>")
                for violation in pep8['violations'][:10]:
                    html.append(f"<tr><td>{violation['line']}</td><td>{violation['message']}</td></tr>")
                html.append("</table>")
            html.append("</div>")
            
            # Complexity
            complexity = result.get('complexity', {})
            html.append("<div class='metric'>")
            html.append(f"<h3>Cyclomatic Complexity</h3>")
            html.append(f"<p>Average: {complexity.get('average', 0):.2f}</p>")
            html.append(f"<p>Maximum: {complexity.get('max', 0)}</p>")
            if complexity.get('functions'):
                html.append("<table><tr><th>Function</th><th>Line</th><th>Complexity</th></tr>")
                for func in complexity['functions']:
                    html.append(f"<tr><td>{func['name']}</td><td>{func['line']}</td><td>{func['complexity']}</td></tr>")
                html.append("</table>")
            html.append("</div>")
            
            # Docstrings
            docstrings = result.get('docstring_coverage', {})
            html.append("<div class='metric'>")
            html.append(f"<h3>Docstring Coverage: {docstrings.get('overall_coverage', 0):.2f}%</h3>")
            html.append(f"<p>Functions: {docstrings.get('functions_with_doc', 0)}/{docstrings.get('functions_total', 0)}</p>")
            html.append(f"<p>Classes: {docstrings.get('classes_with_doc', 0)}/{docstrings.get('classes_total', 0)}</p>")
            html.append("</div>")
            
            # Duplication
            duplication = result.get('code_duplication', {})
            html.append("<div class='metric'>")
            html.append(f"<h3>Code Duplication: {duplication.get('duplication_percentage', 0):.2f}%</h3>")
            html.append(f"<p>Duplicate blocks: {duplication.get('duplicate_blocks', 0)}</p>")
            html.append("</div>")
            
            # Naming quality (дополнительная метрика)
            naming = result.get('naming_quality', {})
            if naming:
                html.append("<div class='metric'>")
                html.append(f"<h3>Naming Quality: {naming.get('score', 0):.2f}/100</h3>")
                html.append(f"<p>Functions checked: {naming.get('functions_checked', 0)}</p>")
                html.append(f"<p>Classes checked: {naming.get('classes_checked', 0)}</p>")
                if naming.get('issues_count', 0) > 0:
                    html.append(f"<p>Naming issues: {naming.get('issues_count', 0)}</p>")
                html.append("</div>")
            
            # Recommendations
            recommendations = self._generate_recommendations(result)
            if recommendations:
                html.append("<div class='metric'>")
                html.append("<h3>Recommendations</h3>")
                html.append("<ul>")
                for rec in recommendations:
                    html.append(f"<li>{rec}</li>")
                html.append("</ul>")
                html.append("</div>")
            
            html.append("</div>")
        
        html.append("</div>")
        html.append("</body>")
        html.append("</html>")
        
        html_text = "\n".join(html)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_text)
        
        return html_text
    
    def generate_json_report(self, results: List[Dict], output_path: str = None) -> str:
        """
        Generate a JSON report from analysis results.
        
        Args:
            results: List of analysis results
            output_path: Optional path to save report
            
        Returns:
            Report as JSON string
        """
        report = {
            'timestamp': self.timestamp,
            'files_analyzed': len(results),
            'results': results
        }
        
        json_text = json.dumps(report, indent=2, ensure_ascii=False)
        
        if output_path:
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(json_text)
        
        return json_text
    
    def _generate_recommendations(self, result: Dict) -> List[str]:
        """
        Генерирует рекомендации по улучшению кода на основе анализа.
        
        Алгоритм основан на выявлении проблемных областей и предложении
        конкретных действий для их исправления. Рекомендации приоритизируются
        по важности влияния на итоговую оценку.
        """
        recommendations = []
        
        # PEP 8 recommendations - важны для читаемости
        pep8 = result.get('pep8_score', {})
        if pep8.get('score', 100) < 80:
            violations_count = pep8.get('violations_count', 0)
            if violations_count > 0:
                recommendations.append(
                    f"Исправить {violations_count} нарушений PEP 8 для улучшения читаемости кода"
                )
        
        # Complexity recommendations - влияют на поддерживаемость
        complexity = result.get('complexity', {})
        avg_complexity = complexity.get('average', 0)
        if avg_complexity > 5:
            recommendations.append(
                f"Упростить функции со средней сложностью {avg_complexity:.1f} "
                "(рекомендуется <=5) путем разбиения на более мелкие функции"
            )
        max_complexity = complexity.get('max', 0)
        if max_complexity > 10:
            recommendations.append(
                f"Рефакторинг функций с высокой сложностью (максимум {max_complexity}, "
                "рекомендуется <=10)"
            )
        
        # Docstring recommendations - критично для понимания
        docstrings = result.get('docstring_coverage', {})
        coverage = docstrings.get('overall_coverage', 100)
        if coverage < 80:
            missing = docstrings.get('functions_total', 0) - docstrings.get('functions_with_doc', 0)
            missing += docstrings.get('classes_total', 0) - docstrings.get('classes_with_doc', 0)
            recommendations.append(
                f"Добавить docstrings к {missing} элементам кода "
                f"(текущее покрытие: {coverage:.1f}%, рекомендуется >=80%)"
            )
        
        # Duplication recommendations - влияют на архитектуру
        duplication = result.get('code_duplication', {})
        dup_pct = duplication.get('duplication_percentage', 0)
        if dup_pct > 10:
            recommendations.append(
                f"Уменьшить дублирование кода ({dup_pct:.1f}%, рекомендуется <=10%) "
                "путем выделения общей логики в отдельные функции"
            )
        
        # Naming recommendations (дополнительная проверка)
        naming = result.get('naming_quality', {})
        if naming and naming.get('score', 100) < 90:
            issues_count = naming.get('issues_count', 0)
            if issues_count > 0:
                recommendations.append(
                    f"Исправить именование в {issues_count} местах "
                    "(функции: snake_case, классы: PascalCase)"
                )
        
        # Empty lines ratio (дополнительная рекомендация)
        empty_ratio = result.get('empty_lines_ratio', 0)
        if empty_ratio > 20:
            recommendations.append(
                f"Слишком много пустых строк ({empty_ratio:.1f}%, оптимально 10-15%)"
            )
        elif empty_ratio < 5 and result.get('lines_of_code', 0) > 50:
            recommendations.append(
                "Добавить пустые строки для улучшения читаемости "
                "(оптимально 10-15% пустых строк)"
            )
        
        return recommendations

