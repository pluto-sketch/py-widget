# py-widget

**A sleek little system stats widget dashboard written in Python with PyQt5.**
Because who doesn’t want a stylish little floating dashboard showing CPU, RAM, battery, and clickable icons to launch stuff — without dealing with clunky system monitors?

---

## Features

* Floating, frameless, always-on-top transparent window
* Displays real-time CPU %, RAM %, battery %, and placeholders for other stats
* Clickable icons that run any command you want (launch apps, scripts, whatever)
* Customizable grid layout via JSON config
* Styled with a slick glassy transparent theme and subtle shadows
* Written in Python with performance boost using Cython for system stats
* Drag the dashboard anywhere on your screen — because flexibility > stuck in the corner

---

## Screenshots

*placeholder*

---

## Requirements

* Python 3.7+
* PyQt5
* psutil
* Cython (for compiling `system_stats.pyx`)

---

## Installation

1. Clone this repo or download the files.

2. Install dependencies:

   ```bash
   pip install pyqt5 psutil cython pyinstaller
   ```

3. Compile the Cython module for system stats:

   ```bash
   cythonize -i system_stats.pyx
   ```
4. Compile the python app with pyinstaller

    ```bash
    pyinstaller --onefile --windowed main.py
    ```

5. Edit `widgets_config.json` to customize your widgets (icons, commands, labels).

6. Place your theme file (`glass.qs`) in the appropriate path or adjust path in code.

---

## Usage

Run the main dashboard app:

```bash
python main.py
```

The dashboard will pop up on your screen, showing widgets as defined in your JSON config. Click icons to run their commands. Drag to move around.

---

## Configuring Widgets

Widgets are defined in `widgets_config.json` with these keys:

* `type`: `"icon"` or `"label"`
* `icon_path`: Path to the icon image (for icon widgets)
* `command`: Shell command to run on click (icon widgets only)
* `tooltip`: Hover text (optional)
* `text`: Label text (for label widgets)
* `size`: Tuple with `(width, height)` in pixels

Example:

```json
[
  {
    "type": "icon",
    "icon_path": "icons/firefox.png",
    "command": "firefox",
    "tooltip": "Launch Firefox",
    "size": [80, 80]
  },
  {
    "type": "label",
    "text": "CPU Usage",
    "size": [120, 40]
  }
]
```

---

## Code Highlights

* `ClickableIconWidget`: Icon buttons with drop shadow and click-to-run-command support
* `WidgetDashboard`: Loads config, creates widgets, updates system stats every second
* Uses `psutil` + Cython-accelerated `system_stats.pyx` for efficient stats gathering
* Custom glassy theme with Qt Stylesheet (`glass.qs`) for that sleek translucent look

---

## Troubleshooting

* If icons don’t show up, check your icon paths in the config.
* If commands don’t run, ensure they’re valid shell commands available on your system.
* Permission issues on battery stats? Probably no battery or missing permissions — no worries, it’ll just show “N/A.”
* Make sure you run the Cython compile step, or stats won’t update properly.

---

## License

MIT License

---
