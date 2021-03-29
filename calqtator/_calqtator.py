from decimal import Decimal
from enum import Enum
from functools import partial

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import QWidget, QGridLayout, QPushButton, QLineEdit, QLabel


class Symbol(Enum):
    """The symbols of a calculator."""
    ZERO = '0'
    ONE = '1'
    TWO = '2'
    THREE = '3'
    FOUR = '4'
    FIVE = '5'
    SIX = '6'
    SEVEN = '7'
    EIGHT = '8'
    NINE = '9'
    ADDITION = '+'
    SUBTRACTION = '-'
    MULTIPLICATION = 'x'
    DIVISION = '/'
    EQUALS = '='
    CLEAR = 'C'
    ALL_CLEAR = 'AC'
    POINT = '.'


NUMBERS = {
    Symbol.ONE,
    Symbol.TWO,
    Symbol.THREE,
    Symbol.FOUR,
    Symbol.FIVE,
    Symbol.SIX,
    Symbol.SEVEN,
    Symbol.EIGHT,
    Symbol.NINE,
    Symbol.ZERO
}

OPERATORS = {
    Symbol.ADDITION,
    Symbol.SUBTRACTION,
    Symbol.MULTIPLICATION,
    Symbol.DIVISION
}


class ButtonGrid(QWidget):

    button_clicked = Signal(Symbol)

    def __init__(self, parent=None):
        super().__init__(parent)

        layout_map = [
            [None, None, Symbol.CLEAR, Symbol.ALL_CLEAR],
            [Symbol.SEVEN, Symbol.EIGHT, Symbol.NINE, Symbol.DIVISION],
            [Symbol.FOUR, Symbol.FIVE, Symbol.SIX, Symbol.MULTIPLICATION],
            [Symbol.ONE, Symbol.TWO, Symbol.THREE, Symbol.SUBTRACTION],
            [Symbol.ZERO, Symbol.POINT, Symbol.EQUALS, Symbol.ADDITION]
        ]

        layout = QGridLayout()

        for row, columns in enumerate(layout_map):
            for column, symbol in enumerate(columns):
                if symbol is None:
                    continue
                button = QPushButton(symbol.value)
                button.clicked.connect(partial(self.button_clicked.emit, symbol))
                layout.addWidget(button, row, column)
                shortcut = QShortcut(QKeySequence(symbol.value), self)
                shortcut.activated.connect(button.click)

                alt_shortcut = None

                if symbol == Symbol.MULTIPLICATION:
                    alt_shortcut = QShortcut(QKeySequence('*'), self)
                elif symbol == Symbol.EQUALS:
                    alt_shortcut = QShortcut(QKeySequence.InsertParagraphSeparator, self)

                if alt_shortcut:
                    alt_shortcut.activated.connect(button.click)

        self.setLayout(layout)


class CalQtator(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._expression = '0'
        self.result = None

        self.operator = QLabel()

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.display.setText(Symbol.ZERO.value)

        self.button_grid = ButtonGrid()
        self.button_grid.button_clicked.connect(self.handle_button_clicked)

        layout = QGridLayout()

        layout.addWidget(self.display, 0, 0)
        layout.addWidget(self.operator, 0, 1)
        layout.addWidget(self.button_grid, 1, 0)

        self.setLayout(layout)

    @property
    def expression(self) -> str:
        return self._expression

    @expression.setter
    def expression(self, value) -> None:
        self._expression = value

    @property
    def last_symbol(self) -> Symbol:
        return Symbol(self.last_statement[-1])

    @property
    def last_statement(self) -> str:
        return self.expression.strip().split(' ')[-1]

    def handle_button_clicked(self, symbol: Symbol):

        last_statement = self.last_statement
        last_symbol = self.last_symbol

        if symbol == Symbol.EQUALS:
            if last_symbol in OPERATORS:
                self.expression = self.expression.removesuffix(last_symbol.value)

            operator_values = [o.value for o in OPERATORS]
            prepared_stmts = []
            stmts = self.expression.split()
            for stmt in stmts:
                if stmt not in operator_values:
                    stmt = f'Decimal("{stmt}")'
                if stmt == Symbol.MULTIPLICATION.value:
                    stmt = '*'
                prepared_stmts.append(stmt)

            prepared_expr = ' '.join(prepared_stmts)
            equals: Decimal = eval(prepared_expr)
            self.result = str(equals).removesuffix('.0')
            self.expression = self.result
            self.display.setText(self.result)

        elif symbol == Symbol.CLEAR:
            if last_symbol in OPERATORS:
                self.expression = self.expression.removesuffix(last_symbol.value)
            else:
                self.expression = self.expression.removesuffix(last_statement)
                if not self.expression:
                    self.expression = '0'
                self.display.setText('0')

        elif symbol == Symbol.ALL_CLEAR:
            self.expression = '0'
            self.result = None
            self.display.setText(self.expression)

        elif symbol in NUMBERS:
            if self.result:
                self.result = None
                self.expression = symbol.value
                self.display.setText(self.expression)
            elif last_statement == '0':
                self.result = None
                self.display.setText(symbol.value)
                self.expression = self.expression.removesuffix('0')
                self.expression += symbol.value
            elif last_symbol in NUMBERS:
                self.result = None
                self.expression = self.expression.removesuffix(last_statement)
                last_statement += symbol.value
                self.expression += last_statement
                self.display.setText(last_statement)
            elif last_symbol in OPERATORS:
                self.result = None
                self.expression += f' {symbol.value}'
                self.display.setText(self.last_statement)
            elif last_symbol == Symbol.POINT:
                self.expression += symbol.value
                self.display.setText(self.last_statement)

        elif symbol in OPERATORS:
            self.result = None
            if last_symbol in OPERATORS:
                self.expression = self.expression.removesuffix(last_statement)
            self.expression += f' {symbol.value}'

        elif symbol == Symbol.POINT:
            if self.result:
                self.result = None
                self.expression = '0' + symbol.value
                self.display.setText(self.expression)
            elif last_symbol in OPERATORS:
                self.expression = '0' + symbol.value
                self.display.setText(self.expression)
            elif last_symbol in NUMBERS:
                if Symbol.POINT.value not in last_statement:
                    self.expression += symbol.value
                    self.display.setText(self.last_statement)
