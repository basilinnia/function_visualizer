import sys
from math import sqrt

from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QLineEdit, QPushButton, \
    QHBoxLayout, QSizePolicy, QMessageBox, QToolTip
from matplotlib import pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


def calculate_nth_term(a, b, x0, n):
    global x_curr
    r = (-b) / (2 * a)
    if n == 0:
        return x0
    x_prev = x0
    for i in range(1, n + 1):
        x_curr = (sqrt(
            (a ** 2) * ((x_prev - r) ** 2) + sqrt(
                4 * (a ** 2) * ((x_prev - r) ** 2) + 1) + 1) / a) + r
        x_prev = x_curr
    return x_curr


def draw_circles(a, b, c, xf, ax):
    for i in range(0, 11):
        x0 = calculate_nth_term(a, b, xf, i)
        r = (-1 * b) / (2 * a)
        radius = (sqrt((x0 - r) ** 2 + (1 / (4 * a ** 2))))
        center_x = r
        center_y = ((a * x0 * x0) + (b * x0) + c + 1 / (2 * a))

        ax.add_patch(plt.Circle((center_x, center_y), radius, fill=False))

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Parabol ve Çemberler")
        self.setMouseTracking(True)

        # create the Matplotlib canvas
        self.canvas = FigureCanvas(Figure(figsize=(10, 10)))
        self.canvas.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.a_label, self.b_label, self.c_label = QLabel('a:'), QLabel('b:'), QLabel('c:')
        self.a_edit, self.b_edit, self.c_edit = QLineEdit(), QLineEdit(), QLineEdit()
        self.draw_button = QPushButton('Çiz')

        self.n_label, self.x0_label = QLabel('n:'), QLabel('x<sub>0:')
        self.n_edit, self.x0_edit = QLineEdit(), QLineEdit()
        self.calc_button = QPushButton("Hesapla")
        self.result_label = QLabel()
        self.first_label = QLabel(
            f"<p style='font-size: 19px'>ax<sup>2</sup> + bx + c parabolü için: </p>")
        self.explain_label = QLabel(
            "<p style='font-size: 19px'>x<sub>0</sub> 'a göre x<sub>n</sub> değeri: </p>")

        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.canvas)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.a_label)
        hbox1.addWidget(self.a_edit)
        hbox1.addWidget(self.b_label)
        hbox1.addWidget(self.b_edit)
        hbox1.addWidget(self.c_label)
        hbox1.addWidget(self.c_edit)
        hbox1.addWidget(self.x0_label)
        hbox1.addWidget(self.x0_edit)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.n_label)
        hbox2.addWidget(self.n_edit)
        hbox2.addWidget(self.calc_button)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.first_label)
        vbox2.addLayout(hbox1)
        vbox2.addWidget(self.explain_label)
        vbox2.addLayout(hbox2)
        vbox2.addWidget(self.result_label)
        vbox2.addWidget(self.draw_button)

        widget = QWidget()
        hbox3 = QHBoxLayout(widget)
        hbox3.addLayout(vbox1)
        hbox3.addLayout(vbox2)

        self.setCentralWidget(widget)

        toolbar = NavigationToolbar(self.canvas, self)
        self.addToolBar(toolbar)


        self.init_connections()
        self.set_validators()

    def set_validators(self):
        reg = QRegularExpression("[+-]?[0-9]\\d*\\.?\\d{6}")
        regValidator = QRegularExpressionValidator(reg)
        self.a_edit.setValidator(regValidator)
        self.b_edit.setValidator(regValidator)
        self.c_edit.setValidator(regValidator)
        self.x0_edit.setValidator(regValidator)

    def init_connections(self):
        self.a_edit.textChanged.connect(self.draw_parabola)
        self.b_edit.textChanged.connect(self.draw_parabola)
        self.c_edit.textChanged.connect(self.draw_parabola)
        self.draw_button.clicked.connect(self.draw_parabola)
        self.calc_button.clicked.connect(self.calculate)

    def draw_parabola(self):
        try:
            a = float(self.a_edit.text())

            if a == 0:
                raise ZeroDivisionError

            b = float(self.b_edit.text())
            c = float(self.c_edit.text())
            x0 = float(self.x0_edit.text())

        except ZeroDivisionError:
            return

        except:
            self.statusBar().showMessage('Tüm değerleri sayı formatında girdiğinizden emin olunuz !')
            return

        self.statusBar().clearMessage()

        # clear the canvas
        self.canvas.figure.clear()

        # define x-axis range
        x = np.linspace(-600, 600, 1200)
        # calculate y-values for parabola
        y = a * x ** 2 + b * x + c

        # plot the parabola on the canvas
        ax = self.canvas.figure.add_subplot(1, 1, 1)
        ax.spines['left'].set_position('center')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')
        ax.plot(x, y)
        ax.set_xlim(-600, 600)
        ax.set_ylim(-600, 600)

        draw_circles(a, b, c, x0, ax)

        # redraw the canvas
        self.canvas.draw()

    def calculate(self):
        global x_curr
        try:
            n = int(self.n_edit.text())
            x0 = float(self.x0_edit.text())

            a = float(self.a_edit.text())
            b = float(self.b_edit.text())
        except:
            self.statusBar().showMessage('Tüm değerleri sayı formatında girdiğinizden emin olunuz !')
            return

        self.statusBar().clearMessage()
        result = calculate_nth_term(a, b, x0, n)
        self.result_label.setStyleSheet("font-size: 19px;")
        self.result_label.setText(f"<p style='font-size: 19px'>x<sub>{n}</sub> değeri: {result}</p>")
        self.result_label.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
