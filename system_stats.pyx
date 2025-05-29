# system_stats.pyx
import psutil

def get_system_stats():
    cdef float cpu = psutil.cpu_percent()
    cdef float ram = psutil.virtual_memory().percent
    cdef float battery_percent = -1.0

    try:
        battery = psutil.sensors_battery()
        if battery is not None:
            battery_percent = battery.percent
    except Exception:
        # No battery or permission denied or kernel mood swings
        battery_percent = -1.0

    return cpu, ram, battery_percent
