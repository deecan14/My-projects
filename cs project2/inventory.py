import json


class Item:
    def __init__(self, item_id, name, category, quantity, rental_price, **attributes):
        self.item_id = item_id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.rental_price = rental_price
        self.attributes = attributes

    def update_quantity(self, new_quantity):
        self.quantity = new_quantity

    def get_details(self):
        details = {
            "ID": self.item_id,
            "Name": self.name,
            "Category": self.category,
            "Quantity": self.quantity,
            "Rental Price": self.rental_price,
        }
        details.update(self.attributes)
        return details


class Inventory:
    def __init__(self):
        self.items = {}

    def add_item(self, item):
        self.items[item.item_id] = item
        print(f"Item '{item.name}' added to inventory.")

    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]
            print(f"Item with ID '{item_id}' removed from inventory.")
        else:
            print(f"Item with ID '{item_id}' not found.")

    def get_item(self, item_id):
        return self.items.get(item_id)

    def list_items(self):
        if not self.items:
            print("Inventory is empty.")
        else:
            for item in self.items.values():
                print(item.get_details())

    def update_inventory(self, item_id, new_quantity):
        item = self.get_item(item_id)
        if item:
            item.update_quantity(new_quantity)
            print(f"Item ID {item_id} quantity updated to {new_quantity}.")
        else:
            print(f"Item with ID {item_id} not found.")

    def check_stock(self, threshold=5):
        return [item.get_details() for item in self.items.values() if item.quantity <= threshold]

    def save_to_file(self, filename="inventory.json"):
        data = {item_id: item.get_details() for item_id, item in self.items.items()}
        with open(filename, "w") as file:
            json.dump(data, file)
        print(f"Inventory saved to {filename}.")

    def load_from_file(self, filename="inventory.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for item_id, item_data in data.items():
                    item_id = item_data["ID"]
                    name = item_data["Name"]
                    category = item_data["Category"]
                    quantity = item_data["Quantity"]
                    rental_price = item_data["Rental Price"]
                    additional_attributes = {k: v for k, v in item_data.items()
                                             if k not in ["ID", "Name", "Category", "Quantity", "Rental Price"]}
                    self.items[item_id] = Item(item_id, name, category, quantity, rental_price, **additional_attributes)
            print(f"Inventory loaded from {filename}.")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")


class Report:
    def __init__(self, inventory):
        self.inventory = inventory

    def low_stock_report(self, threshold=5):
        low_stock_items = self.inventory.check_stock(threshold)
        return low_stock_items if low_stock_items else "All items are sufficiently stocked."

    def expiry_report(self):
        expiring_items = [item.get_details() for item in self.inventory.items.values()
                          if 'expiration_date' in item.attributes and
                          item.attributes['expiration_date'] < "2024-12-31"]
        return expiring_items if expiring_items else "No items nearing expiration."

    def sales_report(self):
        return "Sales report is not yet implemented."

    def generate_report(self, report_type, *args):
        if report_type == "low_stock":
            return self.low_stock_report(*args)
        elif report_type == "expiry":
            return self.expiry_report()
        elif report_type == "sales":
            return self.sales_report()
        else:
            return "Invalid report type."


class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role
        self.permissions = {
            "admin": ["add_item", "remove_item", "update_inventory", "generate_report"],
            "manager": ["add_item", "update_inventory", "generate_report"],
        }

    def get_permissions(self):
        return self.permissions.get(self.role, [])

    def perform_inventory_actions(self, action, inventory, *args):
        if action in self.get_permissions():
            if hasattr(inventory, action):
                return getattr(inventory, action)(*args)
            else:
                return f"Action {action} not found in inventory."
        return f"Permission denied for {self.role}."


def menu():
    inventory = Inventory()
    inventory.load_from_file()

    print("Welcome to the Inventory Management System")
    username = input("Enter your username: ")
    role = input("Enter your role (admin/manager): ")
    user = User(username, role)

    while True:
        print("\nMenu:")
        print("1. Add Item")
        print("2. Remove Item")
        print("3. Update Item Quantity")
        print("4. List Items")
        print("5. Generate Report (low stock/expiry)")
        print("6. Save Inventory")
        print("7. Load Inventory")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            item_id = int(input("Enter Item ID: "))
            name = input("Enter Item Name: ")
            category = input("Enter Item Category: ")
            quantity = int(input("Enter Item Quantity: "))
            rental_price = float(input("Enter Rental Price: "))
            item = Item(item_id, name, category, quantity, rental_price)
            print(user.perform_inventory_actions("add_item", inventory, item))

        elif choice == "2":
            item_id = int(input("Enter Item ID to remove: "))
            print(user.perform_inventory_actions("remove_item", inventory, item_id))

        elif choice == "3":
            item_id = int(input("Enter Item ID to update: "))
            new_quantity = int(input("Enter new quantity: "))
            print(user.perform_inventory_actions("update_inventory", inventory, item_id, new_quantity))

        elif choice == "4":
            inventory.list_items()

        elif choice == "5":
            report_type = input("Enter report type (low_stock/expiry): ")
            if report_type == "low_stock":
                threshold = int(input("Enter stock threshold: "))
                report = Report(inventory)
                print(report.generate_report("low_stock", threshold))
            elif report_type == "expiry":
                report = Report(inventory)
                print(report.generate_report("expiry"))

        elif choice == "6":
            inventory.save_to_file()

        elif choice == "7":
            inventory.load_from_file()

        elif choice == "8":
            print("Exiting system.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()
