"""
url2html_gui.py  –  Graphical front-end for converting Windows .url shortcuts
                    into HTML redirect files.

Original command-line logic by Shawn Downey (url2html2.py, 2016).
GUI version 2.0, 2025.

Usage:
    python url2html_gui.py

Build stand-alone .exe (run make_icon.py first to create url2html_gui.ico):
    pyinstaller --onefile --windowed --icon=url2html_gui.ico url2html_gui.py
"""

import os
import base64
import tempfile
import threading
import configparser
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# ── Embedded ICO icon (base64) ────────────────────────────────────────────────
_ICON_B64 = (
    "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"
    "AT7RHqD1agIBAAAAAElFTkSuQmCC"
)

CONFIG_FILE = "url2html_gui.cfg"
APP_TITLE   = "URL \u2192 HTML Converter"
VERSION     = "2.0"

# ── Colour palette ─────────────────────────────────────────────────────────────
BG           = "#1e2430"
# Button backgrounds – mid-tone so disabled text stays readable against them
BTN_DETECT   = "#2e7d32"   # medium green
BTN_MAKE     = "#1565c0"   # medium blue
BTN_CLEANUP  = "#c62828"   # medium red
BTN_SETTINGS = "#6a1b9a"   # medium purple
BTN_EXIT     = "#6d4c41"   # medium brown
# Disabled text – bright enough to read on the mid-tone backgrounds above
BTN_DISABLED_FG = "#b0bec5"
FG           = "#eceff1"
LOG_BG       = "#0d1117"
LOG_FG       = "#c9d1d9"
ACCENT       = "#29b6f6"
HEADER_BG    = "#0d1117"


# ── Core logic (ported from url2html2.py) ─────────────────────────────────────

