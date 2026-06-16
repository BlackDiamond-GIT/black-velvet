def build_price_list(categories):
    entries = []
    for category in categories:
        for item in category.items.all():
            entries.append({
                'item': item,
                'category': category.name,
            })
    return entries
