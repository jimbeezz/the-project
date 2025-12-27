"""
Sample student code for testing the code quality assessment tool.
This file demonstrates various code quality issues.
"""

def calculate_sum(a, b):
    # Missing docstring
    return a + b

def complex_function(x, y, z):
    # High complexity function
    if x > 0:
        if y > 0:
            if z > 0:
                if x + y > z:
                    if x + z > y:
                        if y + z > x:
                            return "valid triangle"
                        else:
                            return "invalid"
                    else:
                        return "invalid"
                else:
                    return "invalid"
            else:
                return "invalid"
        else:
            return "invalid"
    else:
        return "invalid"

class StudentClass:
    # Missing docstring
    def method1(self):
        return 1
    
    def method2(self):
        return 2

# Code duplication example
def duplicate_code_1():
    x = 1
    y = 2
    z = x + y
    result = z * 2
    return result

def duplicate_code_2():
    x = 1
    y = 2
    z = x + y
    result = z * 2
    return result

# PEP 8 violations
def bad_formatting( ):
    x=1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17+18+19+20+21+22+23+24+25  # Line too long
    return x

