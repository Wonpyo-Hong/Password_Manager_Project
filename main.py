import tkinter  # tkinter is imported to use its GUI capabilities for creating windows and handling events.
from tkinter import *  # This imports all names from the tkinter module into the global namespace, allowing easy access to tkinter's functions and classes without prefixing them with 'tkinter.'.
from tkinter import messagebox  # Importing messagebox specifically for showing dialog boxes for warnings, errors, etc.
import random  # The random module is imported for generating random numbers, which are essential for creating random passwords.
import json  # The json module is used for reading from and writing to a JSON file, which stores the website, email, and password data.

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def make_random_password():
    # Defines lists of characters to be used in the password.
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    
    # Determines how many of each type of character to include in the password.
    nr_letters = random.randint(8, 10)  # Randomly choosing the number of letters between 8 and 10.
    nr_symbols = random.randint(2, 4)  # Randomly choosing the number of symbols between 2 and 4.
    nr_numbers = random.randint(2, 4)  # Randomly choosing the number of numbers between 2 and 4.

    # Randomly picking the determined number of characters from each list.
    letter_pick = random.sample(letters, nr_letters)  # Randomly selecting letters.
    symbol_pick = random.sample(symbols, nr_symbols)  # Randomly selecting symbols.
    number_pick = random.sample(numbers, nr_numbers)  # Randomly selecting numbers.

    # Combining all the randomly picked characters into a single list.
    pw_list = letter_pick + symbol_pick + number_pick

    # Shuffling the combined list to ensure the password's randomness.
    random.shuffle(pw_list)
    # Joining the shuffled list into a string to form the final password.
    password = ''.join(s for s in pw_list)

    # Inserting the generated password into the password entry field in the GUI.
    pw_entry.insert(0, password)

# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    # Retrieving user input from the GUI.
    web_info = website_entry.get()  # Gets the website name from the entry field.
    email_info = email_entry.get()  # Gets the email from the entry field.
    pw_info = pw_entry.get()  # Gets the password from the entry field.
    # Structuring the data to be saved in JSON format.
    new_data = {
        web_info: {
            "email": email_info,
            "password": pw_info
        }
    }

    # Checking if any of the essential fields are empty before proceeding to save.
    if not web_info or not pw_info:
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty")  # Shows a warning if any field is empty.
    else:
        try:
            with open('data.json', 'r') as info:  # Tries to open an existing data.json file in read mode.
                data = json.load(info)  # Loads the existing data into a variable if the file exists.
        except FileNotFoundError:  # Handles the case where the data.json file does not exist.
            with open('data.json', 'w') as info:  # Creates a new data.json file in write mode.
                json.dump(new_data, info, indent=4)  # Saves the new data into the newly created file.
        else:  # If the file exists and is successfully opened,
            data.update(new_data)  # Updates the existing data with the new data.

            with open('data.json', 'w') as info:  # Opens the data.json file again in write mode to save the updated data.
                json.dump(data, info, indent=4)  # Saves the updated data into the file.
        finally:  # This block executes no matter what happens above, ensuring the GUI fields are cleared after operation.
            website_entry.delete(0, END)  # Clears the website entry field.
            email_entry.delete(0, END)  # Clears the email entry field.
            pw_entry.delete(0, END)  # Clears the password entry field.

# ---------------------------- FIND PASSWORD ------------------------------- #

def find_password():
    web_info = website_entry.get()  # Gets the website name from the entry field for searching.

    try:
        with open('data.json', 'r') as data_file:  # Tries to open the data.json file in read mode.
            data = json.load(data_file)  # Loads the data from the file if it exists.
    except FileNotFoundError:  # Handles the case where the data.json file does not exist.
        messagebox.showinfo(title="Error", message="No Data File Found")  # Shows an info message indicating the file is missing.
    else:
        if data.get(web_info):  # Checks if the entered website exists in the data.
            # Displays the found login information for the website.
            messagebox.showinfo(title=f"{web_info}",
                                message=f"Email: {data[web_info]['email']} \nPassword: {data[web_info]['password']}")
        else:  # If the website does not exist in the data,
            messagebox.showinfo(title="Error", message=f"No details for {web_info} exists")  # Shows an error message indicating the website was not found.

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()  # Creates the main window using Tkinter.
window.title("Password Manager")  # Sets the title of the window.
window.config(padx=50, pady=50)  # Configures the padding of the window.

canvas = Canvas(window, width=200, height=200, highlightthickness=0)  # Creates a canvas for drawing, e.g., for the logo image.
logo_img = tkinter.PhotoImage(file='logo.png')  # Loads the logo image.
canvas.create_image(100, 100, image=logo_img)  # Places the logo image on the canvas.
canvas.grid(column=1, row=0)  # Positions the canvas in the grid layout of the window.

# Labels, entry fields, and buttons are set up below with specific grid positions, allowing for a structured layout of the UI.

# Website information entry
website_label = Label(text="Website: ")
website_label.grid(column=0, row=1)

website_entry = Entry(width=21)
website_entry.grid(column=1, row=1)
website_entry.focus()  # Sets focus to this entry field when the program starts.

# Email information entry
email_label = Label(text="Email: ")
email_label.grid(column=0, row=2)

email_entry = Entry(width=35)
email_entry.insert(0, string="example@gmail.com")  # Pre-fills the email entry with a default email.
email_entry.grid(column=1, row=2, columnspan=2)

# Password information entry
pw_label = Label(text="Password: ")
pw_label.grid(column=0, row=3)

pw_entry = Entry(width=21)
pw_entry.grid(column=1, row=3)

# Buttons for generating a password, adding the information to the file, and searching for a password.
gp_button = Button(text="Generate Password", command=make_random_password)  # This button triggers the password generation.
gp_button.grid(column=2, row=3)

add_button = Button(text="Add", fg="blue", width=36, command=save)  # This button triggers saving the entered data to the file.
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(window, text="Search", fg="green", width=15, command=find_password)  # This button triggers the search functionality.
search_button.grid(column=2, row=1)

window.mainloop()  # Starts the Tkinter event loop, making the window responsive and interactive.
