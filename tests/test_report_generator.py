"""
Unit tests for ReportGenerator class.
"""

import pytest
import tempfile
from src.report_generator import ReportGenerator


class TestReportGenerator:
    """Test cases for ReportGenerator."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = ReportGenerator()
        self.sample_results = [
            {
                'file': 'test.py',
                'overall_score': 75.5,
                'pep8_score': {
                    'score': 80.0,
                    'violations_count': 5,
                    'violations': [
                        {'line': 10, 'type': 'line_too_long', 'message': 'Line too long'}
                    ]
                },
                'complexity': {
                    'average': 3.5,
                    'max': 7,
                    'functions': [
                        {'name': 'test_func', 'line': 5, 'complexity': 3}
                    ]
                },
                'docstring_coverage': {
                    'overall_coverage': 70.0,
                    'functions_with_doc': 2,
                    'functions_total': 3
                },
                'code_duplication': {
                    'duplication_percentage': 5.0,
                    'duplicate_blocks': 1
                },
                'functions_count': 3,
                'classes_count': 1,
                'lines_of_code': 50
            }
        ]
    
    def test_generate_text_report(self):
        """Test text report generation."""
        report = self.generator.generate_text_report(self.sample_results)
        
        # Проверяем наличие основных элементов отчета
        assert "ОТЧЕТ О КАЧЕСТВЕ КОДА" in report or "test.py" in report
        assert "test.py" in report
        assert "75.50" in report or "75.5" in report
        assert "PEP 8" in report or "pep8" in report.lower()
        assert "сложность" in report.lower() or "complexity" in report.lower()
    
    def test_generate_html_report(self):
        """Test HTML report generation."""
        report = self.generator.generate_html_report(self.sample_results)
        
        assert "<html>" in report
        assert "<!DOCTYPE html>" in report
        assert "test.py" in report
        assert "75.5" in report
    
    def test_generate_json_report(self):
        """Test JSON report generation."""
        report = self.generator.generate_json_report(self.sample_results)
        
        assert '"file"' in report
        assert '"test.py"' in report
        assert '"overall_score"' in report
    
    def test_save_report_to_file(self):
        """Test saving report to file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt', encoding='utf-8') as f:
            temp_path = f.name
        
        try:
            self.generator.generate_text_report(self.sample_results, temp_path)
            
            with open(temp_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Проверяем, что отчет сохранен (любой из ключевых элементов)
                assert "test.py" in content or "ОТЧЕТ" in content or "75.5" in content
        finally:
            import os
            os.unlink(temp_path)
    
    def test_recommendations_generation(self):
        """Test recommendations generation."""
        # This is tested indirectly through report generation
        report = self.generator.generate_text_report(self.sample_results)
        
        # Проверяем наличие рекомендаций (на русском или английском)
        assert "РЕКОМЕНДАЦИИ" in report or "RECOMMENDATIONS" in report or "docstrings" in report.lower()

