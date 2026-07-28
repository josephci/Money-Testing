/* Battery Prices — cordless tool batteries ranked by real $/Wh.
 *
 * Data comes from window.__DATA__ when the page has been through build.py
 * (single-file deploy), otherwise it is fetched from ./data/batteries.json.
 */

const STALE_HOURS = 24; // Amazon's operating agreement caps displayed price age at 24h.

const el = {
  banners: document.getElementById('banners'),
  rows: document.getElementById('rows'),
  table: document.getElementById('table'),
  empty: document.getElementById('empty'),
  summary: document.getElementById('summary'),
  stamp: document.getElementById('stamp'),
  q: document.getElementById('q'),
  sort: document.getElementById('sort'),
  minAh: document.getElementById('minAh'),
  packs: document.getElementById('packs'),
  platformList: document.getElementById('platformList'),
  allPlatforms: document.getElementById('allPlatforms'),
  nonePlatforms: document.getElementById('nonePlatforms'),
};

let DATA = null;
let ITEMS = [];

/* ---------- derive ---------- */

// Everything the table shows is computed here, once, from nominal voltage.
function enrich(raw) {
  const platform = raw.platforms[raw.item.platform];
  const b = raw.item;

  const computedWh = platform.nominal_volts * b.amp_hours;
  const perPackWh = b.rated_wh != null ? b.rated_wh : computedWh;
  const totalWh = perPackWh * b.pack_count;
  const totalAh = b.amp_hours * b.pack_count;

  // If the manufacturer's published Wh disagrees with nominal V x Ah, one of the
  // two is wrong in our data. Surface it rather than silently trusting either.
  const drift = b.rated_wh != null ? Math.abs(b.rated_wh - computedWh) : 0;
  const mismatch = drift > Math.max(1, computedWh * 0.02);

  const hasPrice = typeof b.price === 'number' && b.price > 0;

  return {
    ...b,
    platformKey: b.platform,
    platform,
    perPackWh,
    totalWh,
    totalAh,
    computedWh,
    mismatch,
    hasPrice,
    perWh: hasPrice ? b.price / totalWh : null,
    perAh: hasPrice ? b.price / totalAh : null,
    haystack: [platform.brand, platform.name, b.model, b.name].join(' ').toLowerCase(),
  };
}

/* ---------- format ---------- */

const money = (n) => '$' + n.toFixed(2);
const cents = (n) => '$' + n.toFixed(3);
const num = (n) => (Number.isInteger(n) ? String(n) : n.toFixed(1));

function hoursSince(iso) {
  if (!iso) return Infinity;
  const t = Date.parse(iso);
  return Number.isNaN(t) ? Infinity : (Date.now() - t) / 3.6e6;
}

/* ---------- banners ---------- */

function renderBanners() {
  const out = [];

  if (DATA.meta.price_source === 'sample') {
    out.push(
      `<div class="banner"><strong>Sample data.</strong> These prices are placeholders and the
       specs are unverified. Run <code>scripts/update_prices.py</code> with real listings before
       this page goes anywhere near a visitor.</div>`
    );
  }

  const stale = ITEMS.filter((i) => i.hasPrice && hoursSince(i.checked_at) > STALE_HOURS).length;
  if (DATA.meta.price_source !== 'sample' && stale > 0) {
    out.push(
      `<div class="banner"><strong>${stale} price${stale === 1 ? '' : 's'} older than
       ${STALE_HOURS}h.</strong> Amazon's operating agreement requires displayed prices to be
       refreshed at least daily. Re-run the updater.</div>`
    );
  }

  el.banners.innerHTML = out.join('');
}

/* ---------- platform filter ---------- */

function renderPlatformFilter() {
  const keys = Object.keys(DATA.platforms).sort((a, b) => {
    const pa = DATA.platforms[a], pb = DATA.platforms[b];
    return pa.brand.localeCompare(pb.brand) || pa.name.localeCompare(pb.name);
  });

  el.platformList.innerHTML = keys
    .map((k) => {
      const p = DATA.platforms[k];
      const n = ITEMS.filter((i) => i.platformKey === k).length;
      return `<label title="${escapeAttr(p.note || '')}">
        <input type="checkbox" value="${k}" checked>
        <span>${escapeHtml(p.brand)} ${escapeHtml(p.name)}</span>
        <span class="plat-name">${n}</span>
      </label>`;
    })
    .join('');

  el.platformList.addEventListener('change', render);
  el.allPlatforms.addEventListener('click', () => setAllPlatforms(true));
  el.nonePlatforms.addEventListener('click', () => setAllPlatforms(false));
}

function setAllPlatforms(on) {
  el.platformList.querySelectorAll('input').forEach((i) => (i.checked = on));
  render();
}

function selectedPlatforms() {
  return new Set(
    [...el.platformList.querySelectorAll('input:checked')].map((i) => i.value)
  );
}

/* ---------- render ---------- */