def _get_url(filepath):
    """Extract the URL= value from a Windows .url shortcut file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                stripped = line.strip()
                if stripped.upper().startswith("URL="):
                    return stripped[4:]
    except OSError:
        pass
    return None


def count_types(directory, ext):
    """Recursively count files with *ext* (case-insensitive) under *directory*."""
    ext_lower = "." + ext.lower().lstrip(".")
    n = 0
    for root, _dirs, files in os.walk(directory):
        for f in files:
            if f.lower().endswith(ext_lower):
                n += 1
    return n


def make_htmls(directory, log_cb):
    """Convert every .url file under *directory* into a .html redirect file.
    *log_cb* is called as log_cb(message, tag).
    Returns list of created file paths."""
    created = []
    for root, _dirs, files in os.walk(directory):
        for f in files:
            if not f.lower().endswith(".url"):
                continue
            src = os.path.join(root, f)
            url = _get_url(src)
            if not url:
                log_cb(f"  [WARN] No URL= found in: {src}", "warn")
                continue
            html = (
                "<html><head>\n"
                f'<meta http-equiv="refresh" content="0; url={url}">\n'
                "<title>Redirect</title>\n"
                "</head><body>\n"
                f'<p>Redirecting to <a href="{url}">{url}</a></p>\n'
                "</body></html>\n"
            )
            base = f[:-4]   # strip ".url"
            dst  = os.path.join(root, base + ".html")
            try:
                with open(dst, "w", encoding="utf-8") as fh:
                    fh.write(html)
                created.append(dst)
                log_cb(f"  Created: {dst}", "ok")
            except OSError as e:
                log_cb(f"  [ERROR] {dst}: {e}", "err")
    return created


def delete_urls(directory, log_cb):
    """Delete all .url files under *directory*. Returns count deleted."""
    n = 0
    for root, _dirs, files in os.walk(directory):
        for f in files:
            if not f.lower().endswith(".url"):
                continue
            fp = os.path.join(root, f)
            try:
                os.remove(fp)
                log_cb(f"  Deleted: {fp}", "dim")
                n += 1
            except OSError as e:
                log_cb(f"  [ERROR] {fp}: {e}", "err")
    return n


# ── Settings dialog ────────────────────────────────────────────────────────────

class SettingsDialog(tk.Toplevel):
    """Modal dialog for editing the list of directories to process."""

    def __init__(self, parent, dirs):
        super().__init__(parent)
        self.title("Settings \u2013 Directory Paths")
        self.configure(bg=BG)
        self.resizable(True, True)
        self.result = None
        self._build(dirs)
        self.transient(parent)
        self.grab_set()
        self.geometry("560x320")
        self.minsize(420, 280)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.update_idletasks()
        px = parent.winfo_x() + (parent.winfo_width()  - self.winfo_width())  // 2
        py = parent.winfo_y() + (parent.winfo_height() - self.winfo_height()) // 2
        self.geometry(f"+{px}+{py}")
        self.wait_window()

    def _build(self, dirs):
        # -- Button row at the TOP -- compact ---------------------------------
        bf = tk.Frame(self, bg=BG)
        bf.pack(fill="x", padx=10, pady=(8, 4))

        def btn(text, color, cmd):
            return tk.Button(bf, text=text, bg=color, fg=FG,
                             activebackground=color, activeforeground=FG,
                             relief="raised", bd=2,
                             font=("Segoe UI", 8, "bold"),
                             cursor="hand2", command=cmd,
                             padx=6, pady=2)

        btn("💾  Save",         BTN_DETECT, self._save  ).pack(side="left",  padx=3)
        btn("📂  Browse…", BTN_MAKE,   self._browse).pack(side="left",  padx=3)
        btn("✖  Cancel",           BTN_EXIT,   self._cancel).pack(side="right", padx=3)

        # -- Label ------------------------------------------------------------
        tk.Label(self, text="Directories to scan  (one path per line):",
                 bg=BG, fg=FG, font=("Segoe UI", 9, "bold")
                 ).pack(padx=10, pady=(0, 2), anchor="w")

        # -- Text area --------------------------------------------------------
        frame = tk.Frame(self, bg=BG)
        frame.pack(fill="both", expand=True, padx=10, pady=(0, 2))

        self._txt = tk.Text(frame, bg=LOG_BG, fg=LOG_FG, insertbackground=FG,
                            font=("Consolas", 10), relief="flat", bd=2,
                            wrap="none", undo=True)
        sby = ttk.Scrollbar(frame, orient="vertical",   command=self._txt.yview)
        sbx = ttk.Scrollbar(frame, orient="horizontal", command=self._txt.xview)
        self._txt.configure(yscrollcommand=sby.set, xscrollcommand=sbx.set)
        sby.pack(side="right",  fill="y")
        sbx.pack(side="bottom", fill="x")
        self._txt.pack(fill="both", expand=True)

        if dirs:
            self._txt.insert("1.0", "\n".join(dirs))

        tk.Label(self,
                 text="Tip: use full paths, e.g.   G:\\TV   or   C:\\Users\\you\\Bookmarks",
                 bg=BG, fg="#78909c", font=("Segoe UI", 8, "italic")
                 ).pack(padx=10, pady=(2, 6), anchor="w")
    def _browse(self):
        d = filedialog.askdirectory(title="Select a directory to add")
        if d:
            cur = self._txt.get("1.0", "end").strip()
            self._txt.insert("end", ("\n" if cur else "") + d)

    def _on_close(self):
        """Called when the user clicks the window X button."""
        answer = messagebox.askyesnocancel(
            "Save Changes?",
            "Save the directory list before closing?")
        if answer is True:
            self._save()
        elif answer is False:
            self._cancel()
        # answer is None → user clicked Cancel on the dialog; do nothing (keep window open)

    def _save(self):
        raw = self._txt.get("1.0", "end").strip()
        self.result = [p.strip() for p in raw.splitlines() if p.strip()]
        self.destroy()

    def _cancel(self):
        self.destroy()


# ── Main application ───────────────────────────────────────────────────────────

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f"{APP_TITLE}  v{VERSION}")
        self.configure(bg=BG)
        self.minsize(700, 500)
        self.geometry("860x580")

        self._dirs        = []
        self._dir_index   = 0
        self._url_count   = 0
        self._html_count  = 0
        self._created_all     = []   # cumulative across all runs
        self._created_this_run = []  # reset each time Detect URLs is pressed
        self._busy        = False

        self._apply_icon()
        self._build_ui()
        self._load_config()
        self._refresh_buttons()

    # ── Icon ──────────────────────────────────────────────────────────────────

    def _apply_icon(self):
        try:
            data = base64.b64decode(_ICON_B64)
            tmp  = tempfile.NamedTemporaryFile(suffix=".ico", delete=False)
            tmp.write(data)
            tmp.close()
            self.iconbitmap(tmp.name)
            self.after(500, lambda p=tmp.name: self._rm(p))
        except Exception:
            pass

    @staticmethod
    def _rm(path):
        try:
            os.remove(path)
        except Exception:
            pass

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        hdr = tk.Frame(self, bg=HEADER_BG, height=46)
        hdr.pack(fill="x")
        hdr.pack_propagate(False)
        tk.Label(hdr, text="  \U0001f517  URL \u2192 HTML Converter",
                 bg=HEADER_BG, fg=ACCENT,
                 font=("Segoe UI", 13, "bold")).pack(side="left",  padx=10, pady=8)
        tk.Label(hdr, text=f"v{VERSION}",
                 bg=HEADER_BG, fg="#546e7a",
                 font=("Segoe UI", 9)).pack(side="right", padx=12)

        # Status bar
        self._sv = tk.StringVar(
            value="Ready.  Open Settings to configure directories, then click Detect URLs.")
        tk.Label(self, textvariable=self._sv,
                 bg="#161b22", fg="#adbac7",
                 font=("Segoe UI", 9), anchor="w", padx=10
                 ).pack(fill="x", side="bottom")

        # Toolbar
        toolbar = tk.Frame(self, bg=BG, pady=10)
        toolbar.pack(fill="x", padx=16)

        def mkbtn(text, color, cmd, width=14):
            b = tk.Button(toolbar, text=text, bg=color, fg=FG,
                          activebackground=color, activeforeground=FG,
                          relief="raised", bd=3,
                          font=("Segoe UI", 10, "bold"),
                          width=width, cursor="hand2", command=cmd,
                          disabledforeground=BTN_DISABLED_FG)
            b.pack(side="left", padx=5, ipady=5)
            return b

        self._btn_detect   = mkbtn("\U0001f50d  Detect URLs",  BTN_DETECT,   self._on_detect)
        self._btn_settings = mkbtn("\u2699  Settings",         BTN_SETTINGS, self._on_settings)
        self._btn_exit     = mkbtn("\u2716  Exit",             BTN_EXIT,     self._on_exit)

        # Progress label
        self._pv = tk.StringVar(value="")
        tk.Label(self, textvariable=self._pv,
                 bg=BG, fg="#78909c",
                 font=("Segoe UI", 9, "italic")).pack(anchor="w", padx=18)

        # Log pane
        lo = tk.Frame(self, bg=BG)
        lo.pack(fill="both", expand=True, padx=16, pady=(2, 6))
        tk.Label(lo, text="Output Log",
                 bg=BG, fg="#546e7a",
                 font=("Segoe UI", 8, "italic")).pack(anchor="w")

        lf = tk.Frame(lo, bg=LOG_BG, bd=2, relief="sunken")
        lf.pack(fill="both", expand=True)

        self._log_txt = tk.Text(lf, bg=LOG_BG, fg=LOG_FG,
                                insertbackground=FG,
                                font=("Consolas", 10),
                                state="disabled", wrap="none", relief="flat",
                                selectbackground="#264f78", selectforeground=FG)
        sby = ttk.Scrollbar(lf, orient="vertical",   command=self._log_txt.yview)
        sbx = ttk.Scrollbar(lf, orient="horizontal", command=self._log_txt.xview)
        self._log_txt.configure(yscrollcommand=sby.set, xscrollcommand=sbx.set)
        sby.pack(side="right",  fill="y")
        sbx.pack(side="bottom", fill="x")
        self._log_txt.pack(fill="both", expand=True)

        self._log_txt.tag_configure("hdr",  foreground=ACCENT,    font=("Consolas", 10, "bold"))
        self._log_txt.tag_configure("ok",   foreground="#4caf50")
        self._log_txt.tag_configure("warn", foreground="#ffa726")
        self._log_txt.tag_configure("err",  foreground="#ef5350")
        self._log_txt.tag_configure("dim",  foreground="#607d8b")

        self._writelog(f"  Welcome to URL \u2192 HTML Converter  v{VERSION}", "hdr")
        self._writelog("  Configure directories in Settings, then click Detect URLs.", "dim")

    # ── Logging ───────────────────────────────────────────────────────────────

    def _writelog(self, msg, tag=""):
        self._log_txt.configure(state="normal")
        self._log_txt.insert("end", msg + "\n", tag)
        self._log_txt.see("end")
        self._log_txt.configure(state="disabled")

    def _log(self, msg, tag=""):
        """Thread-safe log write."""
        self.after(0, self._writelog, msg, tag)

    # ── Config ────────────────────────────────────────────────────────────────

    def _load_config(self):
        cfg = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            cfg.read(CONFIG_FILE, encoding="utf-8")
            raw = cfg.get("main", "directories", fallback="")
            self._dirs = [d.strip() for d in raw.split("|") if d.strip()]
        if self._dirs:
            self._sv.set(
                f"Loaded {len(self._dirs)} directory path(s) from {CONFIG_FILE}.")

    def _save_config(self):
        cfg = configparser.ConfigParser()
        cfg["main"] = {"directories": "|".join(self._dirs)}
        with open(CONFIG_FILE, "w", encoding="utf-8") as fh:
            cfg.write(fh)

    # ── Button state ──────────────────────────────────────────────────────────

    def _setbtn(self, btn, enabled):
        btn.configure(state="normal" if enabled else "disabled")

    def _refresh_buttons(self):
        idle     = not self._busy
        can_det  = idle and bool(self._dirs)

        self._setbtn(self._btn_detect,   can_det)
        self._setbtn(self._btn_settings, idle)
        self._setbtn(self._btn_exit,     True)

        if self._dirs:
            idx = min(self._dir_index, len(self._dirs) - 1)
            self._pv.set(
                f"Directory {idx + 1} of {len(self._dirs)}:  {self._dirs[idx]}")
        else:
            self._pv.set("No directories configured \u2013 open Settings first.")

    # ── Button handlers ───────────────────────────────────────────────────────

    def _on_settings(self):
        dlg = SettingsDialog(self, list(self._dirs))
        if dlg.result is not None:
            self._dirs       = dlg.result
            self._dir_index  = 0
            self._url_count  = 0
            self._html_count = 0
            self._save_config()
            self._writelog("\n\u2500" * 42, "hdr")
            if self._dirs:
                word = "directory" if len(self._dirs) == 1 else "directories"
                self._writelog(
                    f" Settings saved \u2013 {len(self._dirs)} {word} queued.", "hdr")
                for i, d in enumerate(self._dirs, 1):
                    self._writelog(f"   [{i}] {d}", "dim")
                self._sv.set(
                    f"Settings saved. {len(self._dirs)} path(s) queued. Click Detect URLs.")
            else:
                self._writelog(" Settings cleared \u2013 no directories configured.", "warn")
                self._sv.set("No directories configured.")
            self._refresh_buttons()

    # -- Detect (scans ALL directories, then asks once) ----------------------
    def _on_detect(self):
        if not self._dirs:
            messagebox.showwarning("No Directories",
                                   "Configure at least one directory in Settings.")
            return
        # Always restart from the beginning
        self._dir_index       = 0
        self._url_count       = 0
        self._html_count      = 0
        self._created_this_run = []
        self._busy = True
        self._refresh_buttons()

        def work():
            scan_results = []   # list of (directory, n_url, n_html)
            for idx, directory in enumerate(self._dirs):
                self._log(f"\n{'='*44}", "hdr")
                self._log(f" Scan  [{idx+1}/{len(self._dirs)}]  {directory}", "hdr")
                self._log(f"{'='*44}", "hdr")
                if not os.path.isdir(directory):
                    self._log(f"  Directory not found: {directory}", "err")
                    scan_results.append((directory, 0, 0))
                    continue
                self.after(0, self._sv.set, f"Scanning {directory} \u2026")
                self._log("  Counting .url files \u2026", "dim")
                n_url  = count_types(directory, "url")
                self._log("  Counting .html files \u2026", "dim")
                n_html = count_types(directory, "html")
                self._log(f"  Found {n_url:,}  .url  file(s)")
                self._log(f"  Found {n_html:,}  .html file(s)")
                scan_results.append((directory, n_url, n_html))
            self.after(0, self._scan_all_done, scan_results)

        threading.Thread(target=work, daemon=True).start()

    def _scan_all_done(self, scan_results):
        self._busy = False
        self._scan_results = scan_results
        total_url  = sum(r[1] for r in scan_results)
        total_html = sum(r[2] for r in scan_results)

        self._writelog(f"\n{'='*44}", "hdr")
        self._writelog(" Scan Complete", "hdr")
        self._writelog(f"{'='*44}", "hdr")
        self._writelog(f"  Directories scanned : {len(scan_results)}")
        self._writelog(f"  Total .url  files   : {total_url:,}",
                       "ok" if total_url > 0 else "warn")
        self._writelog(f"  Total .html files   : {total_html:,}")

        self._refresh_buttons()

        if total_url > 0:
            lines = []
            for d, nu, nh in scan_results:
                if nu > 0:
                    lines.append(f"  {nu:>5}  .url   {d}")
            breakdown = "\n".join(lines)
            n_dirs_with_urls = sum(1 for r in scan_results if r[1] > 0)
            answer = messagebox.askyesno(
                "URL Files Found",
                f"Found {total_url:,} .url file(s) across "
                f"{n_dirs_with_urls} "
                f"director{'y' if n_dirs_with_urls == 1 else 'ies'}:\n\n"
                f"{breakdown}\n\n"
                "Convert them all to .html redirect files now?",
                icon="question")
            if answer:
                self._sv.set("Converting .url \u2192 .html in all directories \u2026")
                self._on_make_all()
            else:
                self._writelog("  Conversion declined by user.", "warn")
                self._sv.set("Conversion declined.")
                self._finish()
        else:
            if total_html > 0:
                self._writelog(
                    "  No .url files found. Directories may already be converted.", "warn")
            else:
                self._writelog("  No .url or .html files found in any directory.", "warn")
            self._sv.set("No .url files found in any directory.")
            self._finish()

    # -- Make (all directories in one pass) ------------------------------------
    def _on_make_all(self):
        self._busy = True
        self._refresh_buttons()

        def work():
            created_pass = []
            dirs_with_urls = [r[0] for r in self._scan_results if r[1] > 0]
            for idx, directory in enumerate(dirs_with_urls):
                self._log(f"\n{'='*44}", "hdr")
                self._log(
                    f" Make HTMLs  [{idx+1}/{len(dirs_with_urls)}]  {directory}", "hdr")
                self._log(f"{'='*44}", "hdr")
                self.after(0, self._sv.set,
                           f"Converting .url \u2192 .html in {directory} \u2026")
                created = make_htmls(directory, self._log)
                created_pass.extend(created)
                self._log(f"  \u2714 {len(created)} .html file(s) created.", "ok")
            self.after(0, self._make_all_done, created_pass)

        threading.Thread(target=work, daemon=True).start()

    def _make_all_done(self, created):
        self._created_all.extend(created)
        self._created_this_run.extend(created)
        self._busy = False
        self._writelog(f"\n  \u2714 {len(created)} .html file(s) created in total.", "ok")
        self._sv.set(f"Created {len(created)} .html file(s). Prompting for cleanup \u2026")
        self._refresh_buttons()
        dirs_with_urls = [r[0] for r in self._scan_results if r[1] > 0]
        if dirs_with_urls:
            dir_list = "\n".join(f"  {d}" for d in dirs_with_urls)
            confirmed = messagebox.askyesno(
                "Delete .url Files?",
                f"Permanently delete ALL .url files under:\n\n"
                f"{dir_list}\n\n"
                "This cannot be undone. Continue?",
                icon="warning")
            if confirmed:
                self._on_cleanup_all(dirs_with_urls)
                return
            else:
                self._writelog("  Cleanup skipped by user.", "warn")
                self._sv.set("Cleanup skipped.")
        self._finish()

    # -- Cleanup (all directories in one pass) ---------------------------------
    def _on_cleanup_all(self, dirs_with_urls):
        self._busy = True
        self._refresh_buttons()

        def work():
            total_deleted = 0
            for idx, directory in enumerate(dirs_with_urls):
                self._log(f"\n{'='*44}", "hdr")
                self._log(
                    f" Cleanup  [{idx+1}/{len(dirs_with_urls)}]  {directory}", "hdr")
                self._log(f"{'='*44}", "hdr")
                self.after(0, self._sv.set,
                           f"Deleting .url files in {directory} \u2026")
                n = delete_urls(directory, self._log)
                total_deleted += n
                self._log(f"  \u2714 {n} .url file(s) deleted.", "ok")
            self.after(0, self._cleanup_all_done, total_deleted)

        threading.Thread(target=work, daemon=True).start()

    def _cleanup_all_done(self, n_deleted):
        self._busy = False
        self._writelog(f"\n  \u2714 {n_deleted} .url file(s) deleted in total.", "ok")
        self._sv.set(f"Cleanup done \u2013 {n_deleted} .url file(s) removed.")
        self._refresh_buttons()
        self._finish()

    def _finish(self):
        self._print_summary()
        self._sv.set("All directories processed. See summary in the log.")
        n = len(self._dirs)
        messagebox.showinfo(
            "All Done",
            f"All {n} director{'y has' if n == 1 else 'ies have'} been processed.\n\n"
            f"Total .html files created this run: {len(self._created_this_run)}")

    def _print_summary(self):
        self._writelog(
            "\n\u2554" + "\u2550"*44 + "\u2557\n"
            "\u2551          Processing Complete            \u2551\n"
            "\u255a" + "\u2550"*44 + "\u255d", "hdr")
        self._writelog(
            f"  .html files created this run: {len(self._created_this_run)}", "ok")
        if self._created_this_run:
            self._writelog("\n  Files created this run:", "hdr")
            for p in self._created_this_run:
                self._writelog(f"    {p}", "dim")

    def _on_exit(self):
        if self._busy:
            if not messagebox.askyesno("Task Running",
                                       "A task is in progress. Quit anyway?"):
                return
        self.destroy()


# ── Entry point ───────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app = App()
    app.mainloop()
