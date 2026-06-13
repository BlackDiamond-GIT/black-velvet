(function () {
  'use strict';

  function initMobileMenu() {
    var btn = document.querySelector('[data-mobile-menu-toggle]');
    var overlay = document.querySelector('[data-mobile-overlay]');
    var closeBtns = document.querySelectorAll('[data-mobile-menu-close]');
    if (!btn || !overlay) return;

    function openMenu() {
      overlay.classList.add('open');
      document.body.style.overflow = 'hidden';
    }

    function closeMenu() {
      overlay.classList.remove('open');
      document.body.style.overflow = '';
    }

    btn.addEventListener('click', function () {
      if (overlay.classList.contains('open')) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    closeBtns.forEach(function (el) {
      el.addEventListener('click', closeMenu);
    });

    overlay.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', closeMenu);
    });
  }

  function initNavScroll() {
    var nav = document.querySelector('.site-nav');
    if (!nav) return;

    window.addEventListener('scroll', function () {
      nav.classList.toggle('scrolled', window.scrollY > 60);
    }, { passive: true });
  }

  function initFAQ() {
    document.querySelectorAll('.faq-item').forEach(function (item) {
      var trigger = item.querySelector('.faq-trigger');
      var body = item.querySelector('.faq-body');
      if (!trigger || !body) return;

      trigger.addEventListener('click', function () {
        var isOpen = item.classList.contains('open');
        document.querySelectorAll('.faq-item.open').forEach(function (openItem) {
          openItem.classList.remove('open');
          var b = openItem.querySelector('.faq-body');
          if (b) b.style.maxHeight = '0px';
        });
        if (!isOpen) {
          item.classList.add('open');
          body.style.maxHeight = body.scrollHeight + 'px';
        }
      });
    });
  }

  function initTestimonials() {
    var block = document.querySelector('[data-testimonials]');
    if (!block) return;

    var track = block.querySelector('[data-testimonial-track]');
    var slides = block.querySelectorAll('[data-testimonial-item]');
    var dots = block.querySelectorAll('[data-testimonial-dot]');
    if (!track || !slides.length) return;

    var current = 0;
    var timer;
    var isVisible = true;
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function setActive(index) {
      current = index;
      dots.forEach(function (dot, i) {
        dot.classList.toggle('is-active', i === current);
      });
    }

    function scrollSlideTo(index, smooth) {
      var slide = slides[index];
      var offset = slide.offsetLeft - (track.clientWidth - slide.clientWidth) / 2;
      track.scrollTo({
        left: Math.max(0, offset),
        behavior: smooth && !reducedMotion ? 'smooth' : 'auto'
      });
    }

    function goTo(index, smooth) {
      var next = (index + slides.length) % slides.length;
      scrollSlideTo(next, smooth);
      setActive(next);
    }

    function onScroll() {
      var trackRect = track.getBoundingClientRect();
      var trackCenter = trackRect.left + trackRect.width / 2;
      var closest = 0;
      var minDist = Infinity;

      slides.forEach(function (slide, i) {
        var rect = slide.getBoundingClientRect();
        var slideCenter = rect.left + rect.width / 2;
        var dist = Math.abs(slideCenter - trackCenter);
        if (dist < minDist) {
          minDist = dist;
          closest = i;
        }
      });

      if (closest !== current) {
        setActive(closest);
      }
    }

    track.addEventListener('scroll', onScroll, { passive: true });

    dots.forEach(function (dot, i) {
      dot.addEventListener('click', function () {
        goTo(i, true);
        startAuto();
      });
    });

    function startAuto() {
      clearInterval(timer);
      if (reducedMotion || !isVisible) return;
      timer = setInterval(function () {
        if (!isVisible) return;
        goTo(current + 1, true);
      }, 6500);
    }

    if ('IntersectionObserver' in window) {
      var visibilityObserver = new IntersectionObserver(function (entries) {
        isVisible = entries[0].isIntersecting;
        if (isVisible) {
          startAuto();
        } else {
          clearInterval(timer);
        }
      }, { threshold: 0.15 });
      visibilityObserver.observe(block);
    }

    goTo(0, false);
    startAuto();
  }

  document.addEventListener('DOMContentLoaded', function () {
    initMobileMenu();
    initNavScroll();
    initFAQ();
    initTestimonials();
  });

  document.body.addEventListener('htmx:afterSwap', function () {
    initFAQ();
  });
})();
