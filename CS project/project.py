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

    def remove_item(self, item_id):
        if item_id in self.items:
            del self.items[item_id]

    def get_item(self, item_id):
        return self.items.get(item_id)

    def list_items(self):
        return [item.get_details() for item in self.items.values()]

    def update_inventory(self, item_id, new_quantity):
        item = self.get_item(item_id)
        if item:
            item.update_quantity(new_quantity)

    def check_stock(self, threshold=5):
        return [item.get_details() for item in self.items.values() if item.quantity <= threshold]

    def save_to_file(self, filename="inventory.json"):
        data = {item_id: item.get_details() for item_id, item in self.items.items()}
        with open(filename, "w") as file:
            json.dump(data, file)

    def load_from_file(self, filename="inventory.json"):
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


if __name__ == "__main__":
    inventory = Inventory()
    admin_user = User("admin1", "admin")

    item1 = Item(item_id=1, name="Hammer", category="Hand Tool", quantity=10, rental_price=5.0)
    item2 = Item(item_id=2, name="Drill", category="Power Tool", quantity=3, rental_price=15.0,
                 expiration_date="2025-01-01")

    admin_user.perform_inventory_actions("add_item", inventory, item1)
    admin_user.perform_inventory_actions("add_item", inventory, item2)

    print("Inventory List:", inventory.list_items())

    admin_user.perform_inventory_actions("update_inventory", inventory, 2, 5)
    print("Updated Inventory List:", inventory.list_items())

    inventory.save_to_file()

    new_inventory = Inventory()
    new_inventory.load_from_file()
    print("Loaded Inventory:", new_inventory.list_items())

    report = Report(new_inventory)
    print("Low Stock Report:", report.generate_report("low_stock", 5))
    print("Expiry Report:", report.generate_report("expiry"))
