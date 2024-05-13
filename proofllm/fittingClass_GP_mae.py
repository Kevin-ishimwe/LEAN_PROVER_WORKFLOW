import numpy as np
import json
import re
from scipy import optimize as opt
from sklearn.metrics import mean_squared_error, mean_absolute_error
import math

class FittingOptimizer:
    def __init__(self):
        self.results = []
        self.all_operator_pattern = re.compile(r'\*{2}|\*{1}|[+]|[-]|[/]')
        self.equation_indices_pattern = re.compile(r'c\[(\d+)\]')



    @staticmethod
    def format_expressions(expressions):
        formatted_expressions = []

        for expression in expressions:
            # Split the expression into left (variable) and right (formula) parts
            if "=" in expression:
                _, formula = expression.split("=")  # We are discarding the left side
                formula = formula.strip()
            else:
                formula = expression.strip()

            # Process the formula (right side)
            formula = re.sub(r"\\sqrt\{([^}]+)\}", r"(\1)**0.5", formula)  # Replace \sqrt{content} with content**0.5
            formula = re.sub(r"\\cbrt\{([^}]+)\}", r"(\1)**(1/3)", formula)  # Replace \cbrt{content} with content**(1/3)
            formula = formula.replace(r"\log", "log").replace(r"\exp", "exp")
            formula = re.sub(r'cube_root\(([^)]+)\)', r'\1**(1/3)', formula)
            formula = re.sub(r'cubert\(([^)]+)\)', r'\1**(1/3)', formula)
            formula = re.sub(r'cube\(([^)]+)\)', r'\1**3', formula)
            formula = re.sub(r'square\(([^)]+)\)', r'\1**2', formula)
            formula = formula.replace("log10*", "log")
            formula = formula.replace("e**", "exp")
            formula = re.sub(r"c(\d+)", r"c[\1]", formula)  # Replace c0, c1, etc. with c[0], c[1], etc.
            formula = re.sub(r"\{([^}]+)\}", r"(\1)", formula) # Replace { } with ( )
            formula = formula.replace("^", "**")  # Replace ^ with **
            formula = formula.replace(" ", "")  # Remove white space
            formula = re.sub(r"(?<![a-zA-Z])x(?![a-zA-Z0-9])", "x1", formula)  # Replace x with x1 if it's not followed by a digit
            formula = re.sub(r"(?<![a-zA-Z])y(?![a-zA-Z0-9])", "x2", formula)  # Replace y with x2 if it's not followed by a digit
            formula = re.sub(r"(?<![a-zA-Z])z(?![a-zA-Z0-9])", "x3", formula)  # Replace z with x3 if it's not followed by a digit
            formula = formula.replace("$", "") #Replace $ signs if present

            formatted_expressions.append(formula)

        return formatted_expressions



    def get_equation_indices(self, equation):
        return sorted([int(index) for index in self.equation_indices_pattern.findall(equation)],
                      reverse=True)

    def calculate_mae(self, equation, data, fitted_params):
        num_indep_vars = data.shape[1] - 1
        x = data[:, :num_indep_vars]
        y = data[:, num_indep_vars]
        predicted_y = eval(equation, {'c': fitted_params, 'np': np,'sqrt': np.sqrt, 'cbrt': np.cbrt, 'log': np.log, 'exp': np.exp, **{f'x{i+1}':x[:,i].reshape(-1) for i in range(num_indep_vars)}})

        if np.isscalar(predicted_y):
            predicted_y = np.full(y.shape, predicted_y)
        mae = mean_absolute_error(y, predicted_y)
        return round(mae, 8)

    def calculate_complexity(self, equation):
        complexity = (len(self.all_operator_pattern.findall(equation)) * 2) + 1
        return complexity

    def equation_error(self, c, equation, data):
        num_indep_vars = data.shape[1] - 1
        x = data[:, :num_indep_vars]
        return np.mean((eval(equation, {'c': c, 'np': np, 'sqrt': np.sqrt, 'cbrt': np.cbrt, 'log': np.log, 'exp': np.exp, **{f'x{i+1}':x[:,i].reshape(-1) for i in range(num_indep_vars)}}) - data[:, num_indep_vars])**2)


    def fitting_constants(self, indep_vars, dep_var, expressions, results=None):
        # Format the expressions first
        expressions = self.format_expressions(expressions)

        # Reshape the inputs and stack the data
        data = np.column_stack([var.reshape(-1, 1) if isinstance(var, np.ndarray) else np.array(eval(var)).reshape(-1, 1) for var in indep_vars] +
                               [dep_var.reshape(-1, 1) if isinstance(dep_var, np.ndarray) else np.array(eval(dep_var)).reshape(-1, 1)])

        # Parse expressions as JSON if it's a string
        if isinstance(expressions, str):
            expressions = json.loads(expressions)

        if results is None:
            results = []
        else:
            results = json.loads(results)

        for equation in expressions:
            equation_indices = self.get_equation_indices(equation)
            constant = len(equation_indices)
            initial_val = [1] * constant

            undesired_patterns = [r"sin", r"cos", r"tan"]
            if any(re.search(pattern, equation) for pattern in undesired_patterns):
                result_dict = {'equation': equation, 'complexity': self.calculate_complexity(equation), 'mae': float('inf')}
                results.append(result_dict)
                continue


            # Check if equation indices are within the available parameters
            if all(index < constant for index in equation_indices):
                try:
                    result = opt.basinhopping(func=self.equation_error, x0=initial_val,
                                          minimizer_kwargs={"method": "Nelder-Mead",
                                                            "args": (equation, data)})
                    fitted_params = result.x

                    mae = self.calculate_mae(equation, data, fitted_params)
                    complexity = self.calculate_complexity(equation)

                    result_dict = {'equation': equation, 'complexity': complexity, 'mae': mae}
                    results.append(result_dict)
                except (ValueError, RuntimeError, NameError, SyntaxError) as e:
                    high_mae_value = float('inf') # Assigning a sufficiently large value
                    result_dict = {'equation': equation, 'complexity': self.calculate_complexity(equation), 'mae': high_mae_value}
                    results.append(result_dict)

        results.sort(key=lambda x: (x['mae'], x['complexity']))
        return json.dumps(results, indent=3)
