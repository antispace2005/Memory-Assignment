#!/usr/bin/env python
"""Capture screenshots of the memory allocation scenarios."""
from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from app import MainWindow, AllocationMethod


def capture_scenario(method: AllocationMethod) -> None:
    """Run a scenario and capture screenshots at each step."""
    method_name = method.value.replace("-", "").lower()
    output_dir = Path(__file__).parent / "screenshots" / method_name
    output_dir.mkdir(parents=True, exist_ok=True)

    app = QApplication.instance() or QApplication([])
    window = MainWindow()
    window.show()

    steps = [
        ("initial", None),
        ("p1_allocated", ("allocate", "P1")),
        ("p2_allocated", ("allocate", "P2")),
        ("p3_attempted", ("allocate", "P3")),
        ("p1_deallocated", ("deallocate", "P1")),
        ("p4_allocated", ("allocate", "P4")),
    ]

    window.load_sample()
    window.current_method = method
    window.methodCombo.setCurrentText(method.value)

    for step_name, operation in steps:
        if operation:
            action, process_name = operation
            process = next(item for item in window.processes if item.name == process_name)
            if action == "allocate":
                window.manager.allocate_process(process, method)
                window.append_log(f"Allocated {process.name}")
            else:
                window.manager.deallocate_process(process)
                window.append_log(f"Deallocated {process.name}")
            window.refresh_view()

        screenshot = window.grab()
        output_path = output_dir / f"{step_name}.png"
        screenshot.save(str(output_path))
        print(f"Saved: {output_path}")

    window.close()


if __name__ == "__main__":
    for method in (AllocationMethod.FIRST_FIT, AllocationMethod.BEST_FIT):
        print(f"\nCapturing {method.value} scenario...")
        capture_scenario(method)
    print("\nDone! Screenshots saved to the 'screenshots' folder.")
