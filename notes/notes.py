import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

# File to store notes
NOTES_FILE = 'notes.json'

# Check if the file exists. If not, create it
if not os.path.exists(NOTES_FILE):
    with open(NOTES_FILE, 'w') as file:
        json.dump({}, file)


class NoteTakingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Note-Taking App")
        
        # UI for tags
        self.tag_label = tk.Label(self, text="Select Tag:")
        self.tag_label.grid(row=0, column=0, padx=20, pady=(20, 0))
        
        self.tag_entry = tk.Entry(self, width=40)
        self.tag_entry.grid(row=1, column=0, columnspan=2, padx=20)
        
        self.load_button = tk.Button(self, text="Load Notes", command=self.load_notes)
        self.load_button.grid(row=1, column=2, padx=20)
        
        # Listbox for notes
        self.notes_listbox = tk.Listbox(self, width=50, height=10)
        self.notes_listbox.grid(row=2, column=0, columnspan=3, padx=20, pady=20)
        
        # Text widget for note content
        self.note_content_text = tk.Text(self, width=50, height=10)
        self.note_content_text.grid(row=3, column=0, columnspan=3, padx=20, pady=20)
        
        # Buttons for CRUD operations
        self.new_button = tk.Button(self, text="New Note", command=self.new_note)
        self.new_button.grid(row=4, column=0, pady=20)
        
        self.save_button = tk.Button(self, text="Save Note", command=self.save_note)
        self.save_button.grid(row=4, column=1, pady=20)
        
        self.delete_button = tk.Button(self, text="Delete Note", command=self.delete_note)
        self.delete_button.grid(row=4, column=2, pady=20)

    def get_all_notes(self):
        with open(NOTES_FILE, 'r') as file:
            return json.load(file)

    def save_all_notes(self, notes):
        with open(NOTES_FILE, 'w') as file:
            json.dump(notes, file)

    def load_notes(self):
        tag = self.tag_entry.get()
        if not tag:
            messagebox.showwarning("Warning", "Please enter a tag!")
            return
        
        self.notes_listbox.delete(0, tk.END)
        all_notes = self.get_all_notes()
        
        for note in all_notes.get(tag, []):
            self.notes_listbox.insert(tk.END, note['title'])

    def new_note(self):
        title = simpledialog.askstring("New Note", "Enter Note Title:")
        if title:
            self.notes_listbox.insert(tk.END, title)
            self.note_content_text.delete(1.0, tk.END)
    
    def save_note(self):
        selected_idx = self.notes_listbox.curselection()
        title = self.notes_listbox.get(selected_idx) if selected_idx else None
        content = self.note_content_text.get(1.0, tk.END).strip()
        tag = self.tag_entry.get()

        if not title or not content or not tag:
            messagebox.showwarning("Warning", "Please select a note and ensure note content is not empty!")
            return

        all_notes = self.get_all_notes()
        if tag not in all_notes:
            all_notes[tag] = []

        for note in all_notes[tag]:
            if note['title'] == title:
                note['content'] = content
                break
        else:
            all_notes[tag].append({'title': title, 'content': content})

        self.save_all_notes(all_notes)

    def delete_note(self):
        selected_idx = self.notes_listbox.curselection()
        title = self.notes_listbox.get(selected_idx) if selected_idx else None
        tag = self.tag_entry.get()

        if not title or not tag:
            messagebox.showwarning("Warning", "Please select a note to delete!")
            return

        all_notes = self.get_all_notes()
        if tag in all_notes:
            all_notes[tag] = [note for note in all_notes[tag] if note['title'] != title]

            if not all_notes[tag]:
                del all_notes[tag]

        self.save_all_notes(all_notes)
        self.load_notes()
        self.note_content_text.delete(1.0, tk.END)

# Create and run the app
app = NoteTakingApp()
app.mainloop()
