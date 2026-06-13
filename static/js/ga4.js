(function () {
  'use strict';

  var measurementId = document.body.dataset.ga4;
  if (!measurementId) return;

  window.dataLayer = window.dataLayer || [];
  function gtag() { dataLayer.push(arguments); }
  gtag('js', new Date());
  gtag('config', measurementId);

  function track(eventName, params) {
    if (typeof gtag === 'function') {
      gtag('event', eventName, params);
    }
  }

  document.addEventListener('click', function (e) {
    var cta = e.target.closest('[data-track-cta]');
    if (cta) {
      track('cta_click', {
        event_category: 'conversion',
        event_label: cta.dataset.trackCta
      });
    }

    var phone = e.target.closest('a[href^="tel:"]');
    if (phone) {
      track('phone_click', {
        event_category: 'conversion',
        event_label: phone.getAttribute('href')
      });
    }
  });

  document.addEventListener('submit', function (e) {
    var form = e.target;
    if (form.dataset.trackForm) {
      track('form_submit', {
        event_category: 'conversion',
        event_label: form.dataset.trackForm
      });
    }
  });
})();
