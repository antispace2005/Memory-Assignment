from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Tuple

from PyQt6 import uic
from PyQt6.QtCore import Qt, QRectF, QSize
from PyQt6.QtGui import QAction, QColor, QFont, QPainter, QPen, QBrush
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QTableWidgetItem


class AllocationMethod(str, Enum):
    FIRST_FIT = "First-Fit"
    BEST_FIT = "Best-Fit"


@dataclass
class Hole:
    start: int
    size: int


@dataclass
class Segment:
    name: str
    size: int
    start: Optional[int] = None


@dataclass
class Process:
    name: str
    segments: List[Segment]
    allocated: bool = False


class MemoryManager:
    def __init__(self, total_size: int, holes: List[Hole]):
        self.total_size = total_size
        self.holes = sorted(holes, key=lambda hole: hole.start)

    def allocate_process(self, process: Process, method: AllocationMethod) -> bool:
        working_holes = [Hole(hole.start, hole.size) for hole in self.holes]
        assigned: List[Segment] = []

        for segment in process.segments:
            hole_index = self._find_hole_index(working_holes, segment.size, method)
            if hole_index is None:
                for assigned_segment in assigned:
                    assigned_segment.start = None
                process.allocated = False
                return False

            hole = working_holes[hole_index]
            segment.start = hole.start
            assigned.append(segment)
            hole.start += segment.size
            hole.size -= segment.size
            if hole.size == 0:
                working_holes.pop(hole_index)

        self.holes = sorted(working_holes, key=lambda hole: hole.start)
        process.allocated = True
        return True

    def deallocate_process(self, process: Process) -> bool:
        if not process.allocated:
            return False

        for segment in process.segments:
            if segment.start is not None:
                self.holes.append(Hole(segment.start, segment.size))
            segment.start = None

        self.holes.sort(key=lambda hole: hole.start)
        merged: List[Hole] = []
        for hole in self.holes:
            if merged and merged[-1].start + merged[-1].size == hole.start:
                merged[-1].size += hole.size
            else:
                merged.append(Hole(hole.start, hole.size))
        self.holes = merged
        process.allocated = False
        return True

    def build_layout(self, processes: List[Process]) -> List[Tuple[int, int, str]]:
        partitions: List[Tuple[int, int, str]] = []
        for process in processes:
            for segment in process.segments:
                if segment.start is not None:
                    partitions.append((segment.start, segment.start + segment.size - 1, f"{process.name}:{segment.name}"))

        for hole in self.holes:
            partitions.append((hole.start, hole.start + hole.size - 1, "Hole"))

        partitions.sort(key=lambda item: item[0])
        layout: List[Tuple[int, int, str]] = []
        cursor = 0
        for start, end, label in partitions:
            if cursor < start:
                layout.append((cursor, start - 1, "Reserved"))
            layout.append((start, end, label))
            cursor = end + 1
        if cursor < self.total_size:
            layout.append((cursor, self.total_size - 1, "Reserved"))
        return layout

    @staticmethod
    def _find_hole_index(holes: List[Hole], size: int, method: AllocationMethod) -> Optional[int]:
        if method == AllocationMethod.FIRST_FIT:
            for index, hole in enumerate(holes):
                if hole.size >= size:
                    return index
            return None

        best_index: Optional[int] = None
        best_waste: Optional[int] = None
        for index, hole in enumerate(holes):
            if hole.size >= size:
                waste = hole.size - size
                if best_waste is None or waste < best_waste:
                    best_index = index
                    best_waste = waste
        return best_index


def sample_scenario() -> Tuple[int, List[Hole], List[Process]]:
    total = 1000
    holes = [Hole(0, 300), Hole(400, 250), Hole(700, 200)]
    processes = [
        Process("P1", [Segment("Code", 100), Segment("Data", 120), Segment("Stack", 90)]),
        Process("P2", [Segment("Code", 200), Segment("Data", 40)]),
        Process("P3", [Segment("Code", 120), Segment("Data", 50)]),
        Process("P4", [Segment("Code", 230), Segment("Data", 40)]),
    ]
    return total, holes, processes


