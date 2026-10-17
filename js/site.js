/* YuZa Studio. Local scroll motion only: reveals, alternating cards,
   phone tilts, gallery drift, word staggers, and a sticky hero.
   Transform and opacity only. No cookies, storage, or network requests.
   Content stays visible when this file does not run. */
(function () {
  var motion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (motion.matches) return;

  var root = document.documentElement;
  var ease = "cubic-bezier(0.22, 1, 0.36, 1)";

  function splitWords(heading) {
    if (heading.getAttribute("data-words") === "1") return;
    var text = heading.textContent.replace(/\s+/g, " ").trim();
    if (!text) return;
    var words = text.split(" ");
    heading.textContent = "";
    words.forEach(function (word, index) {
      if (index) heading.appendChild(document.createTextNode(" "));
      var span = document.createElement("span");
      span.className = "word";
      span.style.setProperty("--i", String(index));
      span.textContent = word;
      heading.appendChild(span);
    });
    heading.setAttribute("data-words", "1");
    heading.classList.add("word-reveal");
    if (!heading.closest(".reveal")) heading.classList.add("reveal");
  }

  Array.prototype.forEach.call(
    document.querySelectorAll(".hero h1, .catalog h2, .band h2, .shot-section h2, .feature-block h2"),
    splitWords
  );

  var reveals = Array.prototype.slice.call(document.querySelectorAll(".reveal"));
  if (!reveals.length) return;

  function inView(el) {
    var rect = el.getBoundingClientRect();
    var vh = window.innerHeight || 1;
    return rect.top < vh * 0.9 && rect.bottom > vh * 0.08 && rect.width > 0;
  }

  function playFrames(rootEl, delay) {
    if (typeof rootEl.animate !== "function") return;
    var frames = rootEl.querySelectorAll(".frame-device, .frame-plate");
    Array.prototype.forEach.call(frames, function (frame, index) {
      var tilt = index % 2 === 0 ? "rotate(-8deg)" : "rotate(8deg)";
      frame.animate(
        [
          { opacity: 0, transform: "translate3d(0, 52px, 0) " + tilt + " scale(0.94)" },
          { opacity: 1, transform: "none" },
        ],
        { duration: 900, delay: delay + 40, easing: ease, fill: "backwards" }
      );
    });
  }

  function playWords(heading, baseDelay) {
    if (typeof heading.animate !== "function") return;
    Array.prototype.forEach.call(heading.querySelectorAll(".word"), function (word, index) {
      word.animate(
        [
          { opacity: 0, transform: "translate3d(0, 18px, 0)" },
          { opacity: 1, transform: "none" },
        ],
        { duration: 560, delay: baseDelay + index * 90, easing: ease, fill: "backwards" }
      );
    });
  }

  function playEnter(el) {
    if (typeof el.animate !== "function") return;
    var raw = window.getComputedStyle(el).getPropertyValue("--stagger");
    var delay = (parseFloat(raw) || 0) * 80;
    var from = "translate3d(0, 52px, 0) scale(0.94)";
    if (el.classList.contains("app-card") && el.parentElement) {
      var index = Array.prototype.indexOf.call(el.parentElement.children, el);
      from = index % 2 === 0
        ? "translate3d(-96px, 40px, 0) scale(0.94)"
        : "translate3d(96px, 40px, 0) scale(0.94)";
    }
    el.animate(
      [
        { opacity: 0, transform: from },
        { opacity: 1, transform: "none" },
      ],
      { duration: 980, delay: delay, easing: ease, fill: "backwards" }
    );
    playFrames(el, delay);
    if (el.classList.contains("word-reveal")) playWords(el, delay);
    var nested = el.querySelector(".word-reveal");
    if (nested) playWords(nested, delay);
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
      { root: null, rootMargin: "0px 0px -18% 0px", threshold: 0.28 }
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
    var vh = window.innerHeight || 1;
    reveals.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.bottom < 8 || inView(el)) el.classList.add("is-in");
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

  var wide = window.matchMedia("(min-width: 48rem)");
  var phones = Array.prototype.slice.call(document.querySelectorAll("[data-parallax]"));
  var galleries = Array.prototype.slice.call(document.querySelectorAll(".gallery"));
  var hero = document.querySelector(".hero");
  var hold = document.querySelector(".hero-hold");
  var ticking = false;

  function clearMotionStyles() {
    phones.forEach(function (el) {
      el.style.transform = "";
    });
    galleries.forEach(function (el) {
      el.style.transform = "";
    });
    if (hero) {
      hero.style.transform = "";
      hero.style.opacity = "";
    }
  }

  function paint() {
    ticking = false;
    if (motion.matches) return;
    var vh = window.innerHeight || 1;
    var maxShift = wide.matches ? 72 : 28;
    phones.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.width < 2 || rect.height < 2) {
        el.style.transform = "";
        return;
      }
      var speed = parseFloat(el.getAttribute("data-parallax")) || 0.16;
      var delta = rect.top + rect.height / 2 - vh / 2;
      var shift = Math.max(-maxShift, Math.min(maxShift, -delta * speed));
      el.style.transform = "translate3d(0," + shift.toFixed(2) + "px,0)";
    });
    var travel = wide.matches ? Math.min(vh * 0.34, 260) : 0;
    galleries.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      if (rect.width < 2 || rect.bottom < 0 || rect.top > vh || !travel) {
        el.style.transform = "";
        return;
      }
      var progress = (vh * 0.65 - rect.top) / (vh * 0.7 + rect.height);
      if (progress < 0) progress = 0;
      if (progress > 1) progress = 1;
      var shift = (0.55 - progress) * travel;
      el.style.transform = "translate3d(" + shift.toFixed(2) + "px,0,0)";
    });
    if (hero && hold) {
      var holdRect = hold.getBoundingClientRect();
      var runway = hold.offsetHeight - hero.offsetHeight;
      var scrolled = -holdRect.top;
      if (scrolled < 0) scrolled = 0;
      if (runway > 4 && scrolled > runway) scrolled = runway;
      var t = runway > 4 ? scrolled / runway : 0;
      hero.style.transform = "scale(" + (1 - t * 0.08).toFixed(4) + ")";
      hero.style.opacity = (1 - t * 0.42).toFixed(4);
    }
  }

  function requestPaint() {
    if (ticking) return;
    ticking = true;
    window.requestAnimationFrame(paint);
  }

  window.addEventListener("scroll", requestPaint, { passive: true });
  window.addEventListener("resize", requestPaint, { passive: true });
  wide.addEventListener("change", requestPaint);
  requestPaint();

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
    clearMotionStyles();
  });
})();
