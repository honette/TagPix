import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
from PIL import Image, ImageTk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ImageTaggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TagPix - Image Tagger")
        self.root.geometry("900x700")
        
        # Initialize variables
        self.image_files = []
        self.current_index = 0
        self.tags = set()
        self.available_tags = []
        
        # Load available tags from file
        self.available_tags = ['1girl', 'smile', 'standing']
        
        # Enable D&D support
        # Removed reassigning self.root to TkinterDnD.Tk()
        
        # UI Elements
        # self.load_available_tags()
        self.create_widgets()

    def create_widgets(self):
        # Load and navigation buttons at the top
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=10)

        self.load_button = tk.Button(self.button_frame, text="Load Folder", command=self.load_folder)
        self.load_button.pack(side="left", padx=10)
        self.prev_button = tk.Button(self.button_frame, text="Previous", command=self.prev_image)
        self.prev_button.pack(side="left", padx=5)
        self.next_button = tk.Button(self.button_frame, text="Next", command=self.next_image)
        self.next_button.pack(side="left", padx=5)

        # Tag buttons below navigation buttons
        self.tag_button_frame = tk.Frame(self.root)
        self.tag_button_frame.pack(pady=10, fill='x')
        for tag in self.available_tags:
            tag_button = tk.Button(self.tag_button_frame, text=tag, command=lambda t=tag: self.add_tag_from_button(t))
            tag_button.pack(side="left", padx=5, pady=10)

        # Tag display area (Text Box) with Save Tags button
        self.tag_display_frame = tk.Frame(self.root)
        self.tag_display_frame.pack(pady=10, fill='x', padx=50)

        self.tag_text = tk.Text(self.tag_display_frame, height=2, wrap='word')
        self.tag_text.pack(side='left', fill='x', expand=True, padx=5)
        
        self.save_button = tk.Button(self.tag_display_frame, text="Save Tags", command=self.save_tags)
        self.save_button.pack(side='left', padx=10)

        # Image preview area
        self.img_label = tk.Label(self.root, text="Drop Image Here", relief="solid")
        self.img_label.pack(pady=10, padx=50, expand=True, fill='both')
        
        # Set up D&D on the image label
        self.img_label.drop_target_register(DND_FILES)
        self.img_label.dnd_bind('<<Drop>>', self.on_drop)

    def load_available_tags(self):
        # Load available tags from planned_tags.txt
        tag_file = 'planned_tags.txt'
        if os.path.exists(tag_file):
            with open(tag_file, 'r') as file:
                self.available_tags = [line.strip() for line in file if line.strip()]

    def on_drop(self, event):
        # Handle the dropped file
        file_path = event.data.strip('{}')
        if os.path.isfile(file_path) and file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            self.image_files = [file_path]
            self.current_index = 0
            self.load_image()

    def load_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.image_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
                                if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
            self.current_index = 0
            self.load_image()

    def load_image(self):
        if self.image_files:
            file_path = self.image_files[self.current_index]
            image = Image.open(file_path)
            
            # Resize while maintaining aspect ratio, with the longer side being 800 pixels
            max_size = 800
            original_width, original_height = image.size
            if original_width > original_height:
                new_width = max_size
                new_height = int((max_size / original_width) * original_height)
            else:
                new_height = max_size
                new_width = int((max_size / original_height) * original_width)
            image = image.resize((new_width, new_height), Image.LANCZOS)
            
            # Keep image reference to prevent garbage collection
            self.img_tk = ImageTk.PhotoImage(image)
            
            # Update label size and image
            self.img_label.config(image=self.img_tk, text="")
            self.load_tags(file_path)
            self.update_tag_display()

    def load_tags(self, file_path):
        self.tags.clear()
        tag_file = f"{os.path.splitext(file_path)[0]}.txt"
        if os.path.exists(tag_file):
            with open(tag_file, "r") as file:
                tags = file.read().split(", ")
                self.tags.update(tags)
        self.update_tag_display()

    def add_tag_from_button(self, tag):
        self.tags.add(tag)
        self.tag_text.delete(1.0, tk.END)
        self.tag_text.insert(tk.END, ', '.join(self.tags))
        self.update_tag_display()

    def update_tag_display(self):
        self.tag_text.delete(1.0, tk.END)
        self.tag_text.insert(tk.END, ', '.join(self.tags))

    def save_tags(self):
        if not self.image_files:
            messagebox.showerror("Error", "No image loaded.")
            return
        file_path = self.image_files[self.current_index]
        tag_file = f"{os.path.splitext(file_path)[0]}.txt"
        tags_to_save = self.tag_text.get(1.0, tk.END).strip()
        tag_file = f"{os.path.splitext(file_path)[0]}.txt"
        with open(tag_file, "w") as file:
            file.write(tags_to_save)
        messagebox.showinfo("Saved", "Tags saved successfully!")

    def next_image(self):
        if self.image_files and self.current_index < len(self.image_files) - 1:
            self.current_index += 1
            self.load_image()

    def prev_image(self):
        if self.image_files and self.current_index > 0:
            self.current_index -= 1
            self.load_image()

if __name__ == "__main__":
    root = TkinterDnD.Tk()  # Create the TkinterDnD root window
    app = ImageTaggerApp(root)
    root.mainloop()
