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