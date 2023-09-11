import tkinter as tk
from tkinter import ttk, messagebox
import os

BASH_PROFILE_PATH = os.path.expanduser("~/.bash_profile")

class AliasApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Alias Manager for macOS")
        self.geometry("650x450")

        self.tab_control = ttk.Notebook(self)

        # Tabs
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        self.tab3 = ttk.Frame(self.tab_control)
        self.tab4 = ttk.Frame(self.tab_control)

        self.tab_control.add(self.tab1, text='Add Alias')
        self.tab_control.add(self.tab2, text='See Existing Alias')
        self.tab_control.add(self.tab3, text='Backup')
        self.tab_control.add(self.tab4, text='Restore')

        self.create_add_alias_ui()
        self.create_existing_alias_ui()
        self.create_backup_ui()
        self.create_restore_ui()

        self.tab_control.pack(expand=1, fill='both')

    def create_add_alias_ui(self):
        ttk.Label(self.tab1, text="Alias:").grid(column=0, row=0, padx=20, pady=20)
        self.alias_entry = ttk.Entry(self.tab1)
        self.alias_entry.grid(column=1, row=0, padx=20, pady=20)

        ttk.Label(self.tab1, text="Command:").grid(column=0, row=1, padx=20, pady=5)
        self.command_text = tk.Text(self.tab1, width=30, height=5)
        self.command_text.grid(column=1, row=1, padx=20, pady=5)

        ttk.Button(self.tab1, text="Add to Bash Profile", command=self.add_alias).grid(column=0, row=2, columnspan=2, pady=20)

    def create_existing_alias_ui(self):
        self.alias_listbox = tk.Listbox(self.tab2, width=40, height=10)
        self.alias_listbox.grid(row=0, column=0, columnspan=2, padx=20, pady=20)

        ttk.Button(self.tab2, text="Edit", command=self.edit_alias).grid(row=1, column=0, padx=10, pady=10)
        ttk.Button(self.tab2, text="Delete", command=self.delete_alias).grid(row=1, column=1, padx=10, pady=10)

        self.load_aliases()

    def create_backup_ui(self):
        ttk.Button(self.tab3, text="Backup", command=self.manual_backup).pack(pady=20)

    def create_restore_ui(self):
        ttk.Label(self.tab4, text="Backup Versions:").pack(padx=20, pady=10)

        self.restore_listbox = tk.Listbox(self.tab4, width=50, height=10)
        self.restore_listbox.pack(padx=20, pady=10)

        ttk.Button(self.tab4, text="Restore", command=self.restore_backup).pack(padx=20, pady=20)

        self.load_backup_versions()

    def add_alias(self):
        alias = self.alias_entry.get()
        command = self.command_text.get(1.0, tk.END).strip()

        if not alias or not command:
            messagebox.showerror("Error", "Both fields are required!")
            return

        with open(BASH_PROFILE_PATH, "a") as file:
            file.write(f"alias {alias}='{command}'\n")

        self.alias_entry.delete(0, tk.END)
        self.command_text.delete(1.0, tk.END)
        self.create_backup(f".{alias}")
        self.load_aliases()

    def load_aliases(self):
        self.alias_listbox.delete(0, tk.END)
        try:
            with open(BASH_PROFILE_PATH, 'r') as file:
                lines = file.readlines()
            for line in lines:
                if line.startswith('alias '):
                    self.alias_listbox.insert(tk.END, line.strip())
        except FileNotFoundError:
            pass

    def edit_alias(self):
        selected_alias = self.alias_listbox.get(tk.ACTIVE)
        if not selected_alias:
            return
        alias_name = selected_alias.split('=')[0][6:]
        new_command = simpledialog.askstring("Edit Alias", f"Enter new command for alias {alias_name}:")
        if new_command:
            with open(BASH_PROFILE_PATH, 'r') as file:
                content = file.readlines()
            with open(BASH_PROFILE_PATH, 'w') as file:
                for line in content:
                    if line.startswith(f'alias {alias_name}='):
                        file.write(f'alias {alias_name}="{new_command}"\n')
                    else:
                        file.write(line)
            self.load_aliases()

    def delete_alias(self):
        selected_alias = self.alias_listbox.get(tk.ACTIVE)
        if not selected_alias:
            return
        alias_name = selected_alias.split('=')[0][6:]
        if messagebox.askyesno("Delete Alias", f"Do you really want to delete alias {alias_name}?"):
            with open(BASH_PROFILE_PATH, 'r') as file:
                content = file.readlines()
            with open(BASH_PROFILE_PATH, 'w') as file:
                for line in content:
                    if not line.startswith(f'alias {alias_name}='):
                        file.write(line)
            self.load_aliases()

    def manual_backup(self):
        backup_name = ".backupversion"
        self.create_backup(backup_name)
        self.load_backup_versions()

    def load_backup_versions(self):
        self.restore_listbox.delete(0, tk.END)
        for file in os.listdir(os.path.expanduser("~")):
            if file.startswith(".bash_profile.backup"):
                self.restore_listbox.insert(tk.END, file)

    def restore_backup(self):
        selected_backup = self.restore_listbox.get(tk.ACTIVE)
        if not selected_backup:
            return
        backup_path = os.path.expanduser(f"~/{selected_backup}")
        with open(backup_path, 'r') as backup_file:
            content = backup_file.read()
        with open(BASH_PROFILE_PATH, 'w') as bash_file:
            bash_file.write(content)

    def create_backup(self, suffix):
        with open(BASH_PROFILE_PATH, 'r') as bash_file:
            content = bash_file.read()
        backup_name = f"{BASH_PROFILE_PATH}.backup{suffix}"
        with open(backup_name, 'w') as backup_file:
            backup_file.write(content)

if __name__ == "__main__":
    app = AliasApp()
    app.mainloop()
