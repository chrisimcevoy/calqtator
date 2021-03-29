# CalQtator
A simple calculator widget built with [PySide6](https://wiki.qt.io/Qt_for_Python).

![](https://raw.githubusercontent.com/chrisimcevoy/calqtator/main/calqtator.png)

## Installation

`$ pip install calqtator`

## Usage

Terminal:

`$ calqtator`

Embed CalQtator in an existing app:

```python
import sys

from PySide6.QtWidgets import QApplication, QMainWindow

from calqtator import CalQtator


def main():
    app = QApplication(sys.argv)
    main_window = QMainWindow()
    main_window.setCentralWidget(CalQtator())
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    main()
```

## Changelog

- 0.2.0
    - Added Changelog to README.md.
    - Button reorganisation.
    - More key bindings.
    - Anticipate unexpected EOF exceptions when `=` is triggered.
- 0.1.0
    - Basic calculator functionality.
