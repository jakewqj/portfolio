# portfolio

Personal portfolio of Jake Wu (吴启杰), built with [Astro](https://astro.build) and Tailwind CSS, deployed to GitHub Pages.

## URLs

- Public landing: https://jakewqj.github.io/portfolio/
- Resume (semi-private): https://jakewqj.github.io/portfolio/resume/jw-e2665966/

The resume URL uses a random hash slug. The site sets `noindex,nofollow` and serves a `robots.txt` that disallows all crawlers, so the link is "share-only" — anyone with the URL can read it, but it should not appear in search results.

To rotate the slug, generate a new one and rename the directory:

```sh
node -e "console.log('jw-' + require('crypto').randomBytes(4).toString('hex'))"
# rename: src/pages/resume/<old-slug>/  →  src/pages/resume/<new-slug>/
```

## Local development

```sh
npm install
npm run dev      # http://localhost:4321/portfolio/
npm run build    # static output in ./dist/
npm run preview  # preview the production build locally
```

## Project structure

```
src/
├── content.config.ts          # content collection schemas
├── content/
│   └── resume/
│       ├── jake-wu.zh.md      # Chinese resume
│       └── jake-wu.en.md      # English resume
├── components/
│   ├── ContactReveal.astro    # click-to-reveal email / phone
│   ├── LangToggle.astro       # ZH / EN switcher (localStorage-backed)
│   └── PrintButton.astro
├── layouts/
│   ├── Base.astro             # html shell, noindex meta, lang init
│   └── ResumeLayout.astro     # resume-specific structure
├── pages/
│   ├── index.astro            # public landing
│   ├── 404.astro
│   └── resume/
│       └── jw-e2665966/
│           └── index.astro    # bilingual resume page
└── styles/
    └── global.css             # tailwind import + resume prose + print rules
```

## Deployment

Pushes to `main` trigger `.github/workflows/deploy.yml`, which builds with `withastro/action@v3` and deploys via `actions/deploy-pages@v4`.

One-time setup in GitHub: **Settings → Pages → Build and deployment → Source: GitHub Actions**.

## Adding new content types

Future collections (writing, coverage, work) follow the same pattern:

1. Add a schema to `src/content.config.ts`
2. Drop markdown files under `src/content/<type>/`
3. Add a list page at `src/pages/<type>/index.astro` and a detail page at `src/pages/<type>/[slug].astro`

If you want a particular collection to be search-indexable, override the `<meta name="robots">` for those pages (otherwise Base.astro's site-wide noindex applies).
