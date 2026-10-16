/* YuZa Studio. Local enhancements only: scroll reveals, staggered card
   entrances, and a light parallax on hero phones. No cookies, storage,
   or network requests. Content stays visible when this file does not run. */
(function () {
  var motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (motion.matches) return;

  var root = document.documentElement;
  var reveals = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if (!reveals.length) return;

  function inView(el) {
    var rect = el.getBoundingClientRect();
    var vh = window.innerHeight || 1;
    return rect.bottom > vh * 0.04 && rect.top < vh * 0.96 && rect.width > 0;
  }

  function playEnter(el) {
    if (typeof el.animate !== "function") return;
    var raw = window.getComputedStyle(el).getPropertyValue("--stagger");
    var delay = (parseFloat(raw) || 0) * 75;
    el.animate(
      [
        { opacity: 0, transform: "translateY(0.85rem)" },
        { opacity: 1, transform: "translateY(0)" },
      ],
      {
        duration: 640,
        delay: delay,
        easing: "cubic-bezier(0.22, 1, 0.36, 1)",
        fill: "backwards",
      }
    );
  }

  var starters = [];
  reveals.forEach(function (el) {
    if (!inView(el)) return;
    el.classList.add("is-in");
    starters.push(el);
  });
  starters.forEach(playEnter);
  root.classList.add("js");

  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          entry.target.classList.add("is-in");
          io.unobserve(entry.target);
        });
      },
      { root: null, rootMargin: "0px 0px -8% 0px", threshold: 0.16 }
    );
    reveals.forEach(function (el) {
      if (!el.classList.contains("is-in")) io.observe(el);
    });
  } else {
    reveals.forEach(function (el) {
      el.classList.add("is-in");
    });
  }

  function showIfSeen() {
    reveals.forEach(function (el) {
      if (inView(el)) el.classList.add("is-in");
    });
  }
  window.addEventListener("scroll", showIfSeen, { passive: true });
  document.addEventListener("visibilitychange", showIfSeen);
  document.addEventListener("focusin", function (event) {
    var node = event.target;
    if (!node || typeof node.closest !== "function") return;
    var reveal = node.closest(".reveal");
    if (reveal) reveal.classList.add("is-in");
  });

  var wide = window.matchMedia("(min-width: 60rem) and (pointer: fine)");
  var phones = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  var ticking = false;

  function paint() {
    ticking = false;
    if (motion.matches) return;
    if (!wide.matches) {
      phones.forEach(function (el) {
        el.style.transform = "";
      });
      return;
    }
    var vh = window.innerHeight || 1;
    phones.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.width < 2 || rect.height < 2) {
        el.style.transform = "";
        return;
      }
      var speed = parseFloat(el.getAttribute("data-parallax")) || 0.05;
      var delta = rect.top + rect.height / 2 - vh / 2;
      var shift = Math.max(-14, Math.min(14, -delta * speed));
      el.style.transform = "translate3d(0," + shift.toFixed(2) + "px,0)";
    });
  }

  function requestPaint() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(paint);
  }

  if (phones.length) {
    window.addEventListener("scroll", requestPaint, { passive: true });
    window.addEventListener("resize", requestPaint, { passive: true });
    wide.addEventListener("change", requestPaint);
    requestPaint();
  }

  motion.addEventListener("change", function (event) {
    if (!event.matches) return;
    root.classList.remove("js");
    reveals.forEach(function (el) {
      el.classList.add("is-in");
      if (typeof el.getAnimations === "function") {
        el.getAnimations().forEach(function (anim) {
          anim.cancel();
        });
      }
    });
    phones.forEach(function (el) {
      el.style.transform = "";
    });
  });
})();
