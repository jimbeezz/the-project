"""
Unit tests for CodeAnalyzer class.
"""

import pytest
import tempfile
import os
from pathlib import Path
from src.code_analyzer import CodeAnalyzer


class TestCodeAnalyzer:
    """Test cases for CodeAnalyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = CodeAnalyzer()
    
    def test_analyze_simple_file(self):
        """Test analysis of a simple Python file."""
        code = """
def hello():
    print("Hello, World!")

class TestClass:
    def method(self):
        return True
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = self.analyzer.analyze_file(temp_path)
            
            assert 'overall_score' in result
            assert 'pep8_score' in result
            assert 'complexity' in result
            assert 'docstring_coverage' in result
            assert 'code_duplication' in result
            assert result['functions_count'] == 2
            assert result['classes_count'] == 1
        finally:
            os.unlink(temp_path)
    
    def test_pep8_violations(self):
        """Test PEP 8 violation detection."""
        code = "x = 1" + " " * 10 + "\n"  # Trailing whitespace
        code += "a" * 100 + "\n"  # Line too long
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = self.analyzer.analyze_file(temp_path)
            pep8 = result['pep8_score']
            
            assert pep8['violations_count'] > 0
            assert pep8['score'] < 100
        finally:
            os.unlink(temp_path)
    
    def test_complexity_calculation(self):
        """Test cyclomatic complexity calculation."""
        code = """
def complex_function(x):
    if x > 0:
        if x > 10:
            if x > 20:
                return x
            return x * 2
        return x * 3
    else:
        return 0
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = self.analyzer.analyze_file(temp_path)
            complexity = result['complexity']
            
            assert complexity['max'] >= 4  # Multiple if statements
            assert 'complex_function' in [f['name'] for f in complexity['functions']]
        finally:
            os.unlink(temp_path)
    
    def test_docstring_coverage(self):
        """Test docstring coverage detection."""
        code = """
def documented():
    \"\"\"This function has a docstring.\"\"\"
    pass

def not_documented():
    pass

class DocumentedClass:
    \"\"\"This class has a docstring.\"\"\"
    pass

class NotDocumentedClass:
    pass
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = self.analyzer.analyze_file(temp_path)
            docstrings = result['docstring_coverage']
            
            assert docstrings['functions_with_doc'] == 1
            assert docstrings['functions_total'] == 2
            assert docstrings['classes_with_doc'] == 1
            assert docstrings['classes_total'] == 2
            assert docstrings['overall_coverage'] == 50.0
        finally:
            os.unlink(temp_path)
    
    def test_duplication_detection(self):
        """Test code duplication detection."""
        code = """
def func1():
    x = 1
    y = 2
    z = x + y
    return z

def func2():
    x = 1
    y = 2
    z = x + y
    return z
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = self.analyzer.analyze_file(temp_path)
            duplication = result['code_duplication']
            
            # Should detect some duplication
            assert 'duplication_percentage' in duplication
            assert 'duplicate_blocks' in duplication
        finally:
            os.unlink(temp_path)
    
    def test_invalid_file(self):
        """Test handling of invalid file path."""
        result = self.analyzer.analyze_file("nonexistent_file.py")
        
        assert 'error' in result
    
    def test_syntax_error(self):
        """Test handling of syntax errors."""
        code = "def invalid syntax here"
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = self.analyzer.analyze_file(temp_path)
            assert 'error' in result
        finally:
            os.unlink(temp_path)
    
    def test_overall_score_calculation(self):
        """Test overall score calculation."""
        code = """
def well_documented():
    \"\"\"A well-documented function.\"\"\"
    return True
"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_path = f.name
        
        try:
            result = self.analyzer.analyze_file(temp_path)
            
            assert 'overall_score' in result
            assert 0 <= result['overall_score'] <= 100
        finally:
            os.unlink(temp_path)

