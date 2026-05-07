# CLAUDE.md

Personal portfolio site of Jake Wu (吴启杰). Astro 6 + Tailwind v4, deployed to GitHub Pages from `main`.

- Live: https://jakewqj.github.io/portfolio/
- Resume (semi-private slug): https://jakewqj.github.io/portfolio/resume/jw-e2665966/
- Repo: public

## Stack

- Astro 6 (static output, content collections)
- Tailwind v4 via `@tailwindcss/vite` (CSS-first, no `tailwind.config.js`)
- TypeScript strict
- Node ≥ 22.12 required
- GitHub Actions: `withastro/action@v3` (Node 22 pinned) → `actions/deploy-pages@v4`

## Commands

```sh
npm install
npm run dev      # http://localhost:4321/portfolio/
npm run build    # ./dist/
npm run preview
```

## Structure

```
src/
├── content.config.ts          # zod schemas for content collections
├── content/
│   └── resume/
│       ├── zh.md              # entry id "zh"
│       └── en.md              # entry id "en"
├── components/
│   ├── ContactReveal.astro    # click-to-reveal email/phone (split + base64)
│   ├── LangToggle.astro       # ZH/EN switcher, localStorage-backed
│   └── PrintButton.astro
├── layouts/
│   ├── Base.astro             # html shell, noindex meta, lang init script
│   └── ResumeLayout.astro     # resume-specific frame
├── pages/
│   ├── index.astro            # / landing
│   ├── 404.astro
│   └── resume/
│       └── jw-e2665966/       # random hash slug — rotate by renaming this dir
│           └── index.astro
└── styles/
    └── global.css             # tailwind import + .resume-prose + @media print
```

## Content collection IDs

`getEntry('resume', 'zh' | 'en')`. **File names must be flat (`zh.md`), not dotted (`jake-wu.zh.md`).** Astro's glob loader treats dots in filenames in a way that broke the lookup — keep IDs simple.

To add a new collection (writing / coverage / work):

1. Add a `defineCollection({ loader: glob({ pattern, base }), schema })` in `src/content.config.ts`
2. Drop markdown files under `src/content/<type>/`
3. Add list page at `src/pages/<type>/index.astro` (use `getCollection('<type>')`) and detail page at `src/pages/<type>/[...slug].astro`

## Bilingual rendering

Both ZH and EN markdown render into the same page, wrapped in `<div data-lang-section="zh">` / `<div data-lang-section="en">`. CSS in `global.css` hides the inactive section based on `<html data-lang>`. `LangToggle.astro` flips the attribute and persists to `localStorage`. Default language detected from `navigator.language`.

When editing the resume, **edit both `zh.md` and `en.md`** to keep them in sync. The English file is currently a Claude-translated draft Jake reviews directly.

## Privacy model

This is **semi-private**, not authenticated. Three layers:

1. `<meta name="robots" content="noindex,nofollow,noarchive">` set in `src/layouts/Base.astro` — applies site-wide
2. `public/robots.txt` with `Disallow: /` — blocks crawlers
3. Random hash slug `jw-e2665966` for the resume URL — relies on URL secrecy

If a future collection (e.g. writing) should be search-indexable, override the `<meta name="robots">` for those pages by adding a per-page meta or by branching `Base.astro`.

To rotate the resume slug:

```sh
node -e "console.log('jw-' + require('crypto').randomBytes(4).toString('hex'))"
# rename src/pages/resume/<old>/ → src/pages/resume/<new>/
git push
```

## Contact obfuscation

Email is split into `emailParts: [local, domain]` in frontmatter; phone is stored as `phoneFull` and emitted as base64 in a `data-phone-b64` attr. `ContactReveal.astro` reassembles on click. Net result: `grep "13570340684" dist/` returns 0. Don't undo this by inlining the values in markdown body.

## Frontmatter schema

Resume markdown frontmatter (validated by zod in `content.config.ts`):

```yaml
name: 吴启杰
nameEn: Jake Wu
title: 高级品牌公关经理        # role/title in this language
location: 广州
tagline: 中英双语
emailParts: ["jake.wu", "donnermusic.com"]
phoneFull: "+8613570340684"
phoneObfuscated: "+86 13570 ••• 0684"
linkedin: "https://www.linkedin.com/in/jake-wu-qijie/"
lang: zh                          # 'zh' | 'en'
```

## Deployment

Pushes to `main` (or manual `workflow_dispatch`) trigger `.github/workflows/deploy.yml`. Build step needs `node-version: 22` explicitly — `withastro/action@v3` defaults to Node 20, which fails Astro 6's `>=22.12` engine check.

GitHub Pages source must be set to **GitHub Actions** (not branch). One-time setup; already configured.

## Build config

`astro.config.mjs` sets:

- `site: 'https://jakewqj.github.io'`
- `base: '/portfolio'` — all internal asset URLs use `import.meta.env.BASE_URL`
- `build.format: 'directory'` — produces `/resume/<slug>/index.html` (clean URLs)

## Don't

- Don't put plain emails or phone digits in markdown bodies — use the frontmatter fields and `ContactReveal`.
- Don't use dotted filenames in `src/content/` — collection IDs break.
- Don't skip the `node-version: 22` pin in CI.
- Don't add a `<meta name="description">` revealing the resume URL on the landing page — keeps slug discovery harder.
