"""
Tkinter-based graphical comic reader.

Provides a viewing interface with page navigation, zoom,
scrolling and metadata display.
"""

from __future__ import annotations

import os
import tkinter as tk
from io import BytesIO
from pathlib import Path
from tkinter import ttk
from typing import Optional

try:
    from ctypes import windll
except ImportError:
    windll = None

from PIL import Image, ImageTk

from cbz.comic import ComicInfo
from cbz.page import PageInfo
from cbz.utils import readable_size, ico_to_png

PARENT = Path(__file__).parent
CTRL_KEY = 0x4  # Tkinter event.state bitmask for the Ctrl modifier


class Player:
    """Comic reader with Tkinter graphical interface.

    Displays comic pages with navigation, zoom and
    a metadata summary page.

    Attributes:
        comic: The comic to display.
        current_page: Index of the current page (-1 = summary).
        root: Main Tkinter window.
    """

    def __init__(self, comic: ComicInfo) -> None:
        """Initialize the reader with a comic.

        Args:
            comic: ComicInfo instance to display.
        """
        self.comic = comic
        self.current_page: int = -1
        self.max_zoom_factor: Optional[float] = None
        self.zoom_factor: Optional[float] = None
        self.img_original: Optional[Image.Image] = None

        # Window initialization
        self.root = tk.Tk()
        self.root.title(self._get_window_title())
        self.root.geometry(self._get_initial_geometry())
        self._set_icon()

        # Main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Display canvas
        self.canvas = tk.Canvas(self.main_frame, bg="white")
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Navigation buttons
        self._create_buttons()

        # Summary text widget
        self._init_summary_text()

        # Initial display
        self.show_page()

        # Keyboard shortcuts and events
        self._bind_keys()

        # Resize tracking
        self.previous_width = self.root.winfo_width()
        self.previous_height = self.root.winfo_height()
        self.resize_timer: Optional[str] = None

    def _set_icon(self) -> None:
        """Set the application icon."""
        icon_path = PARENT / "cbz.ico"
        if os.name == "nt" and windll is not None:
            windll.shell32.SetCurrentProcessExplicitAppUserModelID("cbz.player")
            self.root.iconbitmap(icon_path)
        else:
            image = ico_to_png(icon_path)
            self.root.iconphoto(True, tk.PhotoImage(data=image.getvalue()))

    def _get_window_title(self) -> str:
        """Build the window title."""
        if self.comic.series and self.comic.title:
            return f"{self.comic.series} - {self.comic.title}"
        return self.comic.title or self.__class__.__name__

    def _get_initial_geometry(self) -> str:
        """Calculate the initial window geometry."""
        margin_w = self.root.winfo_screenwidth() * 0.1
        margin_h = self.root.winfo_screenheight() * 0.1
        avail_w = self.root.winfo_screenwidth() - 2 * margin_w
        avail_h = self.root.winfo_screenheight() - 2 * margin_h

        screen_w = int(avail_h * 0.63)
        screen_h = int(avail_h)

        if self.comic.pages:
            # Use minimum dimensions across all pages
            img_w = self.comic.pages[0].image_width
            img_h = self.comic.pages[0].image_height
            for page in self.comic.pages[1:]:
                if page.image_width <= img_w and page.image_height <= img_h:
                    img_w = page.image_width
                    img_h = page.image_height

            scale = min(avail_w / img_w, avail_h / img_h)
            init_w = int(img_w * scale * 0.94)
            init_h = int(img_h * scale)
        else:
            init_w = screen_w
            init_h = screen_h

        if 100 / screen_w * init_w < 50.0:
            init_w = screen_w

        x = self.root.winfo_screenwidth() // 2 - init_w // 2
        y = self.root.winfo_screenheight() // 2 - init_h // 2
        return f"{init_w}x{init_h}+{x}+{y}"

    def _create_buttons(self) -> None:
        """Create navigation buttons."""
        button_frame = ttk.Frame(self.main_frame, height=10)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        self.prev_button = ttk.Button(button_frame, text="Previous", command=self.on_previous)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        self.page_index_label = ttk.Label(
            button_frame, text=f"{self.current_page + 1}/{len(self.comic)}"
        )
        self.page_index_label.pack(side=tk.LEFT, padx=10)

        self.next_button = ttk.Button(button_frame, text="Next", command=self.on_next)
        self.next_button.pack(side=tk.LEFT, padx=10)

        exit_button = ttk.Button(button_frame, text="Exit", command=self.root.quit)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def _init_summary_text(self) -> None:
        """Initialize the metadata summary text widget."""
        self.summary_text = tk.Text(self.canvas, wrap=tk.WORD, bg="white", bd=0, padx=10, pady=10)
        self.summary_text.tag_configure("bold", font=("Arial", 13, "bold"))
        self.summary_text.tag_configure("normal", font=("Arial", 12), lmargin1=10, lmargin2=10)
        self.summary_text.config(state=tk.DISABLED)

    def show_page(self) -> None:
        """Display the current page (summary or image)."""
        self.canvas.delete("all")

        if self.current_page == -1:
            self._show_summary_page()
        elif self.current_page < len(self.comic):
            self._show_image_page()

        self.prev_button.config(state=tk.DISABLED if self.current_page == -1 else tk.NORMAL)
        self.next_button.config(
            state=tk.DISABLED if self.current_page + 1 == len(self.comic) else tk.NORMAL
        )
        self.page_index_label.config(text=f"{self.current_page + 1}/{len(self.comic)}")

    def _show_summary_page(self) -> None:
        """Display the summary page with metadata."""
        self.root.update_idletasks()
        infos = self.comic.get_info()

        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete("1.0", tk.END)

        for key, value in infos.items():
            if not (key.startswith("@") or key == "Pages"):
                if key == "FileSize":
                    value = readable_size(value)
                self.summary_text.insert(tk.END, f"{key}\n", "bold")
                self.summary_text.insert(tk.END, f"{value}\n\n", "normal")

        self.summary_text.config(state=tk.DISABLED)
        self.summary_text.place(relwidth=1, relheight=1)

    def _show_image_page(self) -> None:
        """Display an image page centered on the canvas."""
        self.summary_text.place_forget()
        if self.img_original is not None:
            self.img_original.close()
        page: PageInfo = self.comic[self.current_page]
        self.img_original = Image.open(BytesIO(page.content))
        self._display_image()

    def _display_image(self) -> None:
        """Display the image with the current zoom level."""
        if not self.zoom_factor:
            self.max_zoom_factor = min(
                self.canvas.winfo_width() / self.img_original.width,
                self.canvas.winfo_height() / self.img_original.height,
            )
            self.zoom_factor = self.max_zoom_factor

        new_w = int(self.img_original.width * self.zoom_factor)
        new_h = int(self.img_original.height * self.zoom_factor)
        img = self.img_original.resize((new_w, new_h), Image.Resampling.LANCZOS)

        self.canvas.image = ImageTk.PhotoImage(img)
        x = max(0, (self.canvas.winfo_width() - new_w) // 2)
        y = max(0, (self.canvas.winfo_height() - new_h) // 2)
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.canvas.image)

        canvas_w = max(new_w, self.canvas.winfo_width())
        canvas_h = max(new_h, self.canvas.winfo_height())
        self.canvas.config(scrollregion=(0, 0, canvas_w, canvas_h))

    def _bind_keys(self) -> None:
        """Configure keyboard shortcuts and events."""
        self.root.bind("<Left>", lambda _: self.on_previous())
        self.root.bind("<Right>", lambda _: self.on_next())
        self.root.bind("<Control-q>", lambda _: self.root.quit())
        self.root.bind("<Configure>", lambda e: self.on_window(e))

        self.root.bind("<Control-MouseWheel>", self.on_zoom)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mouse_wheel)

        self.root.bind("<KeyPress-plus>", lambda _: self.on_zoom_key(True))
        self.root.bind("<KeyPress-minus>", lambda _: self.on_zoom_key(False))

    def on_zoom_key(self, zoom_in: bool) -> None:
        """Handle keyboard zoom (+ / -)."""
        event = tk.Event()
        event.delta = 120 if zoom_in else -120
        self.on_zoom(event)

    def on_zoom(self, event: tk.Event) -> None:
        """Handle zoom with Ctrl + mouse wheel."""
        if self.current_page == -1:
            return

        if event.delta > 0:
            self.zoom_factor *= 1.1
        elif event.delta < 0:
            self.zoom_factor /= 1.1

        min_zoom = min(
            self.canvas.winfo_width() / self.img_original.width,
            self.canvas.winfo_height() / self.img_original.height,
        )
        if self.zoom_factor < min_zoom:
            self.zoom_factor = min_zoom

        self._display_image()

    def _on_mouse_wheel(self, event: tk.Event) -> None:
        """Handle vertical scrolling."""
        if self.current_page == -1 or (event.state & CTRL_KEY):
            return
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mouse_wheel(self, event: tk.Event) -> None:
        """Handle horizontal scrolling."""
        if self.current_page == -1 or (event.state & CTRL_KEY):
            return
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_previous(self) -> None:
        """Navigate to the previous page."""
        if self.current_page == -1:
            return
        self.current_page -= 1
        self.zoom_factor = None
        self.show_page()

    def on_next(self) -> None:
        """Navigate to the next page."""
        if self.current_page < len(self.comic) - 1:
            self.current_page += 1
            self.zoom_factor = None
            self.show_page()

    def on_window(self, event: tk.Event) -> None:
        """Handle window resize."""
        if event.width != self.previous_width or event.height != self.previous_height:
            self.previous_width = event.width
            self.previous_height = event.height

            if self.resize_timer:
                self.root.after_cancel(self.resize_timer)
            self.resize_timer = self.root.after(200, self._on_resize)

    def _on_resize(self) -> None:
        """React to window resize with delay."""
        if self.current_page == -1:
            return
        if self.zoom_factor == self.max_zoom_factor:
            self.zoom_factor = None
        self._display_image()
        self.resize_timer = None

    def run(self) -> None:
        """Start the reader main loop."""
        self.root.mainloop()
