from tkinter import *
from tkinter import filedialog
from tkinter import ttk
import json
from PIL import Image, ImageTk, ExifTags


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
root = Tk()
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
        name_entry.delete(0, END)
        number_entry.delete(0, END)
        email_entry.delete(0, END)
        org_entry.delete(0, END)
    else:
        print("Name and number are required.")


# Function to search contacts
def search_contacts():
    search_query = search_entry.get()
    contact_listbox.delete(0, END)

    # Search contacts by the initial letter
    initial_letter = search_query[0].lower()

    if initial_letter in contacts_by_letter:
        current_contact = contacts_by_letter[initial_letter].head
        while current_contact:
            if search_query.lower() in current_contact.name.lower():
                contact_listbox.insert(END, current_contact.name)
            current_contact = current_contact.next


# Function to display all contacts
def display_all_contacts():
    contact_listbox.delete(0, END)

    for initial_letter in contacts_by_letter:
        current_contact = contacts_by_letter[initial_letter].head
        while current_contact:
            contact_listbox.insert(END, current_contact.name)
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
    details_window = Toplevel(root)
    details_window.title("Contact Details")

    details_label = Label(details_window,
                          text=f"Name: {contact.name}\nNumber: {contact.number}\nEmail: {contact.email}\nOrganization: {contact.org}")
    details_label.pack()


def delete_contact():
    selection = contact_listbox.curselection()
    if selection:
        selected_contact_name = contact_listbox.get(selection[0])

        # Find the contact in the dictionary and delete it
        for initial_letter in contacts_by_letter:
            current_contact = contacts_by_letter[initial_letter].head
            prev_contact = None
            while current_contact:
                if selected_contact_name == current_contact.name:
                    # Remove the contact from the linked list
                    if prev_contact:
                        prev_contact.next = current_contact.next
                    else:
                        contacts_by_letter[initial_letter].head = current_contact.next

                    # Serialize and save the updated contacts list to "contacts.json"
                    with open("contacts.json", "w") as file:
                        contacts_data = []
                        for letter in contacts_by_letter:
                            current_contact = contacts_by_letter[letter].head
                            while current_contact:
                                contacts_data.append(vars(current_contact))
                                current_contact = current_contact.next
                        json.dump(contacts_data, file)

                    # Update the listbox
                    contact_listbox.delete(selection[0])
                    break
                prev_contact = current_contact
                current_contact = current_contact.next


name_label = Label(root, text="Name:", pady=5)
name_entry = Entry(root, width=27)
number_label = Label(root, text="Number:", pady=5)
number_entry = Entry(root, width=27)
email_label = Label(root, text="Email:", pady=5)
email_entry = Entry(root, width=27)
org_label = Label(root, text="Organization:", pady=5)
org_entry = Entry(root, width=27)
contact_listbox = Listbox(root)
search_entry = Entry(root)

name_label.grid(row=0, column=0, padx=10, pady=7, sticky='w')
name_entry.grid(row=0, column=1, padx=10, pady=10)
number_label.grid(row=1, column=0, padx=10, pady=7, sticky='w')
number_entry.grid(row=1, column=1, padx=10, pady=10)
email_label.grid(row=2, column=0, padx=10, pady=7, sticky='w')
email_entry.grid(row=2, column=1, padx=10, pady=10)
org_label.grid(row=3, column=0, padx=10, pady=7, sticky='w')
org_entry.grid(row=3, column=1, padx=10, pady=10)
contact_listbox.grid(row=5, column=0,pady=10, padx=(10, 10),  columnspan=2, sticky="nsew",)
search_entry.grid(row=6, column=0, padx=(10,10), pady=10, sticky='e')
delete_button = Button(root, text="Delete", command=delete_contact)
delete_button.grid(row=5, column=1)

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

root.geometry('330x590')
root.title("Contact List")
root.attributes('-alpha', 0.95)
root.resizable(False, False)

# CREATING UI FOR SAVE CONTACTS
button_save_inactive = Image.open(
    'design\\save_button_nohover.png')
button_save_inactive_nohover = ImageTk.PhotoImage(button_save_inactive)

button_save_active = Image.open(
    'design\\save_button_hover.png')
button_save_active_hover = ImageTk.PhotoImage(button_save_active)

button_save_click = Image.open(
    'design\\save_button_clicked.png')
button_save_onclick = ImageTk.PhotoImage(button_save_click)

save_button = Button(root, text="Save", command=add_contact, image=button_save_inactive_nohover, bd=0, relief="sunken",
                     pady=10)
save_button.grid(row=4, column=0, columnspan=2)


def save_on_hover(event):
    save_button.config(image=button_save_active_hover)


def save_on_leave(event):
    save_button.config(image=button_save_inactive_nohover)


def save_on_click(event):
    # Change the image or perform any action you want on button click
    save_button.config(image=button_save_onclick)


save_button.bind("<Enter>", save_on_hover)
save_button.bind("<Leave>", save_on_leave)
save_button.bind("<Button-1>", save_on_click)

# SAVE BUTTON UI
button_search_inactive = Image.open(
    'design\\search_button_nohover.png')
button_search_inactive_nohover = ImageTk.PhotoImage(button_search_inactive)

button_search_active = Image.open(
    'design\\search_button_hover.png')
button_search_active_hover = ImageTk.PhotoImage(button_search_active)

button_search_click = Image.open(
    'design\\search_button_clicked.png')
button_search_onclick = ImageTk.PhotoImage(button_search_click)

search_button = Button(root, text="Save", command=search_contacts, image=button_search_inactive_nohover, bd=0,
                       relief="sunken", pady=10)
search_button.grid(row=6, column=1, )


def search_on_hover(event):
    search_button.config(image=button_search_active_hover)


def search_on_leave(event):
    search_button.config(image=button_search_inactive_nohover)


def search_on_click(event):
    # Change the image or perform any action you want on button click
    search_button.config(image=button_search_onclick)


search_button.bind("<Enter>", search_on_hover)
search_button.bind("<Leave>", search_on_leave)
search_button.bind("<Button-1>", search_on_click)

# SHOW ALL BUTTON UI

button_all_inactive = Image.open(
    'design\\all_button_nohover.png')
button_all_inactive_nohover = ImageTk.PhotoImage(button_all_inactive)

button_all_active = Image.open(
    'design\\all_button_hover.png')
button_all_active_hover = ImageTk.PhotoImage(button_all_active)

button_all_click = Image.open(
    'design\\all_button_clicked.png')
button_all_onclick = ImageTk.PhotoImage(button_all_click)

display_all_button = Button(root, text="Display All Contacts", command=display_all_contacts,
                            image=button_all_inactive_nohover, bd=0,
                            relief="sunken", pady=10)
display_all_button.grid(row=7, column=0, columnspan=2, pady=(10, 0), padx=(0, 0))


def all_on_hover(event):
    display_all_button.config(image=button_all_active_hover)


def all_on_leave(event):
    display_all_button.config(image=button_all_inactive_nohover)


def all_on_click(event):
    # Change the image or perform any action you want on button click
    display_all_button.config(image=button_all_onclick)


display_all_button.bind("<Enter>", all_on_hover)
display_all_button.bind("<Leave>", all_on_leave)
display_all_button.bind("<Button-1>", all_on_click)

style = ttk.Style()
style.configure("TButton", relief="sunken")

root.mainloop()
