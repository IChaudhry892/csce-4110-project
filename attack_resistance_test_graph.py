import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class LineGraph(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle("DES vs AES Decryption Integrity")
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create matplotlib figure
        fig = Figure(figsize=(6, 4))
        self.canvas = FigureCanvas(fig)
        layout.addWidget(self.canvas)

        # Plotting area
        ax = fig.add_subplot(111)

        # X values
        x = [0, 5, 15, 25, 35, 45, 50]

        # DES line + marked points
        des_points_x = [5, 15, 25, 35, 45]
        des_points_y = [0.078921, 0.078286, 0.078136, 0.077720, 0.0778332]

        # AES line + marked points
        aes_points_x = [5, 15, 25, 35, 45]
        aes_points_y = [0.397293, 0.393768, 0.392728, 0.392346, 0.391747]

        # For a smooth line: match x axis positions
        aes_y_full = [None, 0.397293, 0.393768, 0.392728, 0.392346, 0.391747, None]
        des_y_full = [None, 0.078921, 0.078286, 0.078136, 0.077720, 0.0778332, None]

        # Plot DES (blue)
        # ax.plot(x, des_y_full, "b-", label="DES")
        # ax.scatter(des_points_x, des_points_y, color="blue")

        # Plot AES (red line + red dots)
        ax.plot(x, aes_y_full, "r-", label="AES")
        ax.scatter(aes_points_x, aes_points_y, color="red")

        # Set axis labels
        ax.set_xlabel("Data Size in MB")
        ax.set_ylabel("Decryption Integrity %")

        # Set custom ticks
        ax.set_xticks(x)
        ax.set_yticks([0.390 + i * 0.001 for i in range(11)])
        # ax.set_yticks([0.0776, 0.0778, 0.0780, 0.0782, 0.0784, 0.0786, 0.0788, 0.0790])

        # Add legend
        ax.legend()
        
        fig.tight_layout()

        # Redraw
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LineGraph()
    window.show()
    sys.exit(app.exec_())
