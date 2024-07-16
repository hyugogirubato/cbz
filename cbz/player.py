import hashlib
import tkinter as tk
from io import BytesIO
from tkinter import ttk
from tkinter.constants import DISABLED, NORMAL
from ctypes import windll

from PIL import Image, ImageTk
from pathlib import Path

from cbz.comic import ComicInfo
from cbz.page import PageInfo
from cbz.utils import readable_size, ico_to_png
import os

PARENT = Path(__file__).parent


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
    """

    def __init__(self, comic_info: ComicInfo):
        """
        Initialize the comic player with the given ComicInfo object.

        Args:
            comic_info (ComicInfo): Object containing comic book information.
        """
        self.comic_info = comic_info
        self.current_page = -1  # Track the current page index

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
        # TODO: Support scrollable image and/or zoom when it is too large for the screen (eg: webtoon)
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
            initial_width = int(available_height * 0.63)
            initial_height = int(available_height)

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

    def show_page(self):
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
        img = Image.open(BytesIO(page.content))

        # Calculate scaling factor
        scale_width = self.canvas.winfo_width() / img.width
        scale_height = self.canvas.winfo_height() / img.height
        scale_factor = min(scale_width, scale_height)

        # Resize image
        new_width = int(img.width * scale_factor)
        new_height = int(img.height * scale_factor)
        img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Set image on canvas
        self.canvas.image = ImageTk.PhotoImage(img)

        # Calculate coordinates to center the image on the canvas
        x = (self.canvas.winfo_width() - new_width) // 2
        y = (self.canvas.winfo_height() - new_height) // 2
        self.canvas.create_image(x, y, anchor=tk.NW, image=self.canvas.image)

    def _bind_keys(self) -> None:
        """
        Bind keys for navigation (left/right arrow keys) and window events.
        """
        # Bind arrow keys for navigation
        self.root.bind('<Left>', lambda event: self.on_previous())
        self.root.bind('<Right>', lambda event: self.one_next())

        # Bind Ctrl+C to exit application
        self.root.bind('<Control-q>', lambda event: self.root.quit())

        # Bind the configure event to handle window resize
        self.root.bind('<Configure>', lambda event: self.on_window(event))

    def on_previous(self) -> None:
        """
        Navigate to the previous page.
        """
        if self.current_page > -1:
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
            self.resize_timer = self.root.after(100, self.show_page)

    def run(self) -> None:
        """
        Run the comic player application.
        """
        self.root.mainloop()
