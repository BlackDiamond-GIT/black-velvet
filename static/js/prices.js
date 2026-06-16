(function () {
  var currencyTabs = document.querySelectorAll('[data-currency-tab]');
  var priceEls = document.querySelectorAll('.price-row__price[data-price-czk]');
  if (!priceEls.length) return;

  function formatPrice(amount, currency) {
    if (!amount) return '';
    if (currency === 'eur') return '€' + amount;
    if (currency === 'usd') return '$' + amount;
    return amount + ' Kč';
  }

  function applyCurrency(currency) {
    priceEls.forEach(function (el) {
      var amount = el.getAttribute('data-price-' + currency);
      if (amount) {
        el.textContent = formatPrice(amount, currency);
      }
    });
  }

  function activateCurrency(tab) {
    currencyTabs.forEach(function (item) {
      var isActive = item === tab;
      item.classList.toggle('is-active', isActive);
      item.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });
    applyCurrency(tab.getAttribute('data-currency-tab'));
  }

  document.querySelectorAll('.currency-tabs').forEach(function (list) {
    list.addEventListener('click', function (event) {
      var tab = event.target.closest('[data-currency-tab]');
      if (!tab || tab.classList.contains('is-active')) return;
      activateCurrency(tab);
    });
  });

  applyCurrency('czk');
})();
