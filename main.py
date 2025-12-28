import sys
import time
import serial
import numpy as np
import pyqtgraph as pg
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtCore import QThread, Signal
from rplidar import RPLidar, RPLidarException


LIDAR_PORT = "/dev/ttyUSB0"
ESP32_PORT = "/dev/ttyUSB1"

MAX_DISTANCE = 4000
SAFE_DISTANCE = 650
SIDE_THRESHOLD = 400
POINTS_PER_UPDATE = 1000


class LidarWorker(QThread):
    new_data = Signal(list)

    def __init__(self, port):
        super().__init__()
        self.lidar = RPLidar(port)
        self.running = True

    def run(self):
        try:
            for scan in self.lidar.iter_scans():
                if not self.running:
                    break
                self.new_data.emit(scan[:POINTS_PER_UPDATE])
        except RPLidarException:
            pass

    def stop(self):
        self.running = False
        try:
            self.lidar.stop()
            self.lidar.stop_motor()
            self.lidar.disconnect()
        except:
            pass
        self.quit()
        self.wait()


class LidarVisualizer(QWidget):
    def __init__(self):
        super().__init__()
        self.last_command = None
        self.esp_serial = None

        self.init_ui()

        try:
            self.esp_serial = serial.Serial(ESP32_PORT, 115200, timeout=1)
        except:
            self.esp_serial = None

        self.lidar_worker = LidarWorker(LIDAR_PORT)
        self.lidar_worker.new_data.connect(self.update_plot)
        self.lidar_worker.start()

    def init_ui(self):
        self.setWindowTitle("Autonomous Robot Navigation")
        self.setGeometry(100, 100, 600, 600)

        self.plot = pg.PlotWidget()
        self.plot.setAspectLocked(True)
        self.plot.setXRange(-MAX_DISTANCE, MAX_DISTANCE)
        self.plot.setYRange(-MAX_DISTANCE, MAX_DISTANCE)
        self.plot.showGrid(x=True, y=True)

        self.scatter = pg.ScatterPlotItem(
            size=3, pen=None, brush=pg.mkBrush(0, 255, 0, 150)
        )
        self.plot.addItem(self.scatter)

        self.arrow = pg.ArrowItem(
            angle=180, headLen=40, tailLen=20, tailWidth=8, brush="r", pen="r"
        )
        self.plot.addItem(self.arrow)

        layout = QVBoxLayout()
        layout.addWidget(self.plot)
        self.setLayout(layout)

    def update_plot(self, scan):
        points = []
        front = False
        left = False
        right = False

        for _, angle, distance in scan:
            if 0 < distance < MAX_DISTANCE:
                rad = np.radians(angle)
                x = distance * np.cos(rad)
                y = distance * np.sin(rad)
                points.append((x, y))

                if (angle <= 10 or angle >= 350) and distance < SAFE_DISTANCE:
                    front = True
                elif 80 <= angle <= 100 and distance < SIDE_THRESHOLD:
                    left = True
                elif 260 <= angle <= 280 and distance < SIDE_THRESHOLD:
                    right = True

        if points:
            xs, ys = zip(*points)
            self.scatter.setData(xs, ys)

        self.arrow.setPos(0, 0)
        self.control_logic(front, left, right)

    def control_logic(self, front, left, right):
        if not self.esp_serial:
            return

        if front:
            if left and right:
                self.send_command("b")
                time.sleep(0.5)
                self.send_command("s")
                time.sleep(0.2)
                self.send_command("r")
            elif left:
                self.send_command("r")
            elif right:
                self.send_command("l")
            else:
                self.send_command("s")
        else:
            self.send_command("f")

    def send_command(self, cmd):
        if cmd == self.last_command:
            return
        try:
            self.esp_serial.write(f"{cmd}\n".encode())
            self.last_command = cmd
        except:
            pass

    def closeEvent(self, event):
        self.lidar_worker.stop()
        if self.esp_serial:
            self.esp_serial.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LidarVisualizer()
    window.show()
    sys.exit(app.exec())
