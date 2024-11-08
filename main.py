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
        self.root.geometry("800x600")
        
        # Initialize variables
        self.image_files = []
        self.current_index = 0
        self.tags = set()
        
        # Enable D&D support
        # Removed reassigning self.root to TkinterDnD.Tk()
        
        # UI Elements
        self.create_widgets()

    def create_widgets(self):
        # Image preview area
        self.img_label = tk.Label(self.root, text="Drop Image Here", relief="solid")
        self.img_label.pack(pady=10, expand=True)
        
        # Set up D&D on the image label
        self.img_label.drop_target_register(DND_FILES)
        self.img_label.dnd_bind('<<Drop>>', self.on_drop)

        # Tag display area
        self.tags_frame = tk.Frame(self.root)
        self.tags_frame.pack()

        # Load and navigation buttons
        self.load_button = tk.Button(self.root, text="Load Folder", command=self.load_folder)
        self.load_button.pack(side="left", padx=10)
        self.prev_button = tk.Button(self.root, text="Previous", command=self.prev_image)
        self.prev_button.pack(side="left", padx=5)
        self.next_button = tk.Button(self.root, text="Next", command=self.next_image)
        self.next_button.pack(side="left", padx=5)

        # Tag entry and add button
        self.tag_entry = tk.Entry(self.root)
        self.tag_entry.pack(side="left", padx=5)
        self.add_tag_button = tk.Button(self.root, text="Add Tag", command=self.add_tag)
        self.add_tag_button.pack(side="left", padx=5)

        # Save button
        self.save_button = tk.Button(self.root, text="Save Tags", command=self.save_tags)
        self.save_button.pack(side="left", padx=10)

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
            self.img_label.pack(pady=10, expand=True)
            self.load_tags(file_path)

    def load_tags(self, file_path):
        self.tags.clear()
        tag_file = f"{os.path.splitext(file_path)[0]}.txt"
        if os.path.exists(tag_file):
            with open(tag_file, "r") as file:
                tags = file.read().split(", ")
                self.tags.update(tags)
        self.update_tag_display()

    def add_tag(self):
        tag = self.tag_entry.get().strip()
        if tag:
            self.tags.add(tag)
            self.tag_entry.delete(0, tk.END)
            self.update_tag_display()

    def update_tag_display(self):
        for widget in self.tags_frame.winfo_children():
            widget.destroy()
        for tag in self.tags:
            tag_label = tk.Label(self.tags_frame, text=tag, relief="solid", padx=5, pady=2)
            tag_label.pack(side="left", padx=5)

    def save_tags(self):
        if not self.image_files:
            messagebox.showerror("Error", "No image loaded.")
            return
        file_path = self.image_files[self.current_index]
        tag_file = f"{os.path.splitext(file_path)[0]}.txt"
        with open(tag_file, "w") as file:
            file.write(", ".join(self.tags))
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
