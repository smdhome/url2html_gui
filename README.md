# URL → HTML Converter GUI

A Windows desktop application that converts Windows Internet Shortcut (`.url`) files
into portable `.html` redirect files, so bookmarks stored as `.url` shortcuts can be
opened in any browser on any platform.

This project is a graphical front-end for
[url2html2.py](https://github.com/smdhome/url2html) by Shawn Downey.

---

## Features

- **Dark-themed graphical interface** with a scrollable, colour-coded output log
- **3-D toolbar buttons** – Detect URLs · Settings · Exit
- **Multi-directory support** – scan as many directory trees as you like in one pass
- **Fully automatic workflow** – one button press scans all directories, then asks once whether to convert and once whether to delete the source `.url` files
- **Non-blocking** – all file operations run on a background thread; the UI stays responsive
- **Persistent settings** – your directory list is saved to `url2html_gui.cfg` and reloaded on next launch
- **Embedded icon** – no external asset files needed to run the script
- **Stand-alone `.exe`** build via PyInstaller (no Python installation required on the target PC)

---

## Requirements

| Component | Version |
|-----------|---------|
| Python | 3.8 or newer |
| tkinter | included with standard Python on Windows |
| Pillow | only needed to *regenerate* the icon (`make_icon.py`) |
| PyInstaller | only needed to build the `.exe` |

---

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/smdhome/url2html.git
cd url2html

# 2. Run the GUI (no extra packages required)
python url2html_gui.py
```

---

## Workflow

### Step 1 – Configure directories

Click **⚙ Settings** to open the directory editor.

- Enter one full directory path per line, e.g. `G:\TV` or `C:\Users\you\Bookmarks`
- Use **📂 Browse…** to pick a folder visually
- Click **💾 Save** (or press the Save button at the top of the dialog) when done
- Click **✖ Cancel** to discard changes

Settings are saved automatically to `url2html_gui.cfg` so you don't have to re-enter them next time.

### Step 2 – Detect URLs

Click **🔍 Detect URLs**. The program scans **all** configured directories one after another without any prompting. For each directory it reports the number of `.url` and `.html` files found in the output log.

### Step 3 – Convert (one prompt)

After all directories have been scanned, a single dialog summarises the findings:

> *Found 312 .url file(s) across 3 directories:*
> ```
>    42  .url   G:\TV
>   187  .url   G:\Movies
>    83  .url   G:\Music
> ```
> *Convert them all to .html redirect files now?*

- **Yes** – an `.html` redirect file is created alongside every `.url` file in every directory tree. Then the cleanup prompt is shown automatically.
- **No** – conversion is skipped and a final summary is displayed.

### Step 4 – Cleanup (one prompt)

After conversion, a single dialog asks whether to delete the original `.url` files:

> *Permanently delete ALL .url files under:*
> ```
>   G:\TV
>   G:\Movies
>   G:\Music
> ```
> *This cannot be undone. Continue?*

- **Yes** – all `.url` files are deleted from every converted directory tree.
- **No** – the `.url` files are left in place.

### Step 5 – Summary

A completion popup shows the number of `.html` files created **on this run**. The output log lists every file that was created.

---

## What the generated HTML looks like

```html
<html><head>
<meta http-equiv="refresh" content="0; url=https://example.com/">
<title>Redirect</title>
</head><body>
<p>Redirecting to <a href="https://example.com/">https://example.com/</a></p>
</body></html>
```

The browser opens the target URL immediately via the `meta refresh` tag, making the `.html` file a drop-in replacement for the `.url` shortcut on any operating system.

---

## Building a Stand-Alone Executable

### Step 1 – Generate the icon (optional – already embedded in the script)

```bash
pip install pillow
python make_icon.py
# Produces: url2html_gui.ico  and  url2html_gui_256.png
```

### Step 2 – Install PyInstaller

```bash
pip install pyinstaller
```

### Step 3 – Build

```bash
pyinstaller --onefile --windowed --icon=url2html_gui.ico url2html_gui.py
```

The finished executable is written to `dist\url2html_gui.exe`. Copy it anywhere — no Python installation is required on the target machine.

| PyInstaller flag | Purpose |
|-----------------|---------|
| `--onefile` | Bundle everything into a single `.exe` |
| `--windowed` | Suppress the console window (GUI-only app) |
| `--icon=…` | Embed the `.ico` as the Windows taskbar / Explorer icon |

---

## File Reference

| File | Purpose |
|------|---------|
| `url2html_gui.py` | Main graphical application *(run this directly or build into an `.exe`)* |
| `make_icon.py` | Regenerates `url2html_gui.ico` from scratch using Pillow |
| `url2html_gui.cfg` | Auto-created config file that stores your directory list |
| `url2html2.py` | Original command-line script (reference / historical) |

---

## Configuration File

`url2html_gui.cfg` is created automatically next to the script (or `.exe`) the first time you save from the Settings dialog. It uses standard INI format:

```ini
[main]
directories = G:\TV|G:\MOVIES|C:\Users\you\Bookmarks
```

Directory paths are separated by `|`. You can edit this file by hand if needed.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Directory not found" in log | Check the path in Settings; make sure the drive is connected and the path is typed correctly |
| No `.url` files found | The directory may already have been converted, or the path is wrong |
| `.html` file not created | Check the log for `[ERROR]` lines; you may lack write permission on that folder |
| Emoji show as boxes | Install a font that supports Unicode emoji (e.g. Segoe UI Emoji, included in Windows 10/11) |
| `.exe` triggers antivirus | PyInstaller one-file bundles are sometimes flagged as suspicious; add a folder exclusion in your AV settings, or use `--onedir` to produce a folder-based build instead |

---

## License

Original `url2html2.py` Copyright © Shawn Downey, 2016.  
GUI front-end (`url2html_gui.py`) Copyright © Shawn Downey, 2025.  
Released under the MIT License – see [LICENSE](LICENSE) for details.

---

## Contributing

Pull requests are welcome. Please open an issue first to discuss any significant change.
