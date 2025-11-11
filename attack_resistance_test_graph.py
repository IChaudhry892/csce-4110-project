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

        # DES sample line (you can update these values as needed)
        # des_y = [0.398, 0.397, 0.396, 0.395, 0.394, 0.393, 0.392]

        # AES line + marked points
        aes_points_x = [5, 15, 25, 35, 45]
        aes_points_y = [0.397293, 0.393768, 0.392728, 0.392346, 0.391747]

        # For a smooth line: match x axis positions
        aes_y_full = [None, 0.397293, 0.393768, 0.392728, 0.392346, 0.391747, None]

        # Plot DES (blue)
        # ax.plot(x, des_y, label="DES")

        # Plot AES (red line + red dots)
        ax.plot(x, aes_y_full, "r-", label="AES")
        ax.scatter(aes_points_x, aes_points_y, color="red")

        # Set axis labels
        ax.set_xlabel("Data Size in MB")
        ax.set_ylabel("Decryption Integrity %")

        # Set custom ticks
        ax.set_xticks(x)
        ax.set_yticks([0.390 + i * 0.001 for i in range(11)])

        # Add legend
        ax.legend()

        # Redraw
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LineGraph()
    window.show()
    sys.exit(app.exec_())
