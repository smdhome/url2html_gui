# URL → HTML Converter GUI

A Windows desktop application that converts Windows Internet Shortcut (`.url`) files
into portable `.html` redirect files, so bookmarks stored as `.url` shortcuts can be
opened in any browser on any platform.

This project is a graphical front-end for
[url2html2.py](https://github.com/smdhome/url2html) by Shawn Downey.

---

## Download

Pre-built Windows executables are available on the
[Releases](../../releases) page — no Python installation required.

---

## Features

- **Dark-themed graphical interface** with a scrollable, colour-coded output log
- **3-D toolbar buttons** – Detect URLs · Settings · Exit
- **Multi-directory support** – scan as many directory trees as you like in one pass
- **Fully automatic workflow** – one button press scans all directories, then asks once
  whether to convert and once whether to delete the source `.url` files
- **Non-blocking** – all file operations run on a background thread; the UI stays responsive
- **Persistent settings** – your directory list is saved to `url2html_gui.cfg` and
  reloaded on next launch
- **Embedded icon** – no external asset files needed at runtime
- **Stand-alone `.exe`** – built with PyInstaller; runs on any Windows PC

---

## Requirements (running from source)

| Component | Version |
|-----------|---------|
| Python | 3.8 or newer |
| tkinter | included with standard Python on Windows |
| Pillow | only needed to regenerate the icon (`make_icon.py`) |
| PyInstaller | only needed to build the `.exe` |

---

## Quick Start (running from source)

```bat
:: 1. Clone the repository
git clone https://github.com/smdhome/url2html.git
cd url2html

:: 2. Run the GUI directly (no extra packages required)
python url2html_gui.py
```

---

## Workflow

### Step 1 – Configure directories

Click **⚙ Settings** to open the directory editor.

- Enter one full directory path per line, e.g. `G:\TV` or `C:\Users\you\Bookmarks`
- Use **📂 Browse…** to pick a folder visually
- Click **💾 Save** at the top of the dialog when done
- Click **✖ Cancel** to discard changes

Settings are saved to `url2html_gui.cfg` so you don't need to re-enter them next time.

### Step 2 – Detect URLs

Click **🔍 Detect URLs**. The program scans **all** configured directories
sequentially without any further prompting, logging counts to the output pane as it goes.

### Step 3 – Convert (one prompt)

After scanning, a single dialog summarises every directory that contains `.url` files:

> *Found 312 .url file(s) across 3 directories:*
> ```
>    42  .url   G:\TV
>   187  .url   G:\Movies
>    83  .url   G:\Music
> ```
> *Convert them all to .html redirect files now?*

- **Yes** – an `.html` redirect file is created alongside every `.url` file in every
  directory tree. The cleanup prompt then appears automatically.
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

- **Yes** – all `.url` files are deleted across every converted directory tree.
- **No** – the `.url` files are left in place.

### Step 5 – Summary

A completion popup reports the number of `.html` files created **on this run**.
The output log lists every file that was created.

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

The browser opens the target URL immediately via the `meta refresh` tag, making the
`.html` file a drop-in replacement for the `.url` shortcut on any operating system.

---

## Building the Executable

### Using the build script (recommended)

A `build.bat` script is provided that handles everything automatically:
installing dependencies, regenerating the icon, cleaning old build artefacts,
and running PyInstaller with the `--windowed` flag so no black console window appears.

> **Note:** `make_icon.py` assembles the `.ico` file manually from PNG byte buffers
> rather than using Pillow's built-in ICO encoder, which is known to hang on Windows
> when called from a batch script or IDLE due to internal GDI calls. The manual
> assembler produces an identical, fully valid ICO file with no risk of stalling.

```bat
:: From the project directory:
build.bat

:: Or specify a Python interpreter explicitly:
build.bat C:\Python311\python.exe
```

The script runs four steps:

| Step | Action |
|------|--------|
| 1 | Installs / upgrades `pillow` and `pyinstaller` via pip |
| 2 | Runs `make_icon.py` to regenerate `url2html_gui.ico` |
| 3 | Removes any previous `build\`, `dist\`, and `.spec` artefacts |
| 4 | Runs PyInstaller with the correct flags |

On success the finished executable is written to `dist\url2html_gui.exe`.

### Manual build

If you prefer to run the steps yourself:

```bat
:: Install dependencies
pip install pillow pyinstaller

:: Regenerate the icon (bypasses Pillow's ICO encoder to avoid Windows hangs)
python make_icon.py

:: Build
pyinstaller --onefile --windowed --icon=url2html_gui.ico --name=url2html_gui url2html_gui.py
```

| PyInstaller flag | Purpose |
|-----------------|---------|
| `--onefile` | Bundle everything into a single `.exe` |
| `--windowed` | Suppress the console / black window (GUI-only app) |
| `--icon=…` | Embed the `.ico` as the Windows taskbar / Explorer icon |
| `--name=…` | Set the output filename |
| `--noconfirm` | Overwrite previous output without prompting |
| `--clean` | Remove PyInstaller's cache before building |

---

## Creating a GitHub Release

1. **Build the executable** using `build.bat` (see above).
2. **Tag the release** in git:
   ```bat
   git tag -a v2.0 -m "Release v2.0"
   git push origin v2.0
   ```
3. **Create the release on GitHub:**
   - Go to your repository → **Releases** → **Draft a new release**
   - Select the tag you just pushed
   - Set the release title, e.g. `v2.0 – URL → HTML Converter GUI`
   - Write release notes (see template below)
   - Upload `dist\url2html_gui.exe` as a release asset
   - Click **Publish release**

### Release notes template

```markdown
## What's new in v2.0

- Fully graphical dark-themed interface with colour-coded output log
- Scans all configured directories in a single pass (no per-directory prompts)
- One confirmation to convert all .url files; one confirmation to delete them
- Settings dialog with multi-line path editor and Browse button
- Persistent settings saved to url2html_gui.cfg
- Stand-alone .exe — no Python required on target machine

## Download

Download **url2html_gui.exe** from the Assets section below and run it directly.
No installation required.

## System requirements

- Windows 10 or Windows 11 (64-bit)
- No additional software required
```

---

## File Reference

| File | Purpose |
|------|---------|
| `url2html_gui.py` | Main graphical application *(run directly or build into an `.exe`)* |
| `build.bat` | Build script – installs deps, generates icon, runs PyInstaller |
| `make_icon.py` | Generates `url2html_gui.ico` using Pillow for drawing and a hand-written ICO assembler to avoid Windows GDI hangs |
| `url2html_gui.cfg` | Auto-created at runtime; stores your directory list |
| `url2html2.py` | Original command-line script (reference / historical) |

---

## Configuration File

`url2html_gui.cfg` is created automatically next to the script (or `.exe`) the first
time you save from the Settings dialog. It uses standard INI format:

```ini
[main]
directories = G:\TV|G:\MOVIES|C:\Users\you\Bookmarks
```

Directory paths are separated by `|`. You can edit this file by hand if needed.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Directory not found" in log | Check the path in Settings; make sure the drive is connected |
| No `.url` files found | The directory may already have been converted, or the path is wrong |
| `.html` file not created | Check the log for `[ERROR]` lines; you may lack write permission on that folder |
| Black console window appears | Rebuild using `build.bat` — it includes `--windowed` automatically |
| `make_icon.py` hangs in IDLE or `build.bat` | Ensure you are using the latest `make_icon.py` — it writes the `.ico` file manually without calling Pillow's ICO encoder, which is the source of the hang on Windows |
| Emoji show as boxes | Windows 10 or 11 includes Segoe UI Emoji; older Windows may need a font update |
| `.exe` flagged by antivirus | PyInstaller bundles are sometimes flagged; add a folder exclusion in your AV settings, or use `--onedir` to produce a folder-based build instead |
| `build.bat` says Python not found | Install Python 3.8+ and ensure it is on your PATH, or pass the full path: `build.bat C:\Python311\python.exe` |

---

## License

Original `url2html2.py` Copyright © Shawn Downey, 2016.  
GUI front-end (`url2html_gui.py`) Copyright © Shawn Downey, 2025.  
Released under the MIT License – see [LICENSE](LICENSE) for details.

---

## Contributing

Pull requests are welcome. Please open an issue first to discuss any significant change.