function render() {
  const q = el.q.value.trim().toLowerCase();
  const minAh = parseFloat(el.minAh.value);
  const packs = el.packs.value;
  const plats = selectedPlatforms();

  let list = ITEMS.filter((i) => {
    if (!plats.has(i.platformKey)) return false;
    if (i.amp_hours < minAh) return false;
    if (packs === '1' && i.pack_count !== 1) return false;
    if (packs === '2' && i.pack_count < 2) return false;
    if (q && !i.haystack.includes(q)) return false;
    return true;
  });

  const key = el.sort.value;
  const asc = key === 'perWh' || key === 'perAh' || key === 'price';
  list.sort((a, b) => {
    const va = sortValue(a, key), vb = sortValue(b, key);
    if (va === null) return 1; // rows without a price always sink
    if (vb === null) return -1;
    return asc ? va - vb : vb - va;
  });

  // Cheapest $/Wh within each platform — the number someone locked into a
  // battery system actually cares about.
  const best = new Map();
  for (const i of list) {
    if (!i.hasPrice) continue;
    const cur = best.get(i.platformKey);
    if (!cur || i.perWh < cur) best.set(i.platformKey, i.perWh);
  }

  el.rows.innerHTML = list.map((i) => row(i, best.get(i.platformKey) === i.perWh)).join('');
  el.empty.hidden = list.length > 0;
  el.table.hidden = list.length === 0;

  const priced = list.filter((i) => i.hasPrice);
  const cheapest = priced.length ? Math.min(...priced.map((i) => i.perWh)) : null;
  el.summary.textContent =
    `${list.length} of ${ITEMS.length} batteries` +
    (cheapest !== null ? ` · best value ${cents(cheapest)}/Wh` : '');
}

function sortValue(i, key) {
  switch (key) {
    case 'perWh': return i.perWh;
    case 'perAh': return i.perAh;
    case 'price': return i.hasPrice ? i.price : null;
    case 'wh': return i.totalWh;
    case 'ah': return i.totalAh;
    default: return null;
  }
}

function row(i, isBest) {
  const p = i.platform;

  const vCell = p.marketing_volts !== p.nominal_volts
    ? `<span class="vmark" title="Sold as ${p.marketing_volts}V. ${escapeAttr(p.note || '')}">${p.nominal_volts}</span>`
    : String(p.nominal_volts);

  const badges = [
    isBest ? '<span class="badge badge-best">best $/Wh</span>' : '',
    i.pack_count > 1 ? `<span class="badge badge-packs">${i.pack_count}-pack</span>` : '',
    i.mismatch
      ? `<span class="badge badge-warn" title="Published rating ${i.rated_wh}Wh but ${p.nominal_volts}V x ${i.amp_hours}Ah = ${i.computedWh.toFixed(1)}Wh. Check the spec sheet.">check</span>`
      : '',
  ].join('');

  const buy = i.url
    ? `<a class="buy" href="${escapeAttr(i.url)}" rel="nofollow sponsored noopener" target="_blank">Buy</a>`
    : `<a class="buy" aria-disabled="true" href="#">Buy</a>`;

  return `<tr class="${isBest ? 'is-best' : ''}">
    <td class="col-plat"><span class="brand">${escapeHtml(p.brand)}</span><br><span class="plat-name">${escapeHtml(p.name)}</span></td>
    <td class="col-model"><span class="name">${escapeHtml(i.name)}${badges}</span><span class="model">${escapeHtml(i.model)}</span></td>
    <td class="num">${num(i.amp_hours)}</td>
    <td class="num">${vCell}</td>
    <td class="num">${num(i.totalWh)}</td>
    <td class="num">${i.hasPrice ? money(i.price) : '—'}</td>
    <td class="num perwh">${i.perWh !== null ? cents(i.perWh) : '—'}</td>
    <td class="num">${i.perAh !== null ? money(i.perAh) : '—'}</td>
    <td class="col-buy">${buy}</td>
  </tr>`;
}

/* ---------- escaping ---------- */

function escapeHtml(s) {
  return String(s).replace(/[&<>"']/g, (c) =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])
  );
}
const escapeAttr = escapeHtml;

/* ---------- boot ---------- */

async function boot() {
  try {
    DATA = window.__DATA__ || (await fetch('data/batteries.json').then((r) => {
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return r.json();
    }));
  } catch (err) {
    el.banners.innerHTML =
      `<div class="banner"><strong>Could not load data.</strong> ${escapeHtml(err.message)}.
       Opening this file directly with <code>file://</code> will not work — run
       <code>python3 -m http.server</code> from the project root instead.</div>`;
    return;
  }

  ITEMS = DATA.batteries.map((item) => enrich({ item, platforms: DATA.platforms }));

  renderBanners();
  renderPlatformFilter();

  el.stamp.textContent = DATA.meta.generated_at
    ? `Last updated ${new Date(DATA.meta.generated_at).toLocaleString()}.`
    : '';

  ['input', 'change'].forEach((ev) => {
    el.q.addEventListener(ev, render);
  });
  [el.sort, el.minAh, el.packs].forEach((n) => n.addEventListener('change', render));

  render();
}

boot();
