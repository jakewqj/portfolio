// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://jakewqj.github.io',
  base: '/portfolio',
  build: { format: 'directory' },
  vite: {
    plugins: [tailwindcss()],
  },
});
