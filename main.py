import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import imagehash
from PIL import Image

class Item:
    def __init__(self, item_type, description, brand, model, color, serial_number, id_number, amount, mobile_number, image_path, name, phone_number):
        self.item_type = item_type
        self.description = description
        self.brand = brand
        self.model = model
        self.color = color
        self.serial_number = serial_number
        self.id_number = id_number
        self.amount = amount
        self.mobile_number = mobile_number
        self.image_path = image_path
        self.name = name
        self.phone_number = phone_number

class LostAndFoundApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Lost and Found Management System")

        self.lost_items = []
        self.found_items = []

        # Setup Tabs
        self.tab_control = ttk.Notebook(root)
        self.lost_tab = ttk.Frame(self.tab_control)
        self.found_tab = ttk.Frame(self.tab_control)
        self.match_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.lost_tab, text='Report Lost Item')
        self.tab_control.add(self.found_tab, text='Report Found Item')
        self.tab_control.add(self.match_tab, text='Find Matches')
        self.tab_control.pack(expand=1, fill='both')

        # Lost Item Form
        self.lost_frame = ttk.Frame(self.lost_tab)
        self.lost_frame.pack(padx=10, pady=10)

        ttk.Label(self.lost_frame, text="Name:").grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        self.lost_name_entry = ttk.Entry(self.lost_frame, width=30)
        self.lost_name_entry.grid(column=1, row=0, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.lost_frame, text="Phone Number:").grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
        self.lost_phone_number_entry = ttk.Entry(self.lost_frame, width=30)
        self.lost_phone_number_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.lost_frame, text="Item Type:").grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
        self.lost_item_type_var = tk.StringVar()
        self.lost_item_type_combobox = ttk.Combobox(self.lost_frame, textvariable=self.lost_item_type_var, values=("Laptop", "Phone", "Wallet", "Student ID"))
        self.lost_item_type_combobox.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)
        self.lost_item_type_combobox.bind("<<ComboboxSelected>>", self.update_lost_brand_model_options)

        ttk.Label(self.lost_frame, text="Brand:").grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
        self.lost_brand_var = tk.StringVar()
        self.lost_brand_combobox = ttk.Combobox(self.lost_frame, textvariable=self.lost_brand_var)
        self.lost_brand_combobox.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)
        self.lost_brand_combobox.bind("<<ComboboxSelected>>", self.update_lost_model_options)

        ttk.Label(self.lost_frame, text="Model:").grid(column=0, row=4, padx=10, pady=10, sticky=tk.W)
        self.lost_model_var = tk.StringVar()
        self.lost_model_combobox = ttk.Combobox(self.lost_frame, textvariable=self.lost_model_var)
        self.lost_model_combobox.grid(column=1, row=4, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.lost_frame, text="Color:").grid(column=0, row=5, padx=10, pady=10, sticky=tk.W)
        self.lost_color_var = tk.StringVar()
        self.lost_color_combobox = ttk.Combobox(self.lost_frame, textvariable=self.lost_color_var, values=("Black", "White", "Blue", "Red", "Green", "Yellow", "Pink", "Orange", "Purple"))
        self.lost_color_combobox.grid(column=1, row=5, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.lost_frame, text="Description:").grid(column=0, row=6, padx=10, pady=10, sticky=tk.W)
        self.lost_description_entry = ttk.Entry(self.lost_frame, width=30)
        self.lost_description_entry.grid(column=1, row=6, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.lost_frame, text="Serial Number:").grid(column=0, row=7, padx=10, pady=10, sticky=tk.W)
        self.lost_serial_number_entry = ttk.Entry(self.lost_frame, width=30)
        self.lost_serial_number_entry.grid(column=1, row=7, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.lost_frame, text="ID Number (for student IDs):").grid(column=0, row=8, padx=10, pady=10, sticky=tk.W)
        self.lost_id_number_entry = ttk.Entry(self.lost_frame, width=30)
        self.lost_id_number_entry.grid(column=1, row=8, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.lost_frame, text="Amount (for cash):").grid(column=0, row=9, padx=10, pady=10, sticky=tk.W)
        self.lost_amount_entry = ttk.Entry(self.lost_frame, width=30)
        self.lost_amount_entry.grid(column=1, row=9, padx=10, pady=10, sticky=tk.W)
        self.lost_amount_entry.grid_remove()  # Initially hidden

        ttk.Label(self.lost_frame, text="Mobile Number:").grid(column=0, row=10, padx=10, pady=10, sticky=tk.W)
        self.lost_mobile_number_entry = ttk.Entry(self.lost_frame, width=30)
        self.lost_mobile_number_entry.grid(column=1, row=10, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.lost_frame, text="Image:").grid(column=0, row=11, padx=10, pady=10, sticky=tk.W)
        self.lost_image_path_var = tk.StringVar()
        self.lost_image_label = ttk.Label(self.lost_frame, textvariable=self.lost_image_path_var)
        self.lost_image_label.grid(column=1, row=11, padx=10, pady=10, sticky=tk.W)
        self.lost_upload_button = ttk.Button(self.lost_frame, text="Upload Image", command=self.upload_lost_image)
        self.lost_upload_button.grid(column=2, row=11, padx=10, pady=10)

        self.lost_reset_image_button = ttk.Button(self.lost_frame, text="Reset Image", command=self.reset_lost_image)
        self.lost_reset_image_button.grid(column=3, row=11, padx=10, pady=10)

        self.lost_submit_button = ttk.Button(self.lost_frame, text="Report Lost Item", command=self.report_lost_item)
        self.lost_submit_button.grid(column=0, row=12, padx=10, pady=10)

        # Found Item Form
        self.found_frame = ttk.Frame(self.found_tab)
        self.found_frame.pack(padx=10, pady=10)

        ttk.Label(self.found_frame, text="Name:").grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
        self.found_name_entry = ttk.Entry(self.found_frame, width=30)
        self.found_name_entry.grid(column=1, row=0, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.found_frame, text="Phone Number:").grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
        self.found_phone_number_entry = ttk.Entry(self.found_frame, width=30)
        self.found_phone_number_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.found_frame, text="Item Type:").grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
        self.found_item_type_var = tk.StringVar()
        self.found_item_type_combobox = ttk.Combobox(self.found_frame, textvariable=self.found_item_type_var, values=("Laptop", "Phone", "Wallet", "Student ID"))
        self.found_item_type_combobox.grid(column=1, row=2, padx=10, pady=10, sticky=tk.W)
        self.found_item_type_combobox.bind("<<ComboboxSelected>>", self.update_found_brand_model_options)

        ttk.Label(self.found_frame, text="Brand:").grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
        self.found_brand_var = tk.StringVar()
        self.found_brand_combobox = ttk.Combobox(self.found_frame, textvariable=self.found_brand_var)
        self.found_brand_combobox.grid(column=1, row=3, padx=10, pady=10, sticky=tk.W)
        self.found_brand_combobox.bind("<<ComboboxSelected>>", self.update_found_model_options)

        ttk.Label(self.found_frame, text="Model:").grid(column=0, row=4, padx=10, pady=10, sticky=tk.W)
        self.found_model_var = tk.StringVar()
        self.found_model_combobox = ttk.Combobox(self.found_frame, textvariable=self.found_model_var)
        self.found_model_combobox.grid(column=1, row=4, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.found_frame, text="Color:").grid(column=0, row=5, padx=10, pady=10, sticky=tk.W)
        self.found_color_var = tk.StringVar()
        self.found_color_combobox = ttk.Combobox(self.found_frame, textvariable=self.found_color_var, values=("Black", "White", "Blue", "Red", "Green", "Yellow", "Pink", "Orange", "Purple"))
        self.found_color_combobox.grid(column=1, row=5, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.found_frame, text="Description:").grid(column=0, row=6, padx=10, pady=10, sticky=tk.W)
        self.found_description_entry = ttk.Entry(self.found_frame, width=30)
        self.found_description_entry.grid(column=1, row=6, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.found_frame, text="Serial Number:").grid(column=0, row=7, padx=10, pady=10, sticky=tk.W)
        self.found_serial_number_entry = ttk.Entry(self.found_frame, width=30)
        self.found_serial_number_entry.grid(column=1, row=7, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.found_frame, text="ID Number (for student IDs):").grid(column=0, row=8, padx=10, pady=10, sticky=tk.W)
        self.found_id_number_entry = ttk.Entry(self.found_frame, width=30)
        self.found_id_number_entry.grid(column=1, row=8, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.found_frame, text="Amount (for cash):").grid(column=0, row=9, padx=10, pady=10, sticky=tk.W)
        self.found_amount_entry = ttk.Entry(self.found_frame, width=30)
        self.found_amount_entry.grid(column=1, row=9, padx=10, pady=10, sticky=tk.W)
        self.found_amount_entry.grid_remove()  # Initially hidden

        ttk.Label(self.found_frame, text="Mobile Number:").grid(column=0, row=10, padx=10, pady=10, sticky=tk.W)
        self.found_mobile_number_entry = ttk.Entry(self.found_frame, width=30)
        self.found_mobile_number_entry.grid(column=1, row=10, padx=10, pady=10, sticky=tk.W)

        ttk.Label(self.found_frame, text="Image:").grid(column=0, row=11, padx=10, pady=10, sticky=tk.W)
        self.found_image_path_var = tk.StringVar()
        self.found_image_label = ttk.Label(self.found_frame, textvariable=self.found_image_path_var)
        self.found_image_label.grid(column=1, row=11, padx=10, pady=10, sticky=tk.W)
        self.found_upload_button = ttk.Button(self.found_frame, text="Upload Image", command=self.upload_found_image)
        self.found_upload_button.grid(column=2, row=11, padx=10, pady=10)

        self.found_reset_image_button = ttk.Button(self.found_frame, text="Reset Image", command=self.reset_found_image)
        self.found_reset_image_button.grid(column=3, row=11, padx=10, pady=10)

        self.found_submit_button = ttk.Button(self.found_frame, text="Report Found Item", command=self.report_found_item)
        self.found_submit_button.grid(column=0, row=12, padx=10, pady=10)

        # Match Tab
        self.match_frame = ttk.Frame(self.match_tab)
        self.match_frame.pack(padx=10, pady=10)

        self.match_button = ttk.Button(self.match_frame, text="Search Matches", command=self.search_matches)
        self.match_button.pack(padx=10, pady=10)

        self.reset_button = ttk.Button(self.match_frame, text="Reset Fields", command=self.reset_fields)
        self.reset_button.pack(padx=10, pady=10)

    def update_lost_brand_model_options(self, event):
        item_type = self.lost_item_type_var.get()
        brands = {
            "Laptop": ["Apple", "Dell", "HP"],
            "Phone": ["Apple", "Samsung", "Google"],
            "Wallet": [],
            "Student ID": []
        }
        self.lost_brand_combobox['values'] = brands.get(item_type, [])
        self.lost_brand_combobox.set('')
        self.update_lost_model_options(event)

    def update_found_brand_model_options(self, event):
        item_type = self.found_item_type_var.get()
        brands = {
            "Laptop": ["Apple", "Dell", "HP"],
            "Phone": ["Apple", "Samsung", "Google"],
            "Wallet": [],
            "Student ID": []
        }
        self.found_brand_combobox['values'] = brands.get(item_type, [])
        self.found_brand_combobox.set('')
        self.update_found_model_options(event)

    def update_lost_model_options(self, event):
        brand = self.lost_brand_var.get()
        models = {
            "Apple": ["MacBook Pro", "iPhone X"],
            "Dell": ["XPS 13"],
            "HP": ["Spectre x360"],
            "Samsung": ["Galaxy S10"],
            "Google": ["Pixel 4"]
        }
        self.lost_model_combobox['values'] = models.get(brand, [])
        self.lost_model_combobox.set('')

    def update_found_model_options(self, event):
        brand = self.found_brand_var.get()
        models = {
            "Apple": ["MacBook Pro", "iPhone X"],
            "Dell": ["XPS 13"],
            "HP": ["Spectre x360"],
            "Samsung": ["Galaxy S10"],
            "Google": ["Pixel 4"]
        }
        self.found_model_combobox['values'] = models.get(brand, [])
        self.found_model_combobox.set('')

    def upload_lost_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.lost_image_path_var.set(file_path)

    def reset_lost_image(self):
        self.lost_image_path_var.set("")

    def upload_found_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.found_image_path_var.set(file_path)

    def reset_found_image(self):
        self.found_image_path_var.set("")

    def report_lost_item(self):
        name = self.lost_name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        item_type = self.lost_item_type_var.get()
        description = self.lost_description_entry.get()
        brand = self.lost_brand_var.get()
        model = self.lost_model_var.get()
        color = self.lost_color_var.get()
        serial_number = self.lost_serial_number_entry.get()
        id_number = self.lost_id_number_entry.get()
        amount = self.lost_amount_entry.get()
        mobile_number = self.lost_mobile_number_entry.get()
        image_path = self.lost_image_path_var.get()
        phone_number = self.lost_phone_number_entry.get()

        lost_item = Item(item_type, description, brand, model, color, serial_number, id_number, amount, mobile_number, image_path, name, phone_number)
        self.lost_items.append(lost_item)
        messagebox.showinfo("Success", "Lost item reported successfully!")

    def report_found_item(self):
        name = self.found_name_entry.get()
        if not name:
            messagebox.showerror("Error", "Name is required!")
            return

        item_type = self.found_item_type_var.get()
        description = self.found_description_entry.get()
        brand = self.found_brand_var.get()
        model = self.found_model_var.get()
        color = self.found_color_var.get()
        serial_number = self.found_serial_number_entry.get()
        id_number = self.found_id_number_entry.get()
        amount = self.found_amount_entry.get()
        mobile_number = self.found_mobile_number_entry.get()
        image_path = self.found_image_path_var.get()
        phone_number = self.found_phone_number_entry.get()

        found_item = Item(item_type, description, brand, model, color, serial_number, id_number, amount, mobile_number, image_path, name, phone_number)
        self.found_items.append(found_item)
        messagebox.showinfo("Success", "Found item reported successfully!")

    def search_matches(self):
        matches = []
        for lost_item in self.lost_items:
            for found_item in self.found_items:
                if (
                    lost_item.item_type == found_item.item_type and
                    (lost_item.brand == found_item.brand or not lost_item.brand or not found_item.brand) and
                    (lost_item.model == found_item.model or not lost_item.model or not found_item.model) and
                    (lost_item.color == found_item.color or not lost_item.color or not found_item.color) and
                    (lost_item.serial_number == found_item.serial_number or not lost_item.serial_number or not found_item.serial_number) and
                    (lost_item.id_number == found_item.id_number or not lost_item.id_number or not found_item.id_number) and
                    (lost_item.amount == found_item.amount or not lost_item.amount or not found_item.amount) and
                    (lost_item.mobile_number == found_item.mobile_number or not lost_item.mobile_number or not found_item.mobile_number)
                ):
                    if lost_item.image_path and found_item.image_path:
                        lost_image = Image.open(lost_item.image_path)
                        found_image = Image.open(found_item.image_path)
                        if imagehash.average_hash(lost_image) - imagehash.average_hash(found_image) < 10:
                            matches.append((lost_item, found_item))
                    else:
                        matches.append((lost_item, found_item))

        if matches:
            match_text = ""
            for lost_item, found_item in matches:
                match_text += f"Lost Item: {lost_item.item_type}, Name: {lost_item.name}, Phone Number: {lost_item.phone_number}\n"
                match_text += f"Found Item: {found_item.item_type}, Name: {found_item.name}, Phone Number: {found_item.phone_number}\n\n"
            messagebox.showinfo("Matches Found", match_text)
        else:
            messagebox.showinfo("No Matches Found", "No matches found for the reported items.")

    def reset_fields(self):
        for widget in self.lost_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
        self.lost_image_path_var.set("")

        for widget in self.found_frame.winfo_children():
            if isinstance(widget, ttk.Entry):
                widget.delete(0, tk.END)
            elif isinstance(widget, ttk.Combobox):
                widget.set('')
        self.found_image_path_var.set("")

if __name__ == "__main__":
    root = tk.Tk()
    app = LostAndFoundApp(root)
    root.mainloop()
