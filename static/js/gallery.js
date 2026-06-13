(function () {
  'use strict';

  var SWIPE_THRESHOLD = 40;

  function initMediaGallery(gallery) {
    if (gallery.dataset.galleryBound) return;
    gallery.dataset.galleryBound = '1';

    var track = gallery.querySelector('[data-gallery-track]');
    var dots = gallery.querySelectorAll('[data-gallery-dot]');
    var slides = gallery.querySelectorAll('[data-gallery-slide]');
    if (!track || !slides.length) return;

    var current = 0;
    var reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    var touchStartX = 0;
    var touchStartY = 0;
    var touchDeltaX = 0;
    var isSwiping = false;
    var slideCount = slides.length;

    function getSlideWidth() {
      return Math.round(track.getBoundingClientRect().width);
    }

    function applyPositions(index, offsetPx, animate) {
      var slideWidth = getSlideWidth();
      if (!slideWidth) return;

      var offset = offsetPx || 0;
      var transition = animate && !reducedMotion ? 'transform 0.45s ease' : 'none';

      track.classList.toggle('is-dragging', !animate && offset !== 0);

      slides.forEach(function (slide, i) {
        var x = Math.round((i - index) * slideWidth + offset);
        slide.style.transition = transition;
        slide.style.transform = 'translate3d(' + x + 'px, 0, 0)';
        slide.classList.toggle('is-active', i === index);
      });
    }

    function setActive(index) {
      current = index;
      gallery.classList.toggle('is-slide-blur', current === 1);
      gallery.classList.remove('is-revealed');

      dots.forEach(function (dot, i) {
        var active = i === current;
        dot.classList.toggle('is-active', active);
        if (active) {
          dot.setAttribute('aria-current', 'true');
        } else {
          dot.removeAttribute('aria-current');
        }
      });
    }

    function goTo(index, animate) {
      var next = Math.max(0, Math.min(index, slideCount - 1));
      setActive(next);
      applyPositions(next, 0, animate);
    }

    dots.forEach(function (dot, index) {
      function activateDot(e) {
        e.preventDefault();
        e.stopPropagation();
        goTo(index, true);
      }

      dot.addEventListener('click', activateDot);
      dot.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') {
          activateDot(e);
        }
      });
    });

    track.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowLeft') {
        e.preventDefault();
        goTo(current - 1, true);
      } else if (e.key === 'ArrowRight') {
        e.preventDefault();
        goTo(current + 1, true);
      }
    });

    gallery.addEventListener('touchstart', function (e) {
      if (e.target.closest('[data-gallery-dot]')) return;

      var touch = e.touches[0];
      touchStartX = touch.clientX;
      touchStartY = touch.clientY;
      touchDeltaX = 0;
      isSwiping = false;

      if (current === 1) {
        gallery.classList.add('is-revealed');
      }
    }, { passive: true });

    gallery.addEventListener('touchmove', function (e) {
      if (e.target.closest('[data-gallery-dot]')) return;

      var touch = e.touches[0];
      touchDeltaX = touch.clientX - touchStartX;
      var touchDeltaY = touch.clientY - touchStartY;

      if (!isSwiping && Math.abs(touchDeltaX) > 8 && Math.abs(touchDeltaX) > Math.abs(touchDeltaY)) {
        isSwiping = true;
      }

      if (!isSwiping) return;

      var atStart = current === 0 && touchDeltaX > 0;
      var atEnd = current === slideCount - 1 && touchDeltaX < 0;
      var offset = touchDeltaX;

      if (atStart || atEnd) {
        offset = touchDeltaX * 0.3;
      }

      applyPositions(current, offset, false);
    }, { passive: true });

    gallery.addEventListener('touchend', function (e) {
      if (e.target.closest('[data-gallery-dot]')) return;

      gallery.classList.remove('is-revealed');

      if (isSwiping) {
        if (touchDeltaX < -SWIPE_THRESHOLD && current < slideCount - 1) {
          goTo(current + 1, true);
        } else if (touchDeltaX > SWIPE_THRESHOLD && current > 0) {
          goTo(current - 1, true);
        } else {
          goTo(current, true);
        }

        var link = gallery.closest('a');
        if (link) {
          link.addEventListener('click', function blockNav(ev) {
            ev.preventDefault();
            ev.stopPropagation();
            link.removeEventListener('click', blockNav, true);
          }, true);
        }
      } else {
        goTo(current, true);
      }

      isSwiping = false;
      touchDeltaX = 0;
    }, { passive: true });

    gallery.addEventListener('touchcancel', function () {
      gallery.classList.remove('is-revealed');
      isSwiping = false;
      touchDeltaX = 0;
      goTo(current, true);
    }, { passive: true });

    gallery.querySelectorAll('[data-gallery-dot]').forEach(function (dot) {
      dot.addEventListener('touchstart', function (e) {
        e.stopPropagation();
      }, { passive: true });
    });

    window.addEventListener('resize', function () {
      goTo(current, false);
    });

    goTo(0, false);
  }

  function initMediaGalleries() {
    document.querySelectorAll('[data-media-gallery]').forEach(initMediaGallery);
  }

  document.addEventListener('DOMContentLoaded', initMediaGalleries);
})();
