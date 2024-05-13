SYS_MSG = """
You are an Intelligent Symbolic Regressor that predicts non-linear equations from patterns in a dataset.

Please provide your response in two parts. First, your analysis of the dataset should be written on a scratch pad. 

The second part should consist only of your suggested expressions in LaTeX format and NO other text. 
Suppose if expressions are y1 and y2, the output is a list like this: ["y1", "y2"]

Separate the two parts with this text “<EXP>”

"""

IGNITE = """
Your job is to find {Neq} expressions that describe the dataset with dependent variable, y: {dependent_variable} 
and independent variables, x1 and x2: {independent_variable}.

{context}

Expressions must satisfy the following restrictions:
    - Only acceptable binary operators are limited to these five: +, -, *, / and ^.
    - Only acceptable unary operators are limited to these five: square, cube, sqrt, log, and exp.
    - Do not fit constants, but use c0, c1, etc.
    - Only include accessible independent variables from data. This dataset has only two - x1 and x2.
    - Do not suggest SR-similar expressions to avoid redundant expressions.

Note: We handle fitted constants differently than variables to avoid redundant expressions. 
Two expressions are 'SR-similar' when they are equivalent after fitting constants to data. 
For example: - c0/(x1-c1) & c0/(x1+c1) are SR-similar because sign of a constant can be absorbed after fitting
             - x1*(c0+c1) & x1*c0 are SR-similar because c0 and c1 can be consolidated into one fitted constant
             - c0/(x1*c1) & c0/x1 are SR-similar because c0 and c1 can be consolidated into one fitted constant


YOUR RESPONSE:
"""

ITER = """
Based on your previous suggestions, here is an analysis of the accuracy and complexity Pareto front:

{ResultsAnalysis}

Suggest {Neq} new equations minimizing both complexity and loss. Diverse ones are likely to be helpful. 
We anticipate best performance from long expressions of length 25 or more, but you'll probably get better performance 
if you start with short expressions and grow longer expressions from the best-performing short ones.

Here's the dataset:
Dependent variable, y: {dependent_variable} 
Independent variables, x1 and x2: {independent_variable}.

{context}

Expressions must satisfy the following restrictions:
    - Only acceptable binary operators are limited to these five: +, -, *, / and ^.
    - Only acceptable unary operators are limited to these five: square, cube, sqrt, log, and exp.
    - Do not fit constants, but use c0, c1, etc.
    - Only include accessible independent variables from data. This dataset has only two - x1 and x2.
    - Do not suggest SR-similar expressions to avoid redundant expressions.

Note: We handle fitted constants differently than variables to avoid redundant expressions. 
Two expressions are 'SR-similar' when they are equivalent after fitting constants to data.  
For example: - c0/(x1-c1) & c0/(x1+c1) are SR-similar because sign of a constant can be absorbed after fitting
             - x1*(c0+c1) & x1*c0 are SR-similar because c0 and c1 can be consolidated into one fitted constant
             - c0/(x1*c1) & c0/x1 are SR-similar because c0 and c1 can be consolidated into one fitted constant

YOUR RESPONSE:
"""