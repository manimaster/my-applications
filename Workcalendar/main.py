import tkinter as tk
from tkinter import ttk, scrolledtext

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Python App with Tabs")
        self.geometry('800x600')  # Set window size
        
        # Create main notebook (tabs)
        self.notebook = ttk.Notebook(self)
        
        # Create tabs
        self.tab1 = ttk.Frame(self.notebook)
        self.tab2 = ttk.Frame(self.notebook)
        self.tab3 = ttk.Frame(self.notebook)
        
        # Add tabs to the notebook
        self.notebook.add(self.tab1, text="Important Commands")
        self.notebook.add(self.tab2, text="Important Notes")
        self.notebook.add(self.tab3, text="Search")
        
        # Pack the notebook
        self.notebook.pack(expand=True, fill='both')
        
        # Initialize data
        self.commands_data = []
        self.notes_data = []
        
        # Design tabs
        self._design_tab1()
        self._design_tab2()
        self._design_tab3()
        
    def _design_tab1(self):
        # Input section
        ttk.Label(self.tab1, text="Description").grid(row=0, column=0)
        self.cmd_desc_input = ttk.Entry(self.tab1)
        self.cmd_desc_input.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.tab1, text="Tags").grid(row=1, column=0)
        self.cmd_tags_input = ttk.Entry(self.tab1)
        self.cmd_tags_input.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.tab1, text="Command").grid(row=2, column=0)
        self.cmd_command_input = scrolledtext.ScrolledText(self.tab1, width=40, height=5)
        self.cmd_command_input.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.tab1, text="Service").grid(row=3, column=0)
        self.cmd_service_input = ttk.Entry(self.tab1)
        self.cmd_service_input.grid(row=3, column=1, padx=10, pady=10)

        add_button = ttk.Button(self.tab1, text="Add Command", command=self._add_command)
        add_button.grid(row=4, column=1, pady=20)

        # Table section
        self.cmd_table = ttk.Treeview(self.tab1, columns=('Description', 'Command', 'Tags', 'Service'))
        self.cmd_table.heading('Description', text='Description')
        self.cmd_table.heading('Command', text='Command')
        self.cmd_table.heading('Tags', text='Tags')
        self.cmd_table.heading('Service', text='Service')
        # self.cmd_table.pack(pady=20)
        self.cmd_table.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky='nsew')


    def _design_tab2(self):
        # Input section
        ttk.Label(self.tab2, text="Description").grid(row=0, column=0)
        self.notes_desc_input = ttk.Entry(self.tab2)
        self.notes_desc_input.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.tab2, text="Tags").grid(row=1, column=0)
        self.notes_tags_input = ttk.Entry(self.tab2)
        self.notes_tags_input.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.tab2, text="Notes").grid(row=2, column=0)
        self.notes_notes_input = scrolledtext.ScrolledText(self.tab2, width=40, height=5)
        self.notes_notes_input.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.tab2, text="Service").grid(row=3, column=0)
        self.notes_service_input = ttk.Entry(self.tab2)
        self.notes_service_input.grid(row=3, column=1, padx=10, pady=10)

        add_button = ttk.Button(self.tab2, text="Add Note", command=self._add_note)
        add_button.grid(row=4, column=1, pady=20)

        # Table section
        self.notes_table = ttk.Treeview(self.tab2, columns=('Description', 'Notes', 'Tags', 'Service'))
        self.notes_table.heading('Description', text='Description')
        self.notes_table.heading('Notes', text='Notes')
        self.notes_table.heading('Tags', text='Tags')
        self.notes_table.heading('Service', text='Service')
        self.notes_table.grid(row=5, column=0, columnspan=2, padx=10, pady=20, sticky='nsew')

    def _design_tab3(self):
        # Search section
        ttk.Label(self.tab3, text="Search for Command/Notes").grid(row=0, column=0)
        self.search_input = ttk.Entry(self.tab3, width=40)
        self.search_input.grid(row=0, column=1, padx=10, pady=10)
        
        search_button = ttk.Button(self.tab3, text="Search and List", command=self._search)
        search_button.grid(row=1, column=1, pady=20)

        # Results section
        self.search_table = ttk.Treeview(self.tab3, columns=('Description', 'Data', 'Tags', 'Service'))
        self.search_table.heading('Description', text='Description')
        self.search_table.heading('Data', text='Notes/Commands')
        self.search_table.heading('Tags', text='Tags')
        self.search_table.heading('Service', text='Service')
        self.search_table.grid(row=2, column=0, columnspan=2, padx=10, pady=20, sticky='nsew')

    def _add_command(self):
        desc = self.cmd_desc_input.get()
        tags = self.cmd_tags_input.get()
        cmd = self.cmd_command_input.get("1.0", tk.END).strip()
        service = self.cmd_service_input.get()

        self.commands_data.append({
            'Description': desc,
            'Command': cmd,
            'Tags': tags,
            'Service': service
        })

        self.cmd_table.insert("", tk.END, values=(desc, cmd, tags, service))

    def _add_note(self):
        desc = self.notes_desc_input.get()
        tags = self.notes_tags_input.get()
        note = self.notes_notes_input.get("1.0", tk.END).strip()
        service = self.notes_service_input.get()

        self.notes_data.append({
            'Description': desc,
            'Notes': note,
            'Tags': tags,
            'Service': service
        })

        self.notes_table.insert("", tk.END, values=(desc, note, tags, service))

    def _search(self):
        search_term = self.search_input.get().lower()

        # Clear the previous search results
        for item in self.search_table.get_children():
            self.search_table.delete(item)

        # Search in commands
        for cmd in self.commands_data:
            if search_term in cmd['Description'].lower() or search_term in cmd['Tags'].lower():
                self.search_table.insert("", tk.END, values=(cmd['Description'], cmd['Command'], cmd['Tags'], cmd['Service']))

        # Search in notes
        for note in self.notes_data:
            if search_term in note['Description'].lower() or search_term in note['Tags'].lower():
                self.search_table.insert("", tk.END, values=(note['Description'], note['Notes'], note['Tags'], note['Service']))

if __name__ == "__main__":
    app = Application()
    app.mainloop()
