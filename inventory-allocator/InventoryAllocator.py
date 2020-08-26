from collections import defaultdict


class InventoryAllocator():
    """
    Inventory Allocator static class
    ship: Class method that finds the optimal shipment of items, given an order and warehouse inventory info
    allowPartialShipment: Question statement is not clear as to if orders should be "partially" shipped, so a boolean
                          flag was added to enable/disable this.
    """

    _ALLOW_PARTIAL = False

    @classmethod
    def allowPartialShipment(cls):
        """
        Return a boolean indicating whether partial orders should be honoured
        """

        return cls._ALLOW_PARTIAL

    @classmethod
    def ship(cls, order, warehouse_inventories):

        """
            Determines optimal shipping for the order 'order', given information of the inventory in 'warehouse_inventories'.
            Return a list of maps, which has the warehouse name as the key and value being the amount that should be
            taken from that warehouse to produce the optimal shipment
        """

        # Store a map of warehouses to a map containing name of warehouse and number of each item to order
        optimal_shipment = defaultdict(lambda: {})

        for item, quantity_remaining in order.items():
            # Store a map of warehouses to the quantity of item that they will ship
            warehouses_for_item = {}

            # Iterate over warehouses from cheapest to most expensive
            for warehouse in warehouse_inventories:
                warehouse_name = warehouse["name"]
                warehouse_inv = warehouse["inventory"]

                # Skip this warehouse if it doesn't contain any instance of the item in question
                if item not in warehouse_inv or warehouse_inv[item] < 1:
                    continue
                item_stock = warehouse_inv[item]
                # If current warehouse can take up the rest of the order then take it and then  leave the loop
                if quantity_remaining <= item_stock:
                    warehouses_for_item[warehouse_name] = quantity_remaining
                    quantity_remaining = 0
                    break

                # If current warehouse can take up some of the order but not all, then take as much as possible
                elif quantity_remaining > item_stock:
                    warehouses_for_item[warehouse_name] = item_stock
                    quantity_remaining -= item_stock

            # Once we have gone through the whole set of warehouses for a particular item and we don't have enough
            # we will either return the partial order (so continue to the subsequent items), or we will simply terminate
            # depending on what the user wants.
            if quantity_remaining > 0:
                if cls.allowPartialShipment():
                    continue
                else:
                    return []

            # Add the item quantities per warehouse to our map of warehouses
            for warehouse_name, item_quantity in warehouses_for_item.items():
                optimal_shipment[warehouse_name][item] = item_quantity

        # Convert our map to a list of one-key maps, as indicated in problem description
        output = [{name: items} for name, items in optimal_shipment.items()]
        return output