class MemoryCanvas(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._total_size = 1
        self._layout: List[Tuple[int, int, str]] = []

    def set_layout(self, total_size: int, layout: List[Tuple[int, int, str]]) -> None:
        self._total_size = max(1, total_size)
        self._layout = layout
        self.update()

    def sizeHint(self) -> QSize:
        return QSize(900, 180)

    def paintEvent(self, event) -> None:  # noqa: N802
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.fillRect(self.rect(), QColor("#0f172a"))

        if not self._layout:
            painter.setPen(QColor("#cbd5e1"))
            painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "Load a scenario to view memory layout")
            return

        margin = 18
        bar_rect = self.rect().adjusted(margin, 40, -margin, -40)
        x = float(bar_rect.x())
        width = float(bar_rect.width())
        height = float(bar_rect.height())

        painter.setPen(QPen(QColor("#334155"), 2))
        painter.setBrush(QBrush(QColor("#111827")))
        painter.drawRoundedRect(bar_rect, 12, 12)

        for start, end, label in self._layout:
            segment_width = max(1.0, width * ((end - start + 1) / self._total_size))
            rect = QRectF(x, bar_rect.y(), segment_width, height)
            painter.setPen(QPen(QColor("#0f172a"), 1))
            painter.setBrush(QBrush(self._color_for_label(label)))
            painter.drawRoundedRect(rect, 8, 8)
            painter.setPen(QColor("#f8fafc"))
            painter.setFont(QFont("Sans Serif", 9, QFont.Weight.Bold))
            painter.drawText(rect.adjusted(8, 8, -8, -8), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop, label)
            painter.setFont(QFont("Sans Serif", 8))
            painter.drawText(rect.adjusted(8, 8, -8, -8), Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom, f"{start}-{end}")
            x += segment_width

        painter.setPen(QColor("#94a3b8"))
        painter.drawText(margin, 24, f"Total memory: {self._total_size} K")

    @staticmethod
    def _color_for_label(label: str) -> QColor:
        if label == "Hole":
            return QColor("#334155")
        if label == "Reserved":
            return QColor("#111827")
        digest = sum(ord(char) for char in label)
        return QColor.fromHsv(digest % 360, 130, 210)


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setObjectName("mainWindow")
        self.total_size = 1000
        self.processes: List[Process] = []
        self.manager: Optional[MemoryManager] = None
        self.current_method = AllocationMethod.FIRST_FIT

        ui_path = Path(__file__).with_name("main_window.ui")
        uic.loadUi(str(ui_path), self)

        self.memory_canvas = MemoryCanvas()
        self.memory_canvas.setObjectName("memoryCanvas")
        self.canvasHost.layout().addWidget(self.memory_canvas)

        self.methodCombo.addItems([method.value for method in AllocationMethod])
        self.methodCombo.setCurrentText(AllocationMethod.FIRST_FIT.value)

        self._bind_widgets()
        self._build_toolbar()
        self._apply_stylesheet()
        self.load_sample(initial=True)

    def _bind_widgets(self) -> None:
        self.methodCombo.currentTextChanged.connect(self.on_method_changed)
        self.totalSpin.valueChanged.connect(self.on_total_changed)
        self.loadButton.clicked.connect(self.load_sample)
        self.allocateButton.clicked.connect(self.allocate_next)
        self.deallocateButton.clicked.connect(self.deallocate_selected)
        self.runButton.clicked.connect(self.run_full_scenario)

    def _build_toolbar(self) -> None:
        toolbar = self.addToolBar("Main")
        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_view)
        toolbar.addAction(refresh_action)

    def _apply_stylesheet(self) -> None:
        style_path = Path(__file__).with_name("styles.qss")
        if style_path.exists():
            with style_path.open("r", encoding="utf-8") as handle:
                self.setStyleSheet(handle.read())

    def append_log(self, text: str) -> None:
        self.activityLog.append(text)
        self.statusLabel.setText(text)

    def on_method_changed(self, text: str) -> None:
        self.current_method = AllocationMethod(text)
        self.append_log(f"Method set to {text}")

    def on_total_changed(self, value: int) -> None:
        self.total_size = value
        if self.manager is not None:
            self.manager.total_size = value
        self.refresh_view()

    def load_sample(self, initial: bool = False) -> None:
        total, holes, processes = sample_scenario()
        self.total_size = total
        self.totalSpin.blockSignals(True)
        self.totalSpin.setValue(total)
        self.totalSpin.blockSignals(False)
        self.manager = MemoryManager(total, holes)
        self.processes = processes
        self.processPicker.clear()
        self.processPicker.addItems([process.name for process in self.processes])
        self.activityLog.clear()
        if initial:
            self.statusLabel.setText("Sample scenario loaded and ready")
        else:
            self.append_log("Loaded sample testcase from testcases.txt")
        self.refresh_view()

    def allocate_next(self) -> None:
        if self.manager is None:
            return

        pending = next((process for process in self.processes if not process.allocated), None)
        if pending is None:
            self.append_log("No pending processes to allocate")
            return

        if self.manager.allocate_process(pending, self.current_method):
            self.append_log(f"Allocated {pending.name} using {self.current_method.value}")
        else:
            self.append_log(f"Process {pending.name} does not fit")
        self.refresh_view()

    def deallocate_selected(self) -> None:
        if self.manager is None:
            return

        process_name = self.processPicker.currentText()
        process = next((item for item in self.processes if item.name == process_name), None)
        if process is None:
            return

        if self.manager.deallocate_process(process):
            self.append_log(f"Deallocated {process.name}")
        else:
            self.append_log(f"{process.name} is already free")
        self.refresh_view()

    def run_full_scenario(self) -> None:
        self.load_sample()
        if self.manager is None:
            return

        self.append_log(f"Running demo using {self.current_method.value}")
        steps = [
            ("allocate", "P1"),
            ("allocate", "P2"),
            ("allocate", "P3"),
            ("deallocate", "P1"),
            ("allocate", "P4"),
        ]
        for action, process_name in steps:
            process = next(item for item in self.processes if item.name == process_name)
            if action == "allocate":
                if self.manager.allocate_process(process, self.current_method):
                    self.append_log(f"Allocated {process.name}")
                else:
                    self.append_log(f"Process {process.name} does not fit")
            else:
                self.manager.deallocate_process(process)
                self.append_log(f"Deallocated {process.name}")
            self.refresh_view()

    def refresh_view(self) -> None:
        if self.manager is None:
            return

        layout = self.manager.build_layout(self.processes)
        self.memory_canvas.set_layout(self.manager.total_size, layout)
        self._refresh_hole_table()
        self._refresh_segment_table()

    def _refresh_hole_table(self) -> None:
        assert self.manager is not None
        self.holesTable.setRowCount(len(self.manager.holes))
        for row, hole in enumerate(self.manager.holes):
            self.holesTable.setItem(row, 0, QTableWidgetItem(str(hole.start)))
            self.holesTable.setItem(row, 1, QTableWidgetItem(str(hole.size)))
        self.holesTable.resizeColumnsToContents()

    def _refresh_segment_table(self) -> None:
        rows: List[Tuple[str, str, int, str, str]] = []
        for process in self.processes:
            for segment in process.segments:
                rows.append(
                    (
                        process.name,
                        segment.name,
                        segment.size,
                        "-" if segment.start is None else str(segment.start),
                        "Allocated" if process.allocated and segment.start is not None else "Free",
                    )
                )

        self.segmentsTable.setRowCount(len(rows))
        for row, (process_name, segment_name, size, start, status) in enumerate(rows):
            self.segmentsTable.setItem(row, 0, QTableWidgetItem(process_name))
            self.segmentsTable.setItem(row, 1, QTableWidgetItem(segment_name))
            self.segmentsTable.setItem(row, 2, QTableWidgetItem(str(size)))
            self.segmentsTable.setItem(row, 3, QTableWidgetItem(start))
            self.segmentsTable.setItem(row, 4, QTableWidgetItem(status))
        self.segmentsTable.resizeColumnsToContents()


def main() -> None:
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()


if __name__ == "__main__":
    main()