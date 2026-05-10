import os
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from app import MainWindow, AllocationMethod

def capture_for_method(window, method, folder):
    os.makedirs(f"screenshots/{folder}", exist_ok=True)
    window.methodCombo.setCurrentText(method.value)
    window.load_sample(initial=True)
    QApplication.processEvents()
    window.grab().save(f"screenshots/{folder}/initial.png")

    steps = [
        ("allocate", "P1", "p1_allocated.png"),
        ("allocate", "P2", "p2_allocated.png"),
        ("allocate", "P3", "p3_attempted.png"),
        ("deallocate", "P1", "p1_deallocated.png"),
        ("allocate", "P4", "p4_allocated.png"),
    ]

    for action, process_name, filename in steps:
        process = next(item for item in window.processes if item.name == process_name)
        if action == "allocate":
            window.manager.allocate_process(process, window.current_method)
        else:
            window.manager.deallocate_process(process)
        window.refresh_view()
        QApplication.processEvents()
        window.grab().save(f"screenshots/{folder}/{filename}")

def run_captures():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    QApplication.processEvents()

    capture_for_method(window, AllocationMethod.FIRST_FIT, "firstfit")
    capture_for_method(window, AllocationMethod.BEST_FIT, "bestfit")

    print("Screenshots captured successfully.")
    sys.exit(0)

if __name__ == "__main__":
    run_captures()
