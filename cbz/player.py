import hashlib
import tkinter as tk
import os

from io import BytesIO
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL
from ctypes import windll

from PIL import Image, ImageTk
from pathlib import Path

from cbz.comic import ComicInfo
from cbz.page import PageInfo
from cbz.utils import readable_size, ico_to_png

PARENT = Path(__file__).parent
CTRL_KEY = 0x4  # Constant for Ctrl key


class Player:
    """
    A simple comic book player application using Tkinter.

    This class initializes a graphical user interface (GUI) using Tkinter
    to display comic book pages (either as images or summaries). It supports
    navigation between pages, window resizing, and basic comic book information
    display.

    Attributes:
        comic_info (ComicInfo): Object containing comic book information.
        current_page (int): Index of the currently displayed page (-1 for summary).
        root (tk.Tk): Tkinter root window instance.
        main_frame (ttk.Frame): Frame for holding main content.
        canvas (tk.Canvas): Canvas for displaying comic book pages.
        prev_button (ttk.Button): Button for navigating to the previous page.
        next_button (ttk.Button): Button for navigating to the next page.
        summary_text (tk.Text): Text widget for displaying comic book information summary.
        page_index_label (ttk.Label): Label showing the current page index.
        previous_width (int): Previous width of the main window.
        previous_height (int): Previous height of the main window.
        resize_timer (int or None): Timer ID for handling window resize delay.
        max_zoom_factor (float or None): Maximum allowable zoom factor based on canvas size and image dimensions.
        zoom_factor (float or None): Current zoom factor for image display.
        img_original (PIL.Image.Image or None): Placeholder for the original image to be displayed.
    """

    def __init__(self, comic_info: ComicInfo):
        """
        Initialize the comic player with the given ComicInfo object.

        Args:
            comic_info (ComicInfo): Object containing comic book information.
        """
        self.comic_info = comic_info
        self.current_page = -1  # Track the current page index
        self.max_zoom_factor = None  # Maximum allowable zoom factor based on canvas size and image dimensions
        self.zoom_factor = None  # Initial zoom factor (None means no zoom initially)
        self.img_original = None  # Placeholder for the original image

        # Initialize tkinter window
        self.root = tk.Tk()
        self.root.title(self._get_window_title())

        # Set initial window size
        self.root.geometry(self._get_initial_geometry())

        # Set the application icon
        self._set_icon()

        # Create main frame for content
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Create canvas for displaying pages
        self.canvas = tk.Canvas(self.main_frame, bg='white')
        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Create navigation buttons
        self._create_buttons()

        # Initialize text widget for the summary page
        self._init_summary_text()

        # Display initial page content
        self.show_page()

        # Bind keys for navigation and window resize
        self._bind_keys()

        # Initialize the previous window size
        self.previous_width = self.root.winfo_width()
        self.previous_height = self.root.winfo_height()

        # Initialize resize timer
        self.resize_timer = None

    def _set_icon(self) -> None:
        """
        Set the application icon for the window.
        """
        image_path = PARENT / 'cbz.ico'
        if os.name == 'nt':
            # Set the application ID and icon on Windows
            windll.shell32.SetCurrentProcessExplicitAppUserModelID('cbz.player')
            self.root.iconbitmap(image_path)
        else:
            # Convert ICO to PNG for other operating systems
            image = ico_to_png(image_path)
            self.root.iconphoto(True, tk.PhotoImage(data=image.getvalue()))

    def _get_window_title(self) -> str:
        """
        Get the window title based on the comic series and title.

        Returns:
            str: Window title.
        """
        if self.comic_info.series and self.comic_info.title:
            return f'{self.comic_info.series} - {self.comic_info.title}'
        return self.comic_info.title or self.__class__.__name__

    def _get_initial_geometry(self) -> str:
        """
        Calculate the initial window size and position based on the first page of the comic or default screen size.

        Returns:
            str: Initial window geometry string in the format 'widthxheight+x_position+y_position'.
        """
        # Determine initial window size based on first page or default
        margin_width = self.root.winfo_screenwidth() * 0.1
        margin_height = self.root.winfo_screenheight() * 0.1

        # Calculate available space after margins
        available_width = self.root.winfo_screenwidth() - 2 * margin_width
        available_height = self.root.winfo_screenheight() - 2 * margin_height

        # Default screen size for initialization
        screen_width = int(available_height * 0.63)
        screen_height = int(available_height)

        # Calculate scaling factors for width and height
        if self.comic_info.pages:
            # Get the minimum dimensions from all pages
            image_width = self.comic_info.pages[0].image_width
            image_height = self.comic_info.pages[0].image_height
            for page in self.comic_info.pages[1:]:
                if page.image_width <= image_width and page.image_height <= image_height:
                    image_width = page.image_width
                    image_height = page.image_height

            scale_width = available_width / image_width
            scale_height = available_height / image_height

            # Choose the smaller scaling factor to maintain proportions
            scale_factor = min(scale_width, scale_height)

            # Calculate new dimensions
            initial_width = int(image_width * scale_factor * 0.94)
            initial_height = int(image_height * scale_factor)
        else:
            # If no pages are available, default to screen size
            initial_width = screen_width
            initial_height = screen_height

        # Ensure that the window's initial width is at least 50% of the screen width
        if 100 / screen_width * initial_width < 50.0:
            initial_width = screen_width

        # Calculate initial position to center the window on the screen
        x = self.root.winfo_screenwidth() // 2 - initial_width // 2
        y = self.root.winfo_screenheight() // 2 - initial_height // 2

        return f'{initial_width}x{initial_height}+{x}+{y}'

    def _create_buttons(self) -> None:
        """
        Create navigation buttons for previous, next, and exit operations.
        """
        # Create button frame
        button_frame = ttk.Frame(self.main_frame, height=10)
        button_frame.pack(side=tk.BOTTOM, pady=10)

        # Previous page button
        self.prev_button = ttk.Button(button_frame, text='Previous', command=self.on_previous)
        self.prev_button.pack(side=tk.LEFT, padx=10)

        # Page index label
        self.page_index_label = ttk.Label(button_frame, text=f'{self.current_page + 1}/{len(self.comic_info.pages)}')
        self.page_index_label.pack(side=tk.LEFT, padx=10)

        # Next page button
        self.next_button = ttk.Button(button_frame, text='Next', command=self.one_next)
        self.next_button.pack(side=tk.LEFT, padx=10)

        # Exit button (optional)
        exit_button = ttk.Button(button_frame, text='Exit', command=self.root.quit)
        exit_button.pack(side=tk.RIGHT, padx=10)

    def _init_summary_text(self) -> None:
        """
        Initialize the summary text widget for displaying comic information.
        """
        self.summary_text = tk.Text(self.canvas, wrap=tk.WORD, bg='white', bd=0, padx=10, pady=10)
        self.summary_text.tag_configure('bold', font=('Arial', 13, 'bold'))
        self.summary_text.tag_configure('normal', font=('Arial', 12), lmargin1=10, lmargin2=10)
        self.summary_text.config(state=DISABLED)

    def show_page(self) -> None:
        """
        Display the current page content (either summary or image).
        """
        # Clear previous content on canvas
        self.canvas.delete('all')

        # Display page content
        if self.current_page == -1:
            self._show_summary_page()
        elif self.current_page < len(self.comic_info.pages):
            self._show_image_page()

        # Update navigation button states based on current page index
        self.prev_button.config(state=DISABLED if self.current_page == -1 else NORMAL)
        self.next_button.config(state=DISABLED if self.current_page + 1 == len(self.comic_info.pages) else NORMAL)

        # Update page index label text
        self.page_index_label.config(text=f'{self.current_page + 1}/{len(self.comic_info.pages)}')

    def _show_summary_page(self) -> None:
        """
        Display the summary page with comic information.
        """
        # Use update_idletasks to ensure window size is updated before using it
        self.root.update_idletasks()

        # Display summary for the first page
        infos = self.comic_info.get_info()
        packed = self.comic_info.pack()
        infos['Pages'] = len(infos['Pages'])
        infos['Size'] = readable_size(len(packed), decimal=2)
        infos['MD5'] = hashlib.md5(packed).hexdigest()

        self.summary_text.config(state=NORMAL)
        self.summary_text.delete('1.0', tk.END)

        for key, value in infos.items():
            self.summary_text.insert(tk.END, f'{key}\n', 'bold')
            self.summary_text.insert(tk.END, f'{value}\n\n', 'normal')

        self.summary_text.config(state=DISABLED)
        self.summary_text.place(relwidth=1, relheight=1)

    def _show_image_page(self) -> None:
        """
        Display the image page centered on the canvas.
        """
        # Hide the summary text widget
        self.summary_text.place_forget()

        # Display image centered on canvas
        page: PageInfo = self.comic_info.pages[self.current_page]
        self.img_original = Image.open(BytesIO(page.content))
        self._display_image()

    def _display_image(self) -> None:
        """
        Display the image on the canvas with zooming capabilities.
        """
        # Check if zoom factor is not set; initialize zoom factors
        if not self.zoom_factor:
            # Determine maximum zoom factor based on canvas size and original image size
            self.max_zoom_factor = min(
                self.canvas.winfo_width() / self.img_original.width,
                self.canvas.winfo_height() / self.img_original.height
            )
            self.zoom_factor = self.max_zoom_factor

        # Calculate new dimensions of the image based on current zoom factor
        new_width = int(self.img_original.width * self.zoom_factor)
        new_height = int(self.img_original.height * self.zoom_factor)
        img = self.img_original.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Convert the resized image to PhotoImage format compatible with Tkinter canvas
        self.canvas.image = ImageTk.PhotoImage(img)

        # Calculate the position to center the image on the canvas
        x = max(0, (self.canvas.winfo_width() - new_width) // 2)
        y = max(0, (self.canvas.winfo_height() - new_height) // 2)
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.canvas.image)

        # Configure the scroll region of the canvas to allow scrolling if image is larger than canvas
        canvas_width = max(new_width, self.canvas.winfo_width())
        canvas_height = max(new_height, self.canvas.winfo_height())
        self.canvas.config(scrollregion=(0, 0, canvas_width, canvas_height))

    def _bind_keys(self) -> None:
        """
        Bind keys for navigation (left/right arrow keys) and window events.
        """
        # Bind arrow keys for navigation
        self.root.bind('<Left>', lambda event: self.on_previous())
        self.root.bind('<Right>', lambda event: self.one_next())

        # Bind Ctrl+Q to exit application
        self.root.bind('<Control-q>', lambda event: self.root.quit())
        # Bind the configure event to handle window resize
        self.root.bind('<Configure>', lambda event: self.on_window(event))

        # Bind mouse wheel events for zooming
        self.root.bind('<Control-MouseWheel>', self.on_zoom)
        self.canvas.bind_all("<MouseWheel>", self._on_mouse_wheel)
        self.canvas.bind_all("<Shift-MouseWheel>", self._on_shift_mouse_wheel)

        # Bind zoom controls to keyboard keys
        self.root.bind('<KeyPress-plus>', lambda event: self.on_zoom_key(True))
        self.root.bind('<KeyPress-minus>', lambda event: self.on_zoom_key(False))

    def on_zoom_key(self, positive: bool) -> None:
        """
        Handle zooming triggered by keyboard keys ('+' for zoom in, '-' for zoom out).

        Args:
            positive (bool): True for zoom in, False for zoom out.
        """
        # Create a synthetic event object to simulate mouse wheel scrolling
        event = tk.Event()
        event.delta = 120 if positive else -120
        self.on_zoom(event)

    def on_zoom(self, event) -> None:
        """
        Handle zooming using Ctrl + Mouse Wheel.
        """
        if self.current_page == -1: return

        # Adjust zoom factor based on mouse wheel direction
        if event.delta > 0:
            # Increase zoom factor by 10% for zoom in
            self.zoom_factor *= 1.1
        elif event.delta < 0:
            # Decrease zoom factor by 10% for zoom out
            self.zoom_factor /= 1.1

        # Ensure the zoom-out factor doesn't go below the original image size
        min_zoom_factor = min(
            self.canvas.winfo_width() / self.img_original.width,
            self.canvas.winfo_height() / self.img_original.height
        )

        if self.zoom_factor < min_zoom_factor:
            self.zoom_factor = min_zoom_factor

        # Update the displayed image with the new zoom factor
        self._display_image()

    def _on_mouse_wheel(self, event) -> None:
        """
        Handle vertical scroll using Mouse Wheel.
        """
        if self.current_page == -1 or (event.state & CTRL_KEY): return
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mouse_wheel(self, event) -> None:
        """
        Handle horizontal scroll using Shift + Mouse Wheel.
        """
        if self.current_page == -1 or (event.state & CTRL_KEY): return
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def on_previous(self) -> None:
        """
        Navigate to the previous page.
        """
        if self.current_page == -1: return
        self.current_page -= 1
        self.show_page()

    def one_next(self) -> None:
        """
        Navigate to the next page.
        """
        if self.current_page < len(self.comic_info.pages) - 1:
            self.current_page += 1
            self.show_page()

    def on_window(self, event: any) -> None:
        """
        Handle window resize event.
        """
        # Check if width or height has changed
        if event.width != self.previous_width or event.height != self.previous_height:
            self.previous_width = event.width
            self.previous_height = event.height

            # Cancel any existing resize timer
            if self.resize_timer:
                self.root.after_cancel(self.resize_timer)

            # Set a new timer to call show_page after a delay
            self.resize_timer = self.root.after(200, self._on_resize)

    def _on_resize(self) -> None:
        """
        Handle resizing of the window and adjust image display accordingly.
        """
        if self.current_page == -1: return

        # Reset zoom factor to None if it's equal to the maximum zoom factor
        if self.zoom_factor == self.max_zoom_factor:
            self.zoom_factor = None

        # Update the displayed image with the current zoom factor
        self._display_image()

        # Reset the resize timer
        self.resize_timer = None

    def run(self) -> None:
        """
        Run the comic player application.
        """
        self.root.mainloop()
