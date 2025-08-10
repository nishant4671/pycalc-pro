"""
PyCalc Pro - Secure Python Calculator with CLI Interface
Fixed evaluation engine to pass all tests
"""

import ast
import operator
import argparse
import math

class PyCalc:
    """Core calculator engine with safe AST-based evaluation"""
    def __init__(self):
        self.history = []
        self.allowed_functions = {
            'sqrt': math.sqrt,
            'log': math.log,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'abs': abs,
            'round': round
        }
    
    def _safe_eval(self, expr: str) -> float:
        """Safely evaluate mathematical expressions using AST parsing"""
        # Replace ^ with ** for exponentiation
        expr = expr.replace('^', '**')
        
        try:
            # Parse expression to Abstract Syntax Tree
            tree = ast.parse(expr, mode='eval')
            
            # Validate AST nodes
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if not isinstance(node.func, ast.Name):
                        raise ValueError("Function calls must use named functions")
                    if node.func.id not in self.allowed_functions:
                        raise ValueError(f"Function {node.func.id} not allowed")
                
                # Block all other unsafe node types
                unsafe_nodes = (
                    ast.Attribute, ast.Subscript, ast.Starred, ast.ListComp,
                    ast.DictComp, ast.GeneratorExp, ast.Yield, ast.Lambda,
                    ast.FormattedValue, ast.JoinedStr, ast.AsyncFunctionDef,
                    ast.ClassDef, ast.Await, ast.Import, ast.ImportFrom
                )
                if isinstance(node, unsafe_nodes):
                    raise ValueError("Unsupported operation")
            
            # Compile and evaluate
            code = compile(tree, '<string>', 'eval')
            return eval(code, {'__builtins__': None}, self.allowed_functions)
            
        except (SyntaxError, ValueError, TypeError, NameError, MemoryError) as e:
            raise ValueError(f"Math error: {str(e)}")

    def calculate(self, expression: str) -> float:
        """Public calculation method with history tracking"""
        try:
            result = self._safe_eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
        except ValueError as e:
            return f"Error: {str(e)}"

    def convert_units(self, value: float, from_unit: str, to_unit: str) -> float:
        """Unit conversion between common units"""
        conversions = {
            'cm_to_inch': 0.393701,
            'kg_to_lb': 2.20462,
            'c_to_f': lambda x: (x * 9/5) + 32,
            'km_to_mile': 0.621371
        }
        key = f"{from_unit}_to_{to_unit}"
        if key in conversions:
            if callable(conversions[key]):
                return conversions[key](value)
            return value * conversions[key]
        return value  # No conversion if units not found

def main():
    calc = PyCalc()
    parser = argparse.ArgumentParser(
        description='PyCalc Pro - Advanced Secure Calculator',
        epilog='Example: python calculator.py "2^3 + sqrt(9)"'
    )
    parser.add_argument(
        'expression',
        help='Math expression (supports +-*/^, sqrt(), log(), etc.)'
    )
    parser.add_argument(
        '--convert',
        nargs=3,
        metavar=('VALUE', 'FROM_UNIT', 'TO_UNIT'),
        help='Unit conversion (e.g., 10 cm inch)'
    )
    
    args = parser.parse_args()
    
    if args.convert:
        value, from_unit, to_unit = args.convert
        try:
            result = calc.convert_units(float(value), from_unit, to_unit)
            print(f"Conversion: {value} {from_unit} = {result:.2f} {to_unit}")
        except ValueError:
            print("Error: Invalid conversion input")
    else:
        result = calc.calculate(args.expression)
        print(f"Result: {result}")

if __name__ == "__main__":
    main()
    