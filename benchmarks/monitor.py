#!/usr/bin/env python3
"""
benchmarks/monitor.py
Giám sát tài nguyên CPU/RAM/Disk I/O bằng psutil.
Chạy trong background thread trong khi benchmark thực thi.
"""

import threading
import time
import psutil


class ResourceMonitor:
    """
    Khởi động sampling loop trong thread riêng.
    Gọi .start() trước benchmark, .stop() sau — trả về dict thống kê.
    """

    def __init__(self, interval: float = 0.5):
        self.interval = interval
        self._samples: list[dict] = []
        self._stop_event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        # Baseline disk counters
        self._disk_start = psutil.disk_io_counters()

    def _run(self):
        while not self._stop_event.is_set():
            mem = psutil.virtual_memory()
            self._samples.append({
                "cpu_pct":  psutil.cpu_percent(interval=None),
                "ram_mb":   mem.used / 1024 / 1024,
                "ram_pct":  mem.percent,
            })
            time.sleep(self.interval)

    def start(self):
        psutil.cpu_percent(interval=None)   # prime the first call
        self._disk_start = psutil.disk_io_counters()
        self._thread.start()
        return self

    def stop(self) -> dict:
        self._stop_event.set()
        self._thread.join(timeout=2)

        disk_end = psutil.disk_io_counters()
        disk_read_mb  = (disk_end.read_bytes  - self._disk_start.read_bytes)  / 1024 / 1024
        disk_write_mb = (disk_end.write_bytes - self._disk_start.write_bytes) / 1024 / 1024

        if not self._samples:
            return {}

        cpu_vals = [s["cpu_pct"] for s in self._samples]
        ram_vals = [s["ram_mb"]  for s in self._samples]

        return {
            "cpu_mean_pct":   round(sum(cpu_vals) / len(cpu_vals), 2),
            "cpu_max_pct":    round(max(cpu_vals), 2),
            "ram_mean_mb":    round(sum(ram_vals) / len(ram_vals), 1),
            "ram_max_mb":     round(max(ram_vals), 1),
            "disk_read_mb":   round(disk_read_mb, 2),
            "disk_write_mb":  round(disk_write_mb, 2),
            "samples":        len(self._samples),
        }
