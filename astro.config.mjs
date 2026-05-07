// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import sitemap from '@astrojs/sitemap';

export default defineConfig({
  site: 'https://jakewqj.github.io',
  base: '/portfolio',
  build: { format: 'directory' },
  integrations: [
    sitemap({
      filter: (page) => page.includes('/portfolio/coverage/'),
    }),
  ],
  vite: {
    plugins: [tailwindcss()],
  },
});
