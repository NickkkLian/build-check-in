def add_item(item, bag=None):
    if bag is None:
        bag = []
    bag.append(item)
    return bag
