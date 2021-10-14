# Shunting-yard algorithm

class Tokenizer:

    def __init__(self):
        self._Token = []
        self._Expression = ''
        self._CharIndex = 0
        self._ExpressionLen = 0

    def _IsExpressionNotEmpty(self):
        return self._CharIndex < self._ExpressionLen

    def _GetExpressionCurrentChar(self):
        return self._Expression[self._CharIndex]

    def _ParseSpace(self):
        IsSpace = self._GetExpressionCurrentChar() == ' '
        while self._IsExpressionNotEmpty() and self._GetExpressionCurrentChar() == ' ':
            self._CharIndex += 1

        return IsSpace

    def _ParseNumber(self):
        def _AddDecimals(numberValue):
            Weight = 0.1
            self._CharIndex += 1
            while self._IsExpressionNotEmpty() and self._GetExpressionCurrentChar().isnumeric():
                numberValue += Weight * int(self._GetExpressionCurrentChar())
                Weight /= 10
                self._CharIndex += 1
            return numberValue

        IsANumber = self._GetExpressionCurrentChar().isnumeric()

        NumberValue = 0
        while self._IsExpressionNotEmpty() and self._GetExpressionCurrentChar().isnumeric():
            NumberValue *= 10
            NumberValue += int(self._GetExpressionCurrentChar())
            self._CharIndex += 1

        if self._CharIndex >= self._ExpressionLen:
            self._Token.append(('NUM', NumberValue))
            return IsANumber

        if self._GetExpressionCurrentChar() == '.':
            NumberValue = _AddDecimals(NumberValue)    

        if IsANumber:
            self._Token.append(('NUM', NumberValue))

        return IsANumber

    def _ParseOperator(self):

        if self._CharIndex >= self._ExpressionLen:
            return

        if self._GetExpressionCurrentChar() == '(':
            self._Token.append(('PARENT', 'OPEN'))
        elif self._GetExpressionCurrentChar() == ')':
            self._Token.append(('PARENT', 'CLOSE'))
        else:
            SwitchOperator = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}
            self._Token.append(('OP', SwitchOperator.get(self._GetExpressionCurrentChar())))

        self._CharIndex += 1 

    def Tokenize(self, Expression):
        """Tokenize an infix expression

        Args:
            Expression (string): an infix expression

        Returns:
            string: a token
        """
        self._Token = []
        self._Expression = Expression
        self._CharIndex = 0
        self._ExpressionLen = len(Expression)

        while self._IsExpressionNotEmpty():
            if self._ParseSpace():
                continue

            if self._ParseNumber():
                continue

            self._ParseOperator()

        return self._Token


class RPNCalculator:

    def __init__(self):
        self._Stack = []

    def PushValue(self, Value):
        self._Stack.append(Value)

    def ApplyOperator(self, Operator):
        def Add():
            return OperandB + OperandA

        def Sub():
            return OperandB - OperandA

        def Mul():
            return OperandB * OperandA

        def Div():
            return OperandB / OperandA

        SwitchOperator = {'ADD': Add, 'SUB': Sub, 'MUL': Mul, 'DIV': Div}

        OperandA = self._Stack.pop()
        OperandB = self._Stack.pop()

        Result = SwitchOperator.get(Operator)()

        self._Stack.append(Result)

    def EvaluateRPNExpression(self, RPNExpression):

        for CurrentTokenType, CurrentTokenValue in RPNExpression:
            if CurrentTokenType == 'NUM':
                self.PushValue(CurrentTokenValue)
            elif CurrentTokenType == 'OP':
                self.ApplyOperator(CurrentTokenValue)

        return self._Stack[-1]

    def Top(self):
        return self._Stack[-1]


class Infix2RPN:

    def __init__(self):
        self._Token = []
        self._Tokenizer = Tokenizer()
        self._RPNCalculator = RPNCalculator()
        self._OperatorStack = []
        self._RPNExpression = []
    
    def Convert2RPN(self, InfixExpression):
        """Convert an infix expression in Reverse Polish Notation

        Args:
            InfixExpression (string): Infix expression

        Returns:
            [string]: RPN expression
        """
        InfixToken = self._Tokenizer.Tokenize(InfixExpression)

        for CurrentTokenType, CurrentTokenValue in InfixToken:
            if CurrentTokenType == 'NUM':
                self._HandleNum(CurrentTokenValue);
            elif CurrentTokenValue == 'OPEN':
                self._HandleOpen()
            elif CurrentTokenValue == 'CLOSE':
                self._HandleClose()
            elif CurrentTokenType == 'OP':
                self._HandleOperator(CurrentTokenValue)
                
        return self._RPNExpression + self._OperatorStack

    def _HandleNum(self, value):
        """Append number to RPN Expression

        Args:
            value (number): the number
        """
        self._RPNExpression.append(('NUM', value))

    def _HandleOpen(self):
        """Handle open parenthesis
        """
        self._OperatorStack.append(('PARENT', 'OPEN'))

    def _HandleClose(self):
        """Handle closing parenthesis
        """

        self._RPNExpression.append(self._OperatorStack.pop())
        while len(self._OperatorStack) > 0 and self._OperatorStack[-1] != ('PARENT', 'OPEN'):
            self._RPNExpression.append(self._OperatorStack.pop())

    def _HandleOperator(self, value):
        """Append an operator to the right stack

        Args:
            value (string): the operator
        """
        OperatorPriority = {'ADD': 2, 'SUB': 2, 'MUL': 3, 'DIV': 3}

        StackTop = len(self._OperatorStack) - 1
        while StackTop >= 0 and self._OperatorStack[StackTop][0] == 'OP':
            if OperatorPriority.get(self._OperatorStack[StackTop][1]) >= OperatorPriority.get(
                    value):
                self._RPNExpression.append(self._OperatorStack.pop())
            StackTop -= 1
        self._OperatorStack.append(('OP', value))



MyRPN = RPNCalculator()
MyInfix2RPN = Infix2RPN()
MyTokenizer = Tokenizer()

InfixExpression = '(458.32 + 78 / 10) / (14.7898 - 32 * 7)'
TokenInfix = MyTokenizer.Tokenize(InfixExpression)
MyRPNExpression = MyInfix2RPN.Convert2RPN(InfixExpression)
EvaluatedExpression = MyRPN.EvaluateRPNExpression(MyRPNExpression)

print('Infix -> ', InfixExpression)
print('Infix Token ->', TokenInfix)
print('RPN Token -> ', MyRPNExpression)
print('Evaluated -> ', EvaluatedExpression)
print('Control -> ', eval(InfixExpression))