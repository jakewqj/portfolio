import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const resume = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/resume' }),
  schema: z.object({
    name: z.string(),
    nameEn: z.string(),
    title: z.string(),
    location: z.string(),
    tagline: z.string(),
    emailParts: z.tuple([z.string(), z.string()]),
    phoneFull: z.string(),
    phoneObfuscated: z.string(),
    linkedin: z.string().url(),
    lang: z.enum(['zh', 'en']),
  }),
});

export const collections = { resume };
