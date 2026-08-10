/*
 * trumper.go — renders content.js into index.html.
 *
 * No framework, no build step, no network calls. Content is set as text
 * rather than HTML, so a stray character in a post can never break the page.
 */

(function () {
  'use strict';

  const $ = (id) => document.getElementById(id);

  const el = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text != null) node.textContent = text;
    return node;
  };

  // 'YYYY-MM-DD' -> 'Aug 9, 2026'. Split by hand: `new Date('2026-08-09')`
  // parses as UTC and can render as the previous day west of Greenwich.
  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

  function formatDate(iso) {
    const parts = String(iso).split('-');
    if (parts.length !== 3) return String(iso);
    const month = MONTHS[Number(parts[1]) - 1];
    if (!month) return String(iso);
    return month + ' ' + Number(parts[2]) + ', ' + parts[0];
  }

  function renderHeader(meta) {
    document.title = meta.domain + ' — ' + meta.tagline.replace(/\.$/, '');

    // Wordmark: name in white, TLD in orange. Split on the last dot so the
    // domain stays a single string in content.js. Uppercasing is done in CSS,
    // so the underlying text is still the real lowercase domain.
    const dot = meta.domain.lastIndexOf('.');
    const name = dot === -1 ? meta.domain : meta.domain.slice(0, dot);
    const tld = dot === -1 ? '' : meta.domain.slice(dot);

    const wordmark = $('domain');
    wordmark.textContent = '';
    wordmark.appendChild(el('span', 'w-name', name));
    if (tld) wordmark.appendChild(el('span', 'w-tld', tld));

    $('tagline').textContent = meta.tagline;
    $('bio').textContent = meta.bio;
    $('updated').textContent = meta.updated;
    const footer = document.querySelector('.footer-domain');
    if (footer) footer.textContent = meta.domain;
  }

  function renderStory(paragraphs) {
    const host = $('story-body');
    paragraphs.forEach((text) => host.appendChild(el('p', null, text)));
  }

  function renderPosts(posts) {
    const host = $('posts');

    if (!posts.length) {
      host.appendChild(el('p', 'empty', 'Nothing posted yet. Check back.'));
      return;
    }

    posts.forEach((post) => {
      const card = el('article', 'post');

      const meta = el('div', 'post-meta');
      const kind = post.kind === 'link' ? 'link' : 'take';
      meta.appendChild(el('span', 'kind kind-' + kind, kind));
      meta.appendChild(el('time', null, formatDate(post.date)));
      card.appendChild(meta);

      card.appendChild(el('h3', null, post.title));
      card.appendChild(el('p', null, post.body));

      if (post.source && post.source.url) {
        const link = el('a', 'source', post.source.label || 'Read it');
        link.href = post.source.url;
        link.rel = 'noopener noreferrer';
        link.target = '_blank';
        card.appendChild(link);
      }

      host.appendChild(card);
    });
  }

  function renderWallets(wallets) {
    if (!wallets || !wallets.live) return;

    $('wallet-note').textContent = wallets.note || '';

    const list = $('wallet-list');
    wallets.addresses.forEach((entry) => {
      const row = el('li');
      row.appendChild(el('span', 'chain', entry.chain));
      row.appendChild(el('span', 'addr', entry.address));
      list.appendChild(row);
    });

    $('wallets').hidden = false;
  }

  function renderLinks(links) {
    const host = $('links');

    links.forEach((entry) => {
      const row = el('li');
      row.appendChild(el('span', 'label', entry.label));

      if (entry.url) {
        const link = el('a', 'handle', entry.handle);
        link.href = entry.url;
        link.rel = 'noopener noreferrer';
        link.target = '_blank';
        row.appendChild(link);
      } else {
        row.appendChild(el('span', 'handle', entry.handle));
        row.appendChild(document.createTextNode(' '));
        row.appendChild(el('span', 'soon', '— not live yet'));
      }

      host.appendChild(row);
    });
  }

  function renderStanding(lines) {
    const host = $('standing-list');
    lines.forEach((line) => host.appendChild(el('li', null, line)));
  }

  renderHeader(SITE.meta);
  renderStory(SITE.story);
  renderPosts(SITE.posts);
  renderWallets(SITE.wallets);
  renderLinks(SITE.links);
  renderStanding(SITE.standing);
})();
