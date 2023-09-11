import tkinter as tk
from tkinter import messagebox
import requests

# Oxford Dictionaries API details
BASE_URL = "https://od-api.oxforddictionaries.com/api/v2/entries/en-gb/"
APP_ID = "YOUR_APP_ID"  # replace with your APP ID
APP_KEY = "YOUR_APP_KEY"  # replace with your APP KEY
HEADERS = {
    "app_id": APP_ID,
    "app_key": APP_KEY
}

def fetch_definition(word):
    try:
        response = requests.get(BASE_URL + word, headers=HEADERS)
        response.raise_for_status()
        json_data = response.json()
        definition = json_data["results"][0]["lexicalEntries"][0]["entries"][0]["senses"][0]["definitions"][0]
        return definition
    except Exception as e:
        messagebox.showerror("Error", str(e))
        return None

class DictionaryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Dictionary App")
        
        self.word_label = tk.Label(self, text="Enter Word:")
        self.word_label.pack(pady=10)
        
        self.word_entry = tk.Entry(self, width=50)
        self.word_entry.pack(pady=10)
        
        self.definition_label = tk.Label(self, text="Definition:")
        self.definition_label.pack(pady=10)
        
        self.definition_text = tk.Text(self, width=50, height=10)
        self.definition_text.pack(pady=10)
        
        self.search_button = tk.Button(self, text="Search", command=self.search_definition)
        self.search_button.pack(pady=10)

    def search_definition(self):
        word = self.word_entry.get()
        if word:
            definition = fetch_definition(word)
            self.definition_text.delete(1.0, tk.END)
            if definition:
                self.definition_text.insert(tk.END, definition)
        else:
            messagebox.showwarning("Warning", "Please enter a word!")

if __name__ == "__main__":
    app = DictionaryApp()
    app.mainloop()
