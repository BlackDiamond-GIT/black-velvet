(function () {
  'use strict';

  var modal = document.getElementById('site-modal');
  if (!modal) return;

  var body = document.getElementById('modal-body');
  var dialog = modal.querySelector('.modal__dialog');
  var lastFocus = null;

  function lockScroll() {
    document.body.style.overflow = 'hidden';
  }

  function unlockScroll() {
    document.body.style.overflow = '';
  }

  function closeModal() {
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    unlockScroll();
    body.innerHTML = '';
    if (lastFocus && typeof lastFocus.focus === 'function') {
      lastFocus.focus();
    }
    window.setTimeout(function () {
      modal.hidden = true;
    }, 300);
  }

  function openModal(html, titleId) {
    lastFocus = document.activeElement;
    body.innerHTML = html;
    if (titleId) {
      var titleEl = body.querySelector('#' + titleId);
      if (titleEl) {
        dialog.setAttribute('aria-labelledby', titleId);
      }
    }
    modal.hidden = false;
    modal.setAttribute('aria-hidden', 'false');
    requestAnimationFrame(function () {
      modal.classList.add('is-open');
    });
    lockScroll();
    var closeBtn = modal.querySelector('.modal__close');
    if (closeBtn) closeBtn.focus();
  }

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function buildServiceModal(card) {
    var name = escapeHtml(card.dataset.serviceName || '');
    var desc = escapeHtml(card.dataset.serviceDesc || '');
    var price = escapeHtml(card.dataset.servicePrice || '');
    var duration = escapeHtml(card.dataset.serviceDuration || '');
    var url = card.dataset.serviceUrl || '#';
    var image = card.dataset.serviceImage || '';
    var reserveUrl = card.dataset.reserveUrl || url;

    var imageHtml = image
      ? '<img class="modal__image" src="' + image + '" alt="' + name + '">'
      : '<div class="modal__image modal__image--placeholder">' + name + '</div>';

    return imageHtml +
      '<h2 class="modal__title" id="modal-title">' + name + '</h2>' +
      '<p class="modal__desc">' + desc + '</p>' +
      '<div class="modal__meta">' +
        '<div class="modal__meta-item"><span>Cena</span><strong>' + price + '</strong></div>' +
        '<div class="modal__meta-item"><span>Délka</span><strong>' + duration + '</strong></div>' +
      '</div>' +
      '<div class="modal__actions">' +
        '<a href="' + reserveUrl + '" class="btn btn--primary">Rezervovat</a>' +
        '<a href="' + url + '" class="btn btn--outline">Detail</a>' +
      '</div>';
  }

  function buildContactModal(trigger) {
    var name = escapeHtml(trigger.dataset.siteName || '');
    var address = escapeHtml(trigger.dataset.siteAddress || '');
    var phone = escapeHtml(trigger.dataset.sitePhone || '');
    var email = escapeHtml(trigger.dataset.siteEmail || '');
    var mapsUrl = 'https://maps.google.com/?q=' + encodeURIComponent(trigger.dataset.siteAddress || '');

    return '<h2 class="modal__title" id="modal-title">' + name + '</h2>' +
      '<div class="modal__contact-row"><span>Adresa</span><p>' + address + '</p></div>' +
      '<div class="modal__contact-row"><span>Telefon</span><a href="tel:' + phone.replace(/\s/g, '') + '">' + phone + '</a></div>' +
      '<div class="modal__contact-row"><span>E-mail</span><a href="mailto:' + email + '">' + email + '</a></div>' +
      '<div class="modal__hours">' +
        '<span style="display:block;font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:rgba(240,233,224,.35);margin-bottom:12px;">Otevírací doba</span>' +
        '<div class="modal__hours-grid">' +
          '<span style="color:rgba(240,233,224,.45);">Denně</span><span>9:00 — 5:00 ráno</span>' +
        '</div>' +
      '</div>' +
      '<div class="modal__actions" style="margin-top:28px;">' +
        '<a href="' + mapsUrl + '" class="btn btn--primary" target="_blank" rel="noopener noreferrer">Otevřít v Mapách</a>' +
      '</div>';
  }

  document.addEventListener('click', function (e) {
    var serviceTrigger = e.target.closest('[data-service-modal-trigger]');
    if (serviceTrigger) {
      e.preventDefault();
      var card = serviceTrigger.closest('[data-service-modal]');
      if (card) openModal(buildServiceModal(card), 'modal-title');
      return;
    }

    var contactTrigger = e.target.closest('[data-contact-modal-trigger]');
    if (contactTrigger) {
      e.preventDefault();
      openModal(buildContactModal(contactTrigger), 'modal-title');
    }
  });

  modal.addEventListener('click', function (e) {
    if (e.target.closest('[data-modal-close]')) {
      closeModal();
    }
  });

  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && modal.classList.contains('is-open')) {
      closeModal();
    }
  });
})();
