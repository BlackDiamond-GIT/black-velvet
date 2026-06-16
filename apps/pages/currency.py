CURRENCIES = ('czk', 'eur', 'usd')

CURRENCY_LABELS = {
    'czk': 'Kč',
    'eur': '€',
    'usd': '$',
}


def format_price(amount, currency='czk'):
    if amount is None:
        return ''
    currency = (currency or 'czk').lower()
    if currency == 'eur':
        return f'€{amount}'
    if currency == 'usd':
        return f'${amount}'
    return f'{amount} Kč'


def price_amounts(czk, eur=None, usd=None):
    return {
        'czk': czk,
        'eur': eur,
        'usd': usd,
    }
