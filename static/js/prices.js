(function () {
  var tablist = document.querySelector('.duration-tabs');
  if (!tablist) return;

  var tabs = tablist.querySelectorAll('[data-duration-tab]');
  var panels = document.querySelectorAll('[data-duration-panel]');
  var currencyTabs = document.querySelectorAll('[data-currency-tab]');
  var priceEls = document.querySelectorAll('.price-row__price[data-price-czk]');
  var activeCurrency = 'czk';

  function formatPrice(amount, currency) {
    if (!amount) return '';
    if (currency === 'eur') return '€' + amount;
    if (currency === 'usd') return '$' + amount;
    return amount + ' Kč';
  }

  function applyCurrency(currency) {
    activeCurrency = currency;
    priceEls.forEach(function (el) {
      var amount = el.getAttribute('data-price-' + currency);
      if (amount) {
        el.textContent = formatPrice(amount, currency);
      }
    });
  }

  function activateTab(tab) {
    var target = tab.getAttribute('data-duration-tab');

    tabs.forEach(function (item) {
      var isActive = item === tab;
      item.classList.toggle('is-active', isActive);
      item.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });

    panels.forEach(function (panel) {
      var isActive = panel.getAttribute('data-duration-panel') === target;
      panel.classList.toggle('is-active', isActive);
      panel.hidden = !isActive;
    });

    tab.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
  }

  function activateCurrency(tab) {
    var currency = tab.getAttribute('data-currency-tab');
    currencyTabs.forEach(function (item) {
      var isActive = item === tab;
      item.classList.toggle('is-active', isActive);
      item.setAttribute('aria-selected', isActive ? 'true' : 'false');
    });
    applyCurrency(currency);
  }

  tablist.addEventListener('click', function (event) {
    var tab = event.target.closest('[data-duration-tab]');
    if (!tab || tab.classList.contains('is-active')) return;
    activateTab(tab);
  });

  tablist.addEventListener('keydown', function (event) {
    var current = tablist.querySelector('.duration-tabs__btn.is-active');
    if (!current) return;

    var items = Array.prototype.slice.call(tabs);
    var index = items.indexOf(current);
    var nextIndex = index;

    if (event.key === 'ArrowRight') {
      nextIndex = (index + 1) % items.length;
    } else if (event.key === 'ArrowLeft') {
      nextIndex = (index - 1 + items.length) % items.length;
    } else if (event.key === 'Home') {
      nextIndex = 0;
    } else if (event.key === 'End') {
      nextIndex = items.length - 1;
    } else {
      return;
    }

    event.preventDefault();
    items[nextIndex].focus();
    activateTab(items[nextIndex]);
  });

  document.querySelectorAll('.currency-tabs').forEach(function (list) {
    list.addEventListener('click', function (event) {
      var tab = event.target.closest('[data-currency-tab]');
      if (!tab || tab.classList.contains('is-active')) return;
      activateCurrency(tab);
    });
  });

  applyCurrency(activeCurrency);
})();
