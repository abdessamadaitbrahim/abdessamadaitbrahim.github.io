/* Portfolio behaviour: theme, menu, project filters, scroll spy, reveal, hero canvas, CV link, email. */
(function () {
  "use strict";
  var root = document.documentElement;
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* theme */
  function setTheme(t) {
    root.setAttribute("data-theme", t);
    try { localStorage.setItem("theme", t); } catch (e) {}
    var b = document.querySelector(".theme-toggle");
    if (b) b.setAttribute("aria-label", t === "dark" ? "Switch to light mode" : "Switch to dark mode");
    document.dispatchEvent(new Event("themechange"));
  }
  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.setAttribute("aria-label", root.getAttribute("data-theme") === "dark" ? "Switch to light mode" : "Switch to dark mode");
    toggle.addEventListener("click", function () {
      setTheme(root.getAttribute("data-theme") === "dark" ? "light" : "dark");
    });
  }

  /* mobile menu */
  var menuBtn = document.querySelector(".menu-btn"), nav = document.querySelector(".nav");
  if (menuBtn && nav) {
    menuBtn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      menuBtn.setAttribute("aria-expanded", String(open));
    });
    nav.addEventListener("click", function (e) {
      if (e.target.tagName === "A") { nav.classList.remove("open"); menuBtn.setAttribute("aria-expanded", "false"); }
    });
  }

  /* project filters */
  var grid = document.getElementById("project-grid");
  if (grid) {
    var cards = Array.prototype.slice.call(grid.querySelectorAll(".card"));
    var filters = document.querySelectorAll(".filter");
    var moreBtn = document.getElementById("show-more");
    var current = "all";
    function apply() {
      var shown = 0;
      grid.classList.toggle("filtering", current !== "all");
      cards.forEach(function (c) {
        var ok = current === "all" || c.getAttribute("data-cats").split(" ").indexOf(current) !== -1;
        c.hidden = !ok;
        if (ok) shown++;
      });
      if (moreBtn) moreBtn.parentNode.hidden = current !== "all" || grid.classList.contains("show-all");
    }
    filters.forEach(function (f) {
      f.addEventListener("click", function () {
        current = f.getAttribute("data-filter");
        filters.forEach(function (x) { x.setAttribute("aria-pressed", String(x === f)); });
        apply();
      });
    });
    if (moreBtn) moreBtn.addEventListener("click", function () { grid.classList.add("show-all"); apply(); });
    apply();
  }

  /* scroll spy for the table of contents and the header nav */
  var links = Array.prototype.slice.call(document.querySelectorAll("[data-spy]"));
  if (links.length && "IntersectionObserver" in window) {
    var map = {};
    links.forEach(function (a) { var id = a.getAttribute("href").slice(1); (map[id] = map[id] || []).push(a); });
    var spy = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          links.forEach(function (a) { a.classList.remove("is-active"); a.removeAttribute("aria-current"); });
          (map[en.target.id] || []).forEach(function (a) { a.classList.add("is-active"); a.setAttribute("aria-current", "true"); });
        }
      });
    }, { rootMargin: "-30% 0px -60% 0px" });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) spy.observe(s); });
  }

  /* reveal on scroll */
  var items = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window && !reduceMotion) {
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); } });
    }, { threshold: 0.08 });
    items.forEach(function (el) { io.observe(el); });
  } else {
    items.forEach(function (el) { el.classList.add("in"); });
  }

  /* email, assembled in the browser so it is not in the page source */
  document.querySelectorAll("[data-email]").forEach(function (el) {
    var addr = el.getAttribute("data-user") + "@" + el.getAttribute("data-domain");
    el.setAttribute("href", "mailto:" + addr);
    if (el.hasAttribute("data-show")) el.textContent = addr;
  });

  /* CV: link only if the file exists */
  var cv = document.getElementById("cv-download");
  if (cv) {
    var url = cv.getAttribute("data-href");
    fetch(url, { method: "HEAD" }).then(function (r) {
      if (r.ok) { cv.setAttribute("href", url); cv.hidden = false; }
      else { var n = document.getElementById("cv-missing"); if (n) n.hidden = false; }
    }).catch(function () { var n = document.getElementById("cv-missing"); if (n) n.hidden = false; });
  }

  /* hero background: a drifting point cloud, like points in an embedding space */
  var canvas = document.getElementById("hero-canvas");
  if (canvas && canvas.getContext) {
    var ctx = canvas.getContext("2d"), dots = [], w = 0, h = 0, raf = 0, visible = true, color = "36,71,245", mouse = null;
    function readColor() {
      var hex = getComputedStyle(root).getPropertyValue("--accent").trim();
      if (/^#[0-9a-f]{6}$/i.test(hex)) color = parseInt(hex.slice(1, 3), 16) + "," + parseInt(hex.slice(3, 5), 16) + "," + parseInt(hex.slice(5, 7), 16);
    }
    function resize() {
      var r = canvas.getBoundingClientRect(), dpr = Math.min(window.devicePixelRatio || 1, 2);
      w = r.width; h = r.height; canvas.width = w * dpr; canvas.height = h * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var n = Math.max(24, Math.min(70, Math.round(w / 20)));
      dots = [];
      for (var i = 0; i < n; i++) dots.push({ x: Math.random() * w, y: Math.random() * h, vx: (Math.random() - .5) * .25, vy: (Math.random() - .5) * .25, r: 1 + Math.random() * 1.6 });
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
        ctx.beginPath(); ctx.arc(a.x, a.y, a.r, 0, 6.2832); ctx.fillStyle = "rgba(" + color + ",.55)"; ctx.fill();
        for (var j = i + 1; j < dots.length; j++) {
          var b = dots[j], dx = a.x - b.x, dy = a.y - b.y, d = dx * dx + dy * dy;
          if (d < 14000) { ctx.strokeStyle = "rgba(" + color + "," + (0.22 * (1 - d / 14000)).toFixed(3) + ")"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(b.x, b.y); ctx.stroke(); }
        }
        if (mouse) {
          var mx = a.x - mouse.x, my = a.y - mouse.y, md = mx * mx + my * my;
          if (md < 20000) { ctx.strokeStyle = "rgba(" + color + "," + (0.35 * (1 - md / 20000)).toFixed(3) + ")"; ctx.beginPath(); ctx.moveTo(a.x, a.y); ctx.lineTo(mouse.x, mouse.y); ctx.stroke(); }
        }
      }
    }
    function loop() { if (visible && !document.hidden) draw(); raf = requestAnimationFrame(loop); }
    window.addEventListener("resize", resize);
    document.addEventListener("themechange", function () { readColor(); draw(); });
    var hero = canvas.parentNode;
    hero.addEventListener("pointermove", function (e) { var r = canvas.getBoundingClientRect(); mouse = { x: e.clientX - r.left, y: e.clientY - r.top }; });
    hero.addEventListener("pointerleave", function () { mouse = null; });
    if ("IntersectionObserver" in window) new IntersectionObserver(function (es) { visible = es[0].isIntersecting; }).observe(hero);
    resize();
    if (!reduceMotion) loop();
  }
})();
