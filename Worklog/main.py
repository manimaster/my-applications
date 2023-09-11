import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
from datetime import datetime

class WorklogApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.title("Manikandan - Worklog")
        self.state('zoomed')  # Maximizes the window

        self.tab_control = ttk.Notebook(self)

        # Tabs
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
        # Additional tabs can be added similarly...

        self.tab_control.add(self.tab1, text='Assigned Tickets')
        self.tab_control.add(self.tab2, text='Ticket Updates')

        # Define methods to create UI components for each tab
        self.create_assigned_tickets_ui()
        self.create_ticket_updates_ui()

        self.tab_control.pack(expand=1, fill='both')

    def create_assigned_tickets_ui(self):
        pass  # Placeholder for the UI components of the first tab

    def create_ticket_updates_ui(self):
        pass  # Placeholder for the UI components of the second tab

    def create_assigned_tickets_ui(self):
        # Section 1: Input fields
        ttk.Label(self.tab1, text="Ticket Number").grid(row=0, column=0, padx=10, pady=10)
        self.ticket_number_entry = ttk.Entry(self.tab1)
        self.ticket_number_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.tab1, text="Ticket Description").grid(row=1, column=0, padx=10, pady=10)
        self.ticket_description_entry = ttk.Entry(self.tab1)
        self.ticket_description_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.tab1, text="Assigned Date (DD-MM-YYYY)").grid(row=2, column=0, padx=10, pady=10)
        self.assigned_date_entry = ttk.Entry(self.tab1)
        self.assigned_date_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Button(self.tab1, text="Create", command=self.create_ticket).grid(row=3, column=0, columnspan=2, pady=20)

        # Section 2: Display assigned tickets
        self.ticket_display = ttk.Treeview(self.tab1, columns=("Ticket Number", "Description", "Status"), show="headings")
        self.ticket_display.heading("Ticket Number", text="Ticket Number")
        self.ticket_display.heading("Description", text="Description")
        self.ticket_display.heading("Status", text="Status")
        self.ticket_display.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.load_tickets()

    def load_tickets(self):
        # Load tickets from JSON file and display in the Treeview
        try:
            with open("tickets.json", "r") as file:
                tickets = json.load(file)
            for ticket in tickets:
                self.ticket_display.insert("", "end", values=(ticket["number"], ticket["description"], ticket["status"]))
        except FileNotFoundError:
            pass

    def create_ticket(self):
        # Collect ticket details and save to JSON file
        ticket_number = self.ticket_number_entry.get()
        description = self.ticket_description_entry.get()
        assigned_date = self.assigned_date_entry.get()
        status = "Created"

        ticket = {
            "number": ticket_number,
            "description": description,
            "date": assigned_date,
            "status": status,
            "updates": []
        }

        # Save ticket to JSON file
        try:
            with open("tickets.json", "r") as file:
                tickets = json.load(file)
        except FileNotFoundError:
            tickets = []

        tickets.append(ticket)

        with open("tickets.json", "w") as file:
            json.dump(tickets, file)

        # Refresh the ticket display
        self.load_tickets()

    def create_ticket_updates_ui(self):
        # Section 1: Table of tickets
        self.update_ticket_display = ttk.Treeview(self.tab2, columns=("Ticket Number", "Description", "Status"), show="headings")
        self.update_ticket_display.heading("Ticket Number", text="Ticket Number")
        self.update_ticket_display.heading("Description", text="Description")
        self.update_ticket_display.heading("Status", text="Status")
        self.update_ticket_display.grid(row=0, column=0, padx=10, pady=10)
        self.update_ticket_display.bind("<Double-1>", self.on_ticket_selected)

        # Section 2: Display updates for a selected ticket
        self.ticket_updates_display = ttk.Treeview(self.tab2, columns=("Date", "Status Change", "Update"), show="headings")
        self.ticket_updates_display.heading("Date", text="Date")
        self.ticket_updates_display.heading("Status Change", text="Status Change")
        self.ticket_updates_display.heading("Update", text="Update")
        self.ticket_updates_display.grid(row=1, column=0, padx=10, pady=10)

        ttk.Button(self.tab2, text="Add an update", command=self.add_update_popup).grid(row=2, column=0, pady=20)

        self.load_ticket_updates()

    def load_ticket_updates(self):
        # Load ticket updates from JSON file and display in the Treeview
        try:
            with open("tickets.json", "r") as file:
                tickets = json.load(file)
            for ticket in tickets:
                self.update_ticket_display.insert("", "end", values=(ticket["number"], ticket["description"], ticket["status"]))
        except FileNotFoundError:
            pass

    def on_ticket_selected(self, event):
        # Display updates for the selected ticket
        self.ticket_updates_display.delete(*self.ticket_updates_display.get_children())
        item = self.update_ticket_display.selection()[0]
        ticket_number = self.update_ticket_display.item(item, "values")[0]

        with open("tickets.json", "r") as file:
            tickets = json.load(file)

        for ticket in tickets:
            if ticket["number"] == ticket_number:
                for update in ticket["updates"]:
                    self.ticket_updates_display.insert("", "end", values=(update["date"], update["status_change"], update["update_text"]))
                break

    def add_update_popup(self):
        # Popup to add a ticket update
        popup = tk.Toplevel(self)
        popup.title("Add Ticket Update")

        ttk.Label(popup, text="Status:").grid(row=0, column=0, padx=10, pady=10)
        status_var = tk.StringVar(value="Created")
        status_options = ["Created", "Paused", "In Progress", "Blocked", "Closed", "Fixed"]
        ttk.Combobox(popup, textvariable=status_var, values=status_options).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(popup, text="Update:").grid(row=1, column=0, padx=10, pady=10)
        update_text = tk.Text(popup, width=30, height=5)
        update_text.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(popup, text="Save Update", command=lambda: self.save_ticket_update(status_var.get(), update_text.get(1.0, tk.END), popup)).grid(row=2, column=0, columnspan=2, pady=20)

    def save_ticket_update(self, status, update_text, popup):
        # Save the ticket update to the JSON file
        item = self.update_ticket_display.selection()[0]
        ticket_number = self.update_ticket_display.item(item, "values")[0]
        current_status = self.update_ticket_display.item(item, "values")[2]

        with open("tickets.json", "r") as file:
            tickets = json.load(file)

        for ticket in tickets:
            if ticket["number"] == ticket_number:
                ticket["status"] = status
                ticket["updates"].append({
                    "date": datetime.now().strftime("%d-%m-%Y"),
                    "status_change": f"{current_status} > {status}",
                    "update_text": update_text.strip()
                })
                break

        with open("tickets.json", "w") as file:
            json.dump(tickets, file)

        popup.destroy()
        self.load_ticket_updates()
        self.on_ticket_selected(None)

if __name__ == "__main__":
    app = WorklogApp()
    app.mainloop()