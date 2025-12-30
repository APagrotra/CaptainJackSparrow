"""
Calculator Tool for Mathematical Operations
Safely evaluates mathematical expressions
"""

import re
import operator
from typing import Union, Dict
import ast


class Calculator:
    """Safe calculator for evaluating mathematical expressions"""
    
    # Supported operators
    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
    }
    
    def __init__(self):
        """Initialize the calculator"""
        print("Calculator tool initialized")
    
    def _safe_eval(self, node) -> Union[int, float]:
        """
        Safely evaluate an AST node
        
        Args:
            node: AST node to evaluate
            
        Returns:
            Result of evaluation
        """
        if isinstance(node, ast.Num):  # Number
            return node.n
        elif isinstance(node, ast.BinOp):  # Binary operation
            left = self._safe_eval(node.left)
            right = self._safe_eval(node.right)
            op = self.OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operation: {type(node.op)}")
            return op(left, right)
        elif isinstance(node, ast.UnaryOp):  # Unary operation
            operand = self._safe_eval(node.operand)
            op = self.OPERATORS.get(type(node.op))
            if op is None:
                raise ValueError(f"Unsupported operation: {type(node.op)}")
            return op(operand)
        else:
            raise ValueError(f"Unsupported expression: {type(node)}")
    
    def calculate(self, expression: str) -> Dict[str, Union[str, float, bool]]:
        """
        Calculate the result of a mathematical expression
        
        Args:
            expression: Mathematical expression as string
            
        Returns:
            Dictionary with 'success', 'result', and 'error' keys
        """
        try:
            # Remove whitespace
            expression = expression.strip()
            
            # Parse the expression into an AST
            tree = ast.parse(expression, mode='eval')
            
            # Evaluate the expression
            result = self._safe_eval(tree.body)
            
            return {
                'success': True,
                'result': result,
                'error': None
            }
        
        except ZeroDivisionError:
            return {
                'success': False,
                'result': None,
                'error': "Cannot divide by zero, mate!"
            }
        except Exception as e:
            return {
                'success': False,
                'result': None,
                'error': f"Invalid expression: {str(e)}"
            }
    
    def extract_and_calculate(self, text: str) -> Union[Dict, None]:
        """
        Extract mathematical expression from text and calculate
        
        Args:
            text: Text that may contain a mathematical expression
            
        Returns:
            Calculation result or None if no expression found
        """
        # Look for patterns like "calculate X" or "what is X"
        patterns = [
            r'calculate\s+([0-9+\-*/().^ ]+)',
            r'what\s+is\s+([0-9+\-*/().^ ]+)',
            r'compute\s+([0-9+\-*/().^ ]+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text.lower())
            if match:
                expression = match.group(1).strip()
                # Replace ^ with ** for power
                expression = expression.replace('^', '**')
                return self.calculate(expression)
        
        return None


def format_calculator_response(result: Dict, pirate_style: bool = True) -> str:
    """
    Format calculator result as a pirate-style response
    
    Args:
        result: Result dictionary from Calculator.calculate()
        pirate_style: Whether to use pirate-style language
        
    Returns:
        Formatted response string
    """
    if result['success']:
        value = result['result']
        if pirate_style:
            return f"By me calculations, that be **{value}**, savvy?"
        else:
            return f"The result is {value}"
    else:
        if pirate_style:
            return f"Arr, there be a problem with yer sum: {result['error']}"
        else:
            return f"Error: {result['error']}"


if __name__ == "__main__":
    # Test the calculator
    print("Testing Calculator...")
    
    calc = Calculator()
    
    # Test cases
    test_expressions = [
        "2 + 2",
        "15 * 12",
        "100 / 4",
        "2 ** 3",  # Power
        "10 - 5 * 2",  # Order of operations
        "10 / 0",  # Division by zero
        "(3 + 5) * 2",
    ]
    
    print("\nTest Results:")
    for expr in test_expressions:
        result = calc.calculate(expr)
        print(f"\n{expr} = ", end="")
        print(format_calculator_response(result))
    
    # Test extraction
    print("\n\nTesting extraction from text:")
    text = "Can you calculate 25 * 4 for me?"
    result = calc.extract_and_calculate(text)
    if result:
        print(f"Text: '{text}'")
        print(f"Result: {format_calculator_response(result)}")
