import tkinter as tk
import json


class Contact:
    def __init__(self, name, number, email, org):
        self.name = name
        self.number = number
        self.email = email
        self.org = org
        self.next = None


class ContactList:
    def __init__(self):
        self.head = None

    def add_contact(self, contact):
        if not self.head:
            self.head = contact
        else:
            current_contact = self.head
            while current_contact.next:
                current_contact = current_contact.next
            current_contact.next = contact


# Initialize a dictionary to store contacts by the first letter of their names
contacts_by_letter = {}

# Initialize the tkinter app
root = tk.Tk()
root.title("Contact Book")


# Function to add contacts
def add_contact():
    name = name_entry.get()
    number = number_entry.get()
    email = email_entry.get()
    org = org_entry.get()

    if name and number:
        contact = Contact(name, number, email, org)
        initial_letter = name[0].lower()

        if initial_letter not in contacts_by_letter:
            contacts_by_letter[initial_letter] = ContactList()

        contacts_by_letter[initial_letter].add_contact(contact)

        # Serialize and save the updated contacts list to "contacts.json"
        with open("contacts.json", "w") as file:
            contacts_data = []
            for letter in contacts_by_letter:
                current_contact = contacts_by_letter[letter].head
                while current_contact:
                    contacts_data.append(vars(current_contact))
                    current_contact = current_contact.next
            json.dump(contacts_data, file)

        # Clear input fields
        name_entry.delete(0, tk.END)
        number_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
        org_entry.delete(0, tk.END)
    else:
        print("Name and number are required.")


# Function to search contacts
def search_contacts():
    search_query = search_entry.get()
    contact_listbox.delete(0, tk.END)

    # Search contacts by the initial letter
    initial_letter = search_query[0].lower()

    if initial_letter in contacts_by_letter:
        current_contact = contacts_by_letter[initial_letter].head
        while current_contact:
            if search_query.lower() in current_contact.name.lower():
                contact_listbox.insert(tk.END, current_contact.name)
            current_contact = current_contact.next


# Function to display all contacts
def display_all_contacts():
    contact_listbox.delete(0, tk.END)

    for initial_letter in contacts_by_letter:
        current_contact = contacts_by_letter[initial_letter].head
        while current_contact:
            contact_listbox.insert(tk.END, current_contact.name)
            current_contact = current_contact.next


# Function to display contacts
def display_contacts(event):
    selection = contact_listbox.curselection()
    if selection:
        selected_contact_name = contact_listbox.get(selection[0])

        # Find the contact in the dictionary and display its details
        for initial_letter in contacts_by_letter:
            current_contact = contacts_by_letter[initial_letter].head
            while current_contact:
                if selected_contact_name == current_contact.name:
                    display_contact_details(current_contact)
                    break
                current_contact = current_contact.next


# Function to display contact details in a separate window
def display_contact_details(contact):
    details_window = tk.Toplevel(root)
    details_window.title("Contact Details")

    details_label = tk.Label(details_window,
                             text=f"Name: {contact.name}\nNumber: {contact.number}\nEmail: {contact.email}\nOrganization: {contact.org}")
    details_label.pack()


name_label = tk.Label(root, text="Name:")
name_entry = tk.Entry(root)
number_label = tk.Label(root, text="Number:")
number_entry = tk.Entry(root)
email_label = tk.Label(root, text="Email:")
email_entry = tk.Entry(root)
org_label = tk.Label(root, text="Organization:")
org_entry = tk.Entry(root)
save_button = tk.Button(root, text="Save", command=add_contact)
contact_listbox = tk.Listbox(root)
search_entry = tk.Entry(root)
search_button = tk.Button(root, text="Search", command=search_contacts)

name_label.pack()
name_entry.pack()
number_label.pack()
number_entry.pack()
email_label.pack()
email_entry.pack()
org_label.pack()
org_entry.pack()
save_button.pack()
contact_listbox.pack()
search_entry.pack()
search_button.pack()

# Add a button to display all contacts
display_all_button = tk.Button(root, text="Display All Contacts", command=display_all_contacts)
display_all_button.pack()

# Bind the display_contacts function to the listbox selection event
contact_listbox.bind('<<ListboxSelect>>', display_contacts)


# Call load_contacts to load existing contacts when the app starts
def load_contacts():
    try:
        with open("contacts.json", "r") as file:
            contacts_data = json.load(file)
            for data in contacts_data:
                contact = Contact(data['name'], data['number'], data['email'], data['org'])
                initial_letter = contact.name[0].lower()
                if initial_letter not in contacts_by_letter:
                    contacts_by_letter[initial_letter] = ContactList()
                contacts_by_letter[initial_letter].add_contact(contact)
        display_all_contacts()
    except FileNotFoundError:
        pass


load_contacts()

root.mainloop()
