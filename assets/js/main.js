/* Portfolio behaviour (light theme only): menus, project filters, "On this page" scroll spy, reveal, email, hero canvas. */
(function () {
  "use strict";
  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function $(s, c) { return (c || document).querySelector(s); }
  function $$(s, c) { return Array.prototype.slice.call((c || document).querySelectorAll(s)); }

  /* mobile menu */
  var menuBtn = $(".menu-btn"), nav = $(".nav");
  function closeMenu() {
    if (!nav || !menuBtn) return;
    nav.classList.remove("open");
    menuBtn.setAttribute("aria-expanded", "false");
    menuBtn.setAttribute("aria-label", "Open menu");
  }
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
      menuBtn.setAttribute("aria-label", open ? "Close menu" : "Open menu");
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) closeMenu(); });
  }

  /* "More" dropdown */
  var more = $(".nav__more"), moreBtn = $(".nav__more-btn");
  function closeMore() {
    if (more) { more.classList.remove("open"); moreBtn.setAttribute("aria-expanded", "false"); }
  }
  if (more && moreBtn) {
    moreBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = more.classList.toggle("open");
      moreBtn.setAttribute("aria-expanded", String(open));
    });
    document.addEventListener("click", function (e) { if (!more.contains(e.target)) closeMore(); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") {
      if (more && more.classList.contains("open")) { closeMore(); moreBtn.focus(); }
      if (nav && nav.classList.contains("open")) { closeMenu(); menuBtn.focus(); }
    }
  });

  /* project filters */
  var grid = document.getElementById("project-grid");
  if (grid) {
    var cards = $$(".card", grid), filters = $$(".filter"), showMore = document.getElementById("show-more"), status = document.getElementById("filter-status");
    var current = "all";
    function apply() {
      var shown = 0;
      grid.classList.toggle("filtering", current !== "all");
      cards.forEach(function (c) {
        var ok = current === "all" || c.getAttribute("data-cats").split(" ").indexOf(current) !== -1;
        c.hidden = !ok;
        if (ok) { shown++; c.classList.add("in"); }
      });
      if (showMore) showMore.parentNode.hidden = current !== "all" || grid.classList.contains("show-all");
      if (status) status.textContent = shown + " projects shown";
    }
    filters.forEach(function (f) {
      f.addEventListener("click", function () {
        current = f.getAttribute("data-filter");
        filters.forEach(function (x) { x.setAttribute("aria-pressed", String(x === f)); });
        apply();
      });
    });
    if (showMore) showMore.addEventListener("click", function () {
      grid.classList.add("show-all");
      cards.forEach(function (c) { c.classList.add("in"); });
      apply();
      var first = $(".is-extra a[href]:not([tabindex])", grid);
      if (first) first.focus({ preventScroll: true });
    });
    apply();
  }

  /* "On this page": highlight the section in view */
  var links = $$(".toc a[data-spy]");
  if (links.length && "IntersectionObserver" in window) {
    var map = {};
    links.forEach(function (a) { map[a.getAttribute("href").slice(1)] = a; });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (!en.isIntersecting) return;
        links.forEach(function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
        var a = map[en.target.id];
        if (a) { a.classList.add("is-active"); a.setAttribute("aria-current", "location"); }
      });
    }, { rootMargin: "-20% 0px -70% 0px" });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) spy.observe(s); });
  }

  /* reveal on scroll */
  var items = $$(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); } });
    }, { threshold: 0.06, rootMargin: "0px 0px -4% 0px" });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  /* email, assembled in the browser so it is not in the page source.
     Every Email link opens a ready-to-send Gmail compose window in a new tab. */
  var SUBJECT = "Portfolio contact";
  function address(el) { return el.getAttribute("data-user") + "@" + el.getAttribute("data-domain"); }
  $$("[data-email]").forEach(function (el) {
    var addr = address(el);
    el.setAttribute("href", "https://mail.google.com/mail/?view=cm&fs=1&to=" + encodeURIComponent(addr) + "&su=" + encodeURIComponent(SUBJECT));
    el.setAttribute("target", "_blank");
    el.setAttribute("rel", "noopener noreferrer");
    var t = $("[data-email-text]", el);
    if (t) t.textContent = addr;
  });

  /* "Copy address" fallback for visitors without a mail app */
  $$("[data-copy-email]").forEach(function (btn) {
    var addr = address(btn), label = $("span", btn), idle = label.textContent, status = $("[data-copy-status]", btn.closest(".contact__item, .foot__mail") || btn.parentNode), timer = 0;
    function done(ok) {
      /* lock the current width so the "Copied" label never moves the layout */
      if (!btn.style.width) btn.style.width = btn.getBoundingClientRect().width + "px";
      label.textContent = ok ? "Copied" : (idle.length > 6 ? "Copy failed" : "Failed");
      if (status) status.textContent = ok ? "Email address copied to the clipboard" : "Copy failed; the address is " + addr;
      btn.classList.toggle("is-done", ok);
      clearTimeout(timer);
      timer = setTimeout(function () { label.textContent = idle; btn.classList.remove("is-done"); if (status) status.textContent = ""; }, 2200);
    }
    function legacy() {
      var ta = document.createElement("textarea");
      ta.value = addr; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta);
      return ok;
    }
    btn.hidden = false;
    btn.addEventListener("click", function () {
      if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(addr).then(function () { done(true); }, function () { done(legacy()); });
      } else {
        done(legacy());
      }
    });
  });

  /* hero background: a slow point cloud, like points in an embedding space */
  var canvas = document.getElementById("hero-canvas");
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext("2d"), dots = [], w = 0, h = 0, visible = true, accent = "140,47,31", sage = "86,99,73", mouse = null;
    function rgb(name, fallback) {
      var hex = getComputedStyle(root).getPropertyValue(name).trim();
      return /^#[0-9a-f]{6}$/i.test(hex) ? parseInt(hex.slice(1, 3), 16) + "," + parseInt(hex.slice(3, 5), 16) + "," + parseInt(hex.slice(5, 7), 16) : fallback;
    }
    function readColor() { accent = rgb("--accent", accent); sage = rgb("--sage", sage); }
    function resize() {
      var r = canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = r.width; h = r.height; canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.max(20, Math.min(60, Math.round(w / 24)));
      dots = [];
      for (var i = 0; i < n; i++) dots.push({ x: Math.random() * w, y: Math.random() * h, vx: (Math.random() - .5) * .2, vy: (Math.random() - .5) * .2, r: .8 + Math.random() * 1.5, c: Math.random() < .3 ? 1 : 0 });
      readColor(); draw();
    }
    function draw() {
      ctx.clearRect(0, 0, w, h);
      for (var i = 0; i < dots.length; i++) {
        var a = dots[i];
        if (!reduceMotion) {
          a.x += a.vx; a.y += a.vy;
          if (a.x < 0 || a.x > w) a.vx *= -1;
          if (a.y < 0 || a.y > h) a.vy *= -1;
        }
        ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.2832); ctx.fillStyle = "rgba(" + (a.c ? sage : accent) + ",.5)"; ctx.fill();
        for (var j = i + 1; j < dots.length; j++) {
          var b = dots[j], dx = a.x - b.x, dy = a.y - b.y, d = dx * dx + dy * dy;
          if (d < 13000) { ctx.strokeStyle = "rgba(" + accent + "," + (0.16 * (1 - d / 13000)).toFixed(3) + ")"; ctx.lineWidth = .8; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
        if (mouse) {
          var mx = a.x - mouse.x, my = a.y - mouse.y, md = mx * mx + my * my;
          if (md < 18000) { ctx.strokeStyle = "rgba(" + accent + "," + (0.3 * (1 - md / 18000)).toFixed(3) + ")"; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke(); }
        }
      }
    }
    function loop() { if (visible && !document.hidden) draw(); requestAnimationFrame(loop); }
    var t = 0;
    window.addEventListener("resize", function () { clearTimeout(t); t = setTimeout(resize, 150); });
    var hero = canvas.parentNode;
    hero.addEventListener("pointermove", function (e) { var r = canvas.getBoundingClientRect(); mouse = { x: e.clientX - r.left, y: e.clientY - r.top }; });
    hero.addEventListener("pointerleave", function () { mouse = null; });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(hero);
    resize();
    if (!reduceMotion) loop();
  }
})();
