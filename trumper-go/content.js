/*
 * trumper.go — all site content lives here.
 *
 * Edit this file to update the site. Nothing else needs to change for
 * content edits: index.html is the layout, app.js renders this object into it.
 */

const SITE = {
  meta: {
    domain: 'trumper.go',
    tagline: 'For the ones who show up.',
    bio: 'Straight talk on Trump, crypto, and the fights that actually matter.',
    // Shown in the footer. Update when you publish.
    updated: 'August 2026',
  },

  /*
   * The short story. Three or four sentences, max. If it takes longer than
   * that to explain, it is not clear enough yet.
   */
  story: [
    'This is a home base for regular people who back Trump and are trying to make sense of crypto at the same time.',
    'No insiders. No newsletter funnel. No one here is going to tell you what to buy.',
    'Just headlines worth reading, takes worth arguing about, and a place that belongs to the people who show up for it.',
  ],

  /*
   * Latest takes and curated headlines. Newest first.
   *
   * date:   ISO date string, e.g. '2026-08-09'
   * kind:   'take' (yours) or 'link' (something you are pointing at)
   * title:  short. Say the thing.
   * body:   two or three sentences.
   * source: optional { label, url } — required for kind: 'link'
   */
  posts: [
    {
      date: '2026-08-09',
      kind: 'take',
      title: 'Why this site exists',
      body:
        'Everybody with a keyboard is selling something. Half the crypto accounts you follow ' +
        'are paid. The other half are exit liquidity and do not know it yet. This is the ' +
        'opposite of that: a place to read, think, and argue without someone reaching for ' +
        'your wallet at the end of the paragraph.',
    },
    {
      date: '2026-08-09',
      kind: 'take',
      title: 'The lesson of the official coin',
      body:
        'A political token launched, ran hard, and came back down. Insiders held most of the ' +
        'supply. Regular buyers ate the drop. That is not a conspiracy theory, it is a chart. ' +
        'Remember it the next time someone waves a flag at you and points at a buy button.',
    },
  ],

  /*
   * Web3 domain wallet addresses. Anyone can look these up from trumper.go
   * and send directly — no exchange, no middleman.
   *
   * Fill in the real addresses, then set `live: true` to show this section.
   * Leave `live: false` while they are placeholders.
   */
  wallets: {
    live: false,
    note: 'Records set on the domain itself. Verify on Unstoppable before you send anything.',
    addresses: [
      { chain: 'SOL', address: 'not set yet' },
      { chain: 'ETH', address: 'not set yet' },
      { chain: 'BTC', address: 'not set yet' },
    ],
  },

  /*
   * Where the community lives. Set url to null to hide a row until it exists.
   */
  links: [
    { label: 'X', handle: '@trumpergo', url: null },
    { label: 'Telegram', handle: 't.me/trumpergo', url: null },
  ],

  /*
   * Plain-language standing. Keep this honest and keep it current — it is the
   * single most useful thing on the page for anyone deciding whether to trust it.
   */
  standing: [
    'There is no token. Nothing on this site is for sale.',
    'Nobody here is paid to post about a coin, and no one is running an affiliate link.',
    'If any of that ever changes, it gets said here first, in plain English, before anywhere else.',
    'Nothing on this site is financial advice. Do your own homework before you spend a dollar.',
  ],
};
