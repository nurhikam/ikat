/*!
 * undangan-engine v1
 * A data-driven renderer for single-page digital wedding invitations.
 *
 * Contract: this file NEVER contains theme decisions (colour, font, ornament).
 * It emits a stable DOM + class structure; themes restyle it via CSS only.
 * See docs/THEMING.md.
 */
(function () {
  'use strict';

  /* ------------------------------------------------------------------ util */

  var ENT = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' };
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) { return ENT[c]; });
  }
  /** Escape for use inside an attribute that we also want URL-safe-ish. */
  function escAttr(s) {
    var v = String(s == null ? '' : s);
    if (/^\s*javascript:/i.test(v)) return '';
    return esc(v);
  }
  function el(html) {
    var t = document.createElement('template');
    t.innerHTML = html.trim();
    return t.content.firstElementChild;
  }
  function qs(sel, root) { return (root || document).querySelector(sel); }
  function qsa(sel, root) { return Array.prototype.slice.call((root || document).querySelectorAll(sel)); }
  function has(v) { return v != null && String(v).trim() !== ''; }

  /** Optional block: returns '' when the value is empty, so themes never
   *  have to style an empty element that shouldn't be there. */
  function when(v, fn) { return has(v) ? fn(v) : ''; }

  /* ------------------------------------------------------------- formatting */

  var LOCALE = 'id-ID';
  var TZ = 'Asia/Jakarta';
  var TZ_LABEL = 'WIB';

  function parseDate(v) {
    if (!has(v)) return null;
    var d = new Date(v);
    return isNaN(d.getTime()) ? null : d;
  }

  /* Every displayed date is formatted in the wedding's timezone, never the
   * viewer's. A guest opening this from Jeddah or a server rendering it in UTC
   * must still read the local Indonesian ceremony time. */
  function fmtDate(d, opts) {
    if (!d) return '';
    try {
      var o = {};
      for (var k in opts) o[k] = opts[k];
      o.timeZone = TZ;
      return new Intl.DateTimeFormat(LOCALE, o).format(d);
    } catch (e) { return d.toDateString(); }
  }

  /* Formats a date whose local fields ALREADY hold wall-clock time in TZ
   * (see wallClock) — applying the timezone again would double-shift it. */
  function fmtLocal(d, opts) {
    if (!d) return '';
    try { return new Intl.DateTimeFormat(LOCALE, opts).format(d); }
    catch (e) { return d.toDateString(); }
  }

  /* Returns a Date whose *local* getters yield the wall-clock time in TZ, so
   * calendar arithmetic (which day of the week is it there?) works without
   * pulling in a date library. */
  function wallClock(d) {
    try {
      var p = new Intl.DateTimeFormat('en-US', {
        timeZone: TZ, year: 'numeric', month: '2-digit', day: '2-digit',
        hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false
      }).formatToParts(d).reduce(function (a, x) { a[x.type] = x.value; return a; }, {});
      return new Date(+p.year, +p.month - 1, +p.day, +p.hour % 24, +p.minute, +p.second);
    } catch (e) { return new Date(d.getTime()); }
  }

  function fmtTime(d) {
    if (!d) return '';
    return fmtDate(d, { hour: '2-digit', minute: '2-digit', hour12: false }).replace(/\./g, ':');
  }
  function pad(n) { return n < 10 ? '0' + n : String(n); }

  /* ------------------------------------------------------- ornament slots */

  /** Every section gets the same decoration hooks. Themes fill them (or not)
   *  purely from CSS — the engine has no opinion about what appears here. */
  function orn() {
    return '<div class="u-orn u-orn--top" aria-hidden="true"></div>' +
           '<div class="u-orn u-orn--bottom" aria-hidden="true"></div>';
  }

  function photo(src, cls, alt, fallback) {
    if (has(src)) {
      return '<img class="u-photo ' + cls + '" src="' + escAttr(src) + '" alt="' + esc(alt || '') +
             '" loading="lazy" decoding="async">';
    }
    // No photo supplied — render a typographic placeholder instead of a broken
    // image. Deliberate: invitations without prewedding photos are a supported
    // first-class case, not a degraded one.
    return '<div class="u-photo u-photo--empty ' + cls + '" role="img" aria-label="' + esc(alt || '') + '">' +
           '<span class="u-photo__mono">' + esc(fallback || '') + '</span></div>';
  }

  /* --------------------------------------------------------------- sections */

  var Sections = {

    cover: function (s, cfg) {
      var d = parseDate(cfg.date);
      var mono = has(s.monogram) ? s.monogram
        : (cfg.couple.bride.name || '') + ' & ' + (cfg.couple.groom.name || '');
      return '' +
      '<section class="u-sec u-cover" id="u-cover" data-sec="cover">' + orn() +
        '<div class="u-cover__inner">' +
          when(s.eyebrow, function (v) { return '<p class="u-cover__eyebrow">' + esc(v) + '</p>'; }) +
          '<h1 class="u-cover__names">' +
            '<span class="u-cover__name">' + esc(cfg.couple.bride.name) + '</span>' +
            '<span class="u-cover__amp" aria-hidden="true">&amp;</span>' +
            '<span class="u-cover__name">' + esc(cfg.couple.groom.name) + '</span>' +
          '</h1>' +
          (d ? '<p class="u-cover__date"><time datetime="' + d.toISOString() + '">' +
                 esc(fmtDate(d, { day: '2-digit', month: '2-digit', year: 'numeric' })) +
               '</time></p>' : '') +
          '<div class="u-cover__frame">' + photo(s.photo, 'u-cover__photo', 'Foto ' + mono, mono) + '</div>' +
          '<div class="u-cover__guest" id="u-guest" hidden>' +
            '<p class="u-cover__guestlabel">' + esc(s.guestLabel || 'Kepada Yth.') + '</p>' +
            '<p class="u-cover__guestname" id="u-guest-name"></p>' +
          '</div>' +
          '<button class="u-btn u-btn--primary u-cover__open" id="u-open" type="button">' +
            '<span class="u-btn__icon" aria-hidden="true">✦</span>' +
            esc(s.openLabel || 'Buka Undangan') +
          '</button>' +
        '</div>' +
      '</section>';
    },

    quote: function (s) {
      return '' +
      '<section class="u-sec u-quote" data-sec="quote">' + orn() +
        '<div class="u-card u-quote__card u-reveal">' +
          when(s.arabic, function (v) {
            return '<p class="u-quote__arabic" lang="ar" dir="rtl">' + esc(v) + '</p>';
          }) +
          when(s.text, function (v) { return '<p class="u-quote__text">' + esc(v) + '</p>'; }) +
          when(s.cite, function (v) { return '<p class="u-quote__cite">' + esc(v) + '</p>'; }) +
        '</div>' +
      '</section>';
    },

    countdown: function (s, cfg) {
      var d = parseDate(cfg.date);
      if (!d) return '';
      var units = [['days', 'Hari'], ['hours', 'Jam'], ['minutes', 'Menit'], ['seconds', 'Detik']];
      return '' +
      '<section class="u-sec u-countdown" data-sec="countdown" data-target="' + d.toISOString() + '">' + orn() +
        '<div class="u-reveal">' +
          when(s.heading, function (v) { return '<h2 class="u-h2 u-countdown__heading">' + esc(v) + '</h2>'; }) +
          '<div class="u-countdown__grid" role="timer" aria-live="off">' +
            units.map(function (u) {
              return '<div class="u-countdown__unit">' +
                       '<span class="u-countdown__num" data-unit="' + u[0] + '">--</span>' +
                       '<span class="u-countdown__label">' + u[1] + '</span>' +
                     '</div>';
            }).join('<span class="u-countdown__sep" aria-hidden="true">:</span>') +
          '</div>' +
          '<p class="u-countdown__done" hidden>Hari bahagia telah tiba 🤍</p>' +
        '</div>' +
      '</section>';
    },

    couple: function (s, cfg) {
      function person(p, role) {
        return '<div class="u-person u-person--' + role + ' u-reveal">' +
          photo(p.photo, 'u-person__photo', p.full || p.name, (p.name || '?').charAt(0)) +
          '<h3 class="u-person__name">' + esc(p.full || p.name) + '</h3>' +
          when(p.parents, function (v) { return '<p class="u-person__parents">' + esc(v) + '</p>'; }) +
          when(p.instagram, function (v) {
            return '<a class="u-person__ig" href="https://instagram.com/' + escAttr(v) +
                   '" target="_blank" rel="noopener noreferrer">@' + esc(v) + '</a>';
          }) +
        '</div>';
      }
      return '' +
      '<section class="u-sec u-couple" data-sec="couple">' + orn() +
        '<div class="u-card u-couple__card">' +
          when(s.greeting, function (v) {
            return '<p class="u-couple__greeting" lang="ar" dir="rtl">' + esc(v) + '</p>';
          }) +
          when(s.intro, function (v) { return '<p class="u-couple__intro u-reveal">' + esc(v) + '</p>'; }) +
          person(cfg.couple.bride, 'bride') +
          '<div class="u-couple__amp u-reveal" aria-hidden="true">&amp;</div>' +
          person(cfg.couple.groom, 'groom') +
        '</div>' +
      '</section>';
    },

    event: function (s) {
      var start = parseDate(s.start);
      var end = parseDate(s.end);
      var strip = start ? weekStrip(start) : '';
      var time = start ? (fmtTime(start) + (end ? ' – ' + fmtTime(end) : '') + ' ' + TZ_LABEL) : '';
      return '' +
      '<section class="u-sec u-event" data-sec="event">' + orn() +
        '<div class="u-event__inner u-reveal">' +
          when(s.heading, function (v) { return '<h2 class="u-h2 u-event__heading">' + esc(v) + '</h2>'; }) +
          (start ? '<p class="u-event__month">' + esc(fmtDate(start, { month: 'long', year: 'numeric' })) + '</p>' : '') +
          strip +
          '<dl class="u-event__meta">' +
            (time ? '<div class="u-event__row"><dt class="u-event__dt">Waktu</dt>' +
                    '<dd class="u-event__dd">' + esc(time) + '</dd></div>' : '') +
            when(s.venue, function (v) {
              return '<div class="u-event__row"><dt class="u-event__dt">Tempat</dt>' +
                     '<dd class="u-event__dd">' + esc(v) +
                     when(s.address, function (a) { return '<span class="u-event__addr">' + esc(a) + '</span>'; }) +
                     '</dd></div>';
            }) +
          '</dl>' +
          when(s.maps, function (v) {
            return '<a class="u-btn u-btn--ghost u-event__maps" href="' + escAttr(v) +
                   '" target="_blank" rel="noopener noreferrer">' +
                   '<span class="u-btn__icon" aria-hidden="true">◎</span>' +
                   esc(s.mapsLabel || 'Petunjuk Lokasi') + '</a>';
          }) +
          (start ? '<button class="u-btn u-btn--ghost u-event__cal" type="button" data-cal="' +
                   escAttr(JSON.stringify({
                     t: s.heading || 'Wedding', s: s.start, e: s.end, l: s.venue, a: s.address
                   })) + '">' +
                   '<span class="u-btn__icon" aria-hidden="true">+</span>Simpan ke Kalender</button>' : '') +
        '</div>' +
      '</section>';
    },

    gallery: function (s) {
      var photos = Array.isArray(s.photos) ? s.photos : [];
      if (!photos.length) return '';
      return '' +
      '<section class="u-sec u-gallery" data-sec="gallery">' + orn() +
        '<div class="u-reveal">' +
          when(s.heading, function (v) { return '<h2 class="u-h2 u-gallery__heading">' + esc(v) + '</h2>'; }) +
          when(s.caption, function (v) { return '<p class="u-gallery__caption">' + esc(v) + '</p>'; }) +
          '<div class="u-gallery__grid">' +
            photos.map(function (p, i) {
              var src = typeof p === 'string' ? p : p.src;
              var cap = typeof p === 'string' ? '' : (p.caption || '');
              return '<figure class="u-gallery__item" data-i="' + i + '">' +
                       photo(src, 'u-gallery__photo', cap || ('Foto ' + (i + 1)), '') +
                       when(cap, function (c) { return '<figcaption class="u-gallery__cap">' + esc(c) + '</figcaption>'; }) +
                     '</figure>';
            }).join('') +
          '</div>' +
        '</div>' +
      '</section>';
    },

    story: function (s) {
      var items = Array.isArray(s.items) ? s.items : [];
      if (!items.length) return '';
      return '' +
      '<section class="u-sec u-story" data-sec="story">' + orn() +
        when(s.heading, function (v) { return '<h2 class="u-h2 u-story__heading u-reveal">' + esc(v) + '</h2>'; }) +
        '<ol class="u-story__list">' +
          items.map(function (it) {
            return '<li class="u-story__item u-reveal">' +
                     '<span class="u-story__dot" aria-hidden="true"></span>' +
                     when(it.when, function (v) { return '<p class="u-story__when">' + esc(v) + '</p>'; }) +
                     when(it.title, function (v) { return '<h3 class="u-story__title">' + esc(v) + '</h3>'; }) +
                     when(it.text, function (v) { return '<p class="u-story__text">' + esc(v) + '</p>'; }) +
                   '</li>';
          }).join('') +
        '</ol>' +
      '</section>';
    },

    gift: function (s) {
      var accounts = Array.isArray(s.accounts) ? s.accounts : [];
      return '' +
      '<section class="u-sec u-gift" data-sec="gift">' + orn() +
        '<div class="u-card u-gift__card u-reveal">' +
          when(s.heading, function (v) { return '<h2 class="u-h2 u-gift__heading">' + esc(v) + '</h2>'; }) +
          when(s.text, function (v) { return '<p class="u-gift__text">' + esc(v) + '</p>'; }) +
          '<div class="u-gift__list">' +
            accounts.map(function (a) {
              if (a.kind === 'address') {
                return '<div class="u-gift__acct u-gift__acct--addr">' +
                  '<p class="u-gift__bank">' + esc(a.label || 'Alamat Pengiriman Hadiah') + '</p>' +
                  when(a.holder, function (v) { return '<p class="u-gift__holder">' + esc(v) + '</p>'; }) +
                  when(a.address, function (v) { return '<p class="u-gift__addr">' + esc(v) + '</p>'; }) +
                  '<button class="u-btn u-btn--ghost u-copy" type="button" data-copy="' +
                    escAttr((a.holder ? a.holder + ' — ' : '') + (a.address || '')) + '">Salin Alamat</button>' +
                '</div>';
              }
              return '<div class="u-gift__acct">' +
                when(a.bank, function (v) { return '<p class="u-gift__bank">' + esc(v) + '</p>'; }) +
                '<p class="u-gift__num">' + esc(a.number) + '</p>' +
                when(a.holder, function (v) { return '<p class="u-gift__holder">a.n. ' + esc(v) + '</p>'; }) +
                '<button class="u-btn u-btn--ghost u-copy" type="button" data-copy="' +
                  escAttr(a.number) + '">Salin Nomor</button>' +
              '</div>';
            }).join('') +
          '</div>' +
        '</div>' +
      '</section>';
    },

    rsvp: function (s, cfg) {
      var gb = cfg.rsvp && cfg.rsvp.guestbook !== false;
      return '' +
      '<section class="u-sec u-rsvp" data-sec="rsvp" id="u-rsvp">' + orn() +
        '<div class="u-card u-rsvp__card u-reveal">' +
          when(s.heading, function (v) { return '<h2 class="u-h2 u-rsvp__heading">' + esc(v) + '</h2>'; }) +
          when(s.text, function (v) { return '<p class="u-rsvp__text">' + esc(v) + '</p>'; }) +
          '<form class="u-rsvp__form" id="u-rsvp-form" novalidate>' +
            '<div class="u-field">' +
              '<label class="u-label" for="u-rsvp-name">Nama Lengkap</label>' +
              '<input class="u-input" id="u-rsvp-name" name="name" type="text" required ' +
                     'autocomplete="name" maxlength="80" placeholder="Nama Anda">' +
            '</div>' +
            '<fieldset class="u-field u-attend">' +
              '<legend class="u-label">Konfirmasi</legend>' +
              '<div class="u-attend__opts">' +
                '<label class="u-attend__opt"><input type="radio" name="attending" value="yes" required>' +
                  '<span class="u-attend__box"><span class="u-attend__icon" aria-hidden="true">✓</span>Hadir</span></label>' +
                '<label class="u-attend__opt"><input type="radio" name="attending" value="no">' +
                  '<span class="u-attend__box"><span class="u-attend__icon" aria-hidden="true">✕</span>Tidak Hadir</span></label>' +
              '</div>' +
            '</fieldset>' +
            '<div class="u-field u-field--guests">' +
              '<label class="u-label" for="u-rsvp-guests">Jumlah Tamu</label>' +
              '<input class="u-input" id="u-rsvp-guests" name="guests" type="number" min="1" max="10" value="1" inputmode="numeric">' +
            '</div>' +
            '<div class="u-field">' +
              '<label class="u-label" for="u-rsvp-msg">Ucapan &amp; Doa</label>' +
              '<textarea class="u-input u-textarea" id="u-rsvp-msg" name="message" rows="3" ' +
                        'maxlength="500" placeholder="Tulis ucapan untuk kedua mempelai…"></textarea>' +
            '</div>' +
            '<button class="u-btn u-btn--primary u-rsvp__submit" type="submit">Kirim</button>' +
            '<p class="u-rsvp__status" id="u-rsvp-status" role="status" aria-live="polite"></p>' +
          '</form>' +
        '</div>' +
        (gb ? '<div class="u-guestbook u-reveal" id="u-guestbook">' +
                when(s.guestbookHeading, function (v) {
                  return '<h3 class="u-h3 u-guestbook__heading">' + esc(v) + '</h3>';
                }) +
                '<ul class="u-guestbook__list" id="u-guestbook-list"></ul>' +
                '<button class="u-btn u-btn--ghost u-guestbook__more" id="u-guestbook-more" type="button" hidden>' +
                  'Lihat lebih banyak</button>' +
              '</div>' : '') +
      '</section>';
    },

    closing: function (s, cfg) {
      var mono = (cfg.couple.bride.name || '') + ' & ' + (cfg.couple.groom.name || '');
      return '' +
      '<section class="u-sec u-closing" data-sec="closing">' + orn() +
        '<div class="u-closing__inner u-reveal">' +
          '<div class="u-closing__frame">' +
            photo(s.photo, 'u-closing__photo', mono, mono) +
          '</div>' +
          when(s.heading, function (v) { return '<h2 class="u-closing__heading">' + esc(v) + '</h2>'; }) +
          when(s.text, function (v) { return '<p class="u-closing__text">' + esc(v) + '</p>'; }) +
          '<div class="u-closing__seal" aria-hidden="true"></div>' +
          when(s.signoff, function (v) { return '<p class="u-closing__signoff">' + esc(v) + '</p>'; }) +
          '<p class="u-closing__names">' + esc(mono) + '</p>' +
        '</div>' +
      '</section>';
    }
  };

  /** Day-of-week strip with the event day highlighted — a recurring convention
   *  in Indonesian digital invitations, so it lives in the engine, not a theme. */
  function weekStrip(d) {
    var w = wallClock(d);                 // calendar maths in the wedding's timezone
    var monday = new Date(w);
    monday.setDate(w.getDate() - ((w.getDay() + 6) % 7));   // 0 = Sunday
    var out = '';
    for (var i = 0; i < 7; i++) {
      var cur = new Date(monday);
      cur.setDate(monday.getDate() + i);
      var active = cur.toDateString() === w.toDateString();
      out += '<div class="u-week__day' + (active ? ' is-active' : '') + '">' +
               '<span class="u-week__dow">' + esc(fmtLocal(cur, { weekday: 'short' })) + '</span>' +
               '<span class="u-week__num">' + pad(cur.getDate()) + '</span>' +
             '</div>';
    }
    return '<div class="u-week" role="img" aria-label="Tanggal acara: ' +
           esc(fmtDate(d, { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' })) +
           '">' + out + '</div>';
  }

  /* -------------------------------------------------------- rsvp adapters */

  var Adapters = {
    /** No backend. Persists to localStorage so the template is fully
     *  demonstrable offline and sellable before a customer has any hosting. */
    demo: function () {
      var KEY = 'undangan.rsvp';
      function read() {
        try { return JSON.parse(localStorage.getItem(KEY) || '[]'); } catch (e) { return []; }
      }
      return {
        list: function () { return Promise.resolve(read()); },
        submit: function (entry) {
          var all = read();
          all.unshift(entry);
          try { localStorage.setItem(KEY, JSON.stringify(all.slice(0, 200))); } catch (e) {}
          return Promise.resolve(entry);
        }
      };
    },

    /** Google Apps Script web app bound to a Sheet. Sent as form-encoded so the
     *  browser skips the CORS preflight Apps Script cannot answer. */
    script: function (cfg) {
      var url = cfg.endpoint;
      return {
        list: function () {
          return fetch(url + (url.indexOf('?') < 0 ? '?' : '&') + 'action=list')
            .then(function (r) { return r.json(); })
            .then(function (j) { return Array.isArray(j) ? j : (j.data || []); })
            .catch(function () { return []; });
        },
        submit: function (entry) {
          var body = new URLSearchParams();
          Object.keys(entry).forEach(function (k) { body.append(k, entry[k]); });
          return fetch(url, { method: 'POST', body: body }).then(function (r) {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return entry;
          });
        }
      };
    },

    /** Supabase REST. Requires an anon key with RLS: insert allowed, select
     *  allowed, update/delete denied. */
    supabase: function (cfg) {
      var url = cfg.endpoint, key = cfg.key, table = cfg.table || 'rsvp';
      var base = url.replace(/\/$/, '') + '/rest/v1/' + table;
      var headers = { apikey: key, Authorization: 'Bearer ' + key, 'Content-Type': 'application/json' };
      return {
        list: function () {
          return fetch(base + '?select=*&order=created_at.desc&limit=200', { headers: headers })
            .then(function (r) { return r.json(); })
            .catch(function () { return []; });
        },
        submit: function (entry) {
          return fetch(base, {
            method: 'POST',
            headers: Object.assign({}, headers, { Prefer: 'return=minimal' }),
            body: JSON.stringify(entry)
          }).then(function (r) {
            if (!r.ok) throw new Error('HTTP ' + r.status);
            return entry;
          });
        }
      };
    }
  };

  /* ------------------------------------------------------------ behaviours */

  function guestName(cfg) {
    var params = new URLSearchParams(location.search);
    var name = params.get('to') || params.get('u') || params.get('kepada');
    if (has(name)) return name;
    // Falls back to cover.guestFallback so one generic link (broadcast to a
    // group, or a preview) still reads as an invitation rather than showing
    // an empty slot where a name belongs.
    var cover = (cfg.sections || []).filter(function (s) { return s.type === 'cover'; })[0];
    return cover && has(cover.guestFallback) ? cover.guestFallback : '';
  }

  function initGuest(cfg) {
    var name = guestName(cfg);
    if (!has(name)) return;
    var box = qs('#u-guest'), out = qs('#u-guest-name');
    if (!box || !out) return;
    out.textContent = name;           // textContent — never innerHTML for URL input
    box.hidden = false;
    document.documentElement.classList.add('has-guest');
  }

  function initCover(cfg) {
    var btn = qs('#u-open');
    var root = document.documentElement;
    root.classList.add('is-locked');
    if (!btn) { root.classList.remove('is-locked'); return; }
    btn.addEventListener('click', function () {
      root.classList.remove('is-locked');
      root.classList.add('is-open');
      var next = qs('.u-sec:not(.u-cover)');
      if (next) next.scrollIntoView({ behavior: 'smooth', block: 'start' });
      startMusic();
    }, { once: true });
  }

  var audio = null;
  function initMusic(cfg) {
    if (!cfg.music || !has(cfg.music.src)) return;
    audio = new Audio(cfg.music.src);
    audio.loop = true;
    audio.preload = 'none';
    var btn = el('<button class="u-music" id="u-music" type="button" aria-pressed="false" ' +
                 'aria-label="' + esc(cfg.music.label || 'Putar musik') + '">' +
                 '<span class="u-music__icon" aria-hidden="true"></span></button>');
    document.body.appendChild(btn);
    btn.addEventListener('click', function () {
      if (audio.paused) startMusic(); else stopMusic();
    });
  }
  function startMusic() {
    if (!audio) return;
    audio.play().then(function () {
      document.documentElement.classList.add('is-playing');
      var b = qs('#u-music'); if (b) b.setAttribute('aria-pressed', 'true');
    }).catch(function () { /* autoplay blocked — the button still works */ });
  }
  function stopMusic() {
    if (!audio) return;
    audio.pause();
    document.documentElement.classList.remove('is-playing');
    var b = qs('#u-music'); if (b) b.setAttribute('aria-pressed', 'false');
  }

  function initCountdown() {
    var sec = qs('.u-countdown');
    if (!sec) return;
    var target = new Date(sec.getAttribute('data-target')).getTime();
    var nums = {};
    qsa('[data-unit]', sec).forEach(function (n) { nums[n.getAttribute('data-unit')] = n; });
    var done = qs('.u-countdown__done', sec);
    var grid = qs('.u-countdown__grid', sec);

    function tick() {
      var diff = target - Date.now();
      if (diff <= 0) {
        Object.keys(nums).forEach(function (k) { nums[k].textContent = '00'; });
        if (done) done.hidden = false;
        if (grid) grid.hidden = true;
        clearInterval(timer);
        return;
      }
      var s = Math.floor(diff / 1000);
      nums.days.textContent = pad(Math.floor(s / 86400));
      nums.hours.textContent = pad(Math.floor(s % 86400 / 3600));
      nums.minutes.textContent = pad(Math.floor(s % 3600 / 60));
      nums.seconds.textContent = pad(s % 60);
    }
    tick();
    var timer = setInterval(tick, 1000);
  }

  function initReveal() {
    var items = qsa('.u-reveal');
    if (!('IntersectionObserver' in window) ||
        window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
      items.forEach(function (n) { n.classList.add('is-in'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); }
      });
    }, { rootMargin: '0px 0px -12% 0px', threshold: 0.08 });
    items.forEach(function (n) { io.observe(n); });
  }

  function initCopy() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('.u-copy') : null;
      if (!btn) return;
      var text = btn.getAttribute('data-copy') || '';
      var done = function () {
        var old = btn.textContent;
        btn.textContent = 'Tersalin ✓';
        btn.classList.add('is-copied');
        setTimeout(function () { btn.textContent = old; btn.classList.remove('is-copied'); }, 1800);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, fallback);
      } else { fallback(); }
      function fallback() {
        var ta = document.createElement('textarea');
        ta.value = text; ta.setAttribute('readonly', '');
        ta.style.cssText = 'position:absolute;left:-9999px';
        document.body.appendChild(ta); ta.select();
        try { document.execCommand('copy'); done(); } catch (err) {}
        document.body.removeChild(ta);
      }
    });
  }

  function initCalendar() {
    document.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('[data-cal]') : null;
      if (!btn) return;
      var d;
      try { d = JSON.parse(btn.getAttribute('data-cal')); } catch (err) { return; }
      var start = parseDate(d.s), end = parseDate(d.e) || (start && new Date(start.getTime() + 7200000));
      if (!start) return;
      var z = function (dt) { return dt.toISOString().replace(/[-:]|\.\d{3}/g, ''); };
      var url = 'https://calendar.google.com/calendar/render?action=TEMPLATE' +
        '&text=' + encodeURIComponent(d.t || 'Wedding') +
        '&dates=' + z(start) + '/' + z(end) +
        '&location=' + encodeURIComponent([d.l, d.a].filter(Boolean).join(', '));
      window.open(url, '_blank', 'noopener');
    });
  }

  function initRsvp(cfg) {
    var form = qs('#u-rsvp-form');
    if (!form) return;
    var conf = cfg.rsvp || {};
    var make = Adapters[conf.adapter] || Adapters.demo;
    var adapter = make(conf);
    var status = qs('#u-rsvp-status');
    var list = qs('#u-guestbook-list');
    var more = qs('#u-guestbook-more');
    var PAGE = 5, shown = PAGE, entries = [];

    var guest = guestName(cfg);
    if (has(guest)) qs('#u-rsvp-name').value = guest;

    function render() {
      if (!list) return;
      var slice = entries.slice(0, shown);
      list.innerHTML = slice.length
        ? slice.map(function (e) {
            var att = e.attending === 'no' ? 'no' : 'yes';
            return '<li class="u-guestbook__item is-' + att + '">' +
                     '<div class="u-guestbook__head">' +
                       '<span class="u-guestbook__name">' + esc(e.name) + '</span>' +
                       '<span class="u-guestbook__badge">' + (att === 'yes' ? 'Hadir' : 'Tidak hadir') + '</span>' +
                     '</div>' +
                     (has(e.message) ? '<p class="u-guestbook__msg">' + esc(e.message) + '</p>' : '') +
                   '</li>';
          }).join('')
        : '<li class="u-guestbook__empty">Belum ada ucapan. Jadilah yang pertama 🤍</li>';
      if (more) more.hidden = entries.length <= shown;
    }

    if (more) {
      more.addEventListener('click', function () { shown += PAGE; render(); });
    }

    adapter.list().then(function (data) {
      entries = Array.isArray(data) ? data : [];
      render();
    });

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var fd = new FormData(form);
      var entry = {
        name: String(fd.get('name') || '').trim(),
        attending: String(fd.get('attending') || ''),
        guests: String(fd.get('guests') || '1'),
        message: String(fd.get('message') || '').trim(),
        created_at: new Date().toISOString()
      };
      if (!entry.name) { setStatus('Nama masih kosong.', 'error'); return; }
      if (!entry.attending) { setStatus('Pilih konfirmasi kehadiran dulu.', 'error'); return; }

      var btn = qs('.u-rsvp__submit', form);
      btn.disabled = true;
      setStatus('Mengirim…', 'pending');

      adapter.submit(entry).then(function () {
        setStatus('Terima kasih, konfirmasi Anda tercatat 🤍', 'ok');
        entries.unshift(entry);
        render();
        form.reset();
        if (has(guest)) qs('#u-rsvp-name').value = guest;
      }).catch(function () {
        setStatus('Gagal mengirim. Cek koneksi lalu coba lagi.', 'error');
      }).then(function () { btn.disabled = false; });
    });

    function setStatus(msg, kind) {
      if (!status) return;
      status.textContent = msg;
      status.className = 'u-rsvp__status is-' + kind;
    }
  }

  /* ------------------------------------------------------------------ boot */

  function applyMeta(cfg) {
    var m = cfg.meta || {};
    if (has(m.locale)) LOCALE = m.locale;
    if (has(m.timezone)) TZ = m.timezone;
    if (has(m.timezoneLabel)) TZ_LABEL = m.timezoneLabel;
    if (has(m.title)) document.title = m.title;
    if (has(m.description)) {
      var tag = qs('meta[name="description"]') ||
                document.head.appendChild(el('<meta name="description">'));
      tag.setAttribute('content', m.description);
    }
  }

  function loadTheme(name) {
    if (!has(name) || qs('link[data-theme]')) return Promise.resolve();
    return new Promise(function (resolve) {
      var link = el('<link rel="stylesheet" data-theme="' + escAttr(name) +
                    '" href="themes/' + escAttr(name) + '/theme.css">');
      link.addEventListener('load', resolve);
      link.addEventListener('error', resolve);   // never block render on a theme
      document.head.appendChild(link);
    });
  }

  function render(cfg, mount) {
    var known = Object.keys(Sections);
    var html = (cfg.sections || []).map(function (s) {
      var fn = Sections[s.type];
      if (!fn) {
        console.warn('[undangan] unknown section type "' + s.type + '". Known:', known.join(', '));
        return '';
      }
      return fn(s, cfg);
    }).join('');
    mount.innerHTML = html;
  }

  function normalise(cfg) {
    cfg.couple = cfg.couple || {};
    cfg.couple.bride = cfg.couple.bride || {};
    cfg.couple.groom = cfg.couple.groom || {};
    cfg.sections = Array.isArray(cfg.sections) ? cfg.sections : [];
    cfg.rsvp = cfg.rsvp || { adapter: 'demo' };
    return cfg;
  }

  function mountAll(cfg, mount) {
    normalise(cfg);
    applyMeta(cfg);
    render(cfg, mount);
    initGuest(cfg);
    initCover(cfg);
    initMusic(cfg);
    initCountdown();
    initReveal();
    initCopy();
    initCalendar();
    initRsvp(cfg);
    document.documentElement.classList.add('is-ready');
  }

  var Undangan = {
    sections: Sections,
    adapters: Adapters,

    /** Register a custom section type. Themes that ship extra sections call
     *  this before init(). */
    register: function (type, fn) { Sections[type] = fn; return this; },

    init: function (opts) {
      opts = opts || {};
      var mount = typeof opts.mount === 'string' ? qs(opts.mount) : (opts.mount || qs('#app'));
      if (!mount) throw new Error('[undangan] mount element not found');

      var get = opts.data
        ? Promise.resolve(opts.data)
        : fetch(opts.src || 'data/demo.json').then(function (r) {
            if (!r.ok) throw new Error('Cannot load ' + (opts.src || 'data/demo.json') + ': HTTP ' + r.status);
            return r.json();
          });

      return get.then(function (cfg) {
        return loadTheme(opts.theme || cfg.theme).then(function () {
          mountAll(cfg, mount);
          return cfg;
        });
      }).catch(function (err) {
        console.error('[undangan]', err);
        mount.innerHTML = '<div class="u-error"><p>Undangan gagal dimuat.</p><code>' +
                          esc(err.message) + '</code></div>';
        throw err;
      });
    }
  };

  window.Undangan = Undangan;
})();
