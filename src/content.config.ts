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

const campaigns = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/campaigns' }),
  schema: z.object({
    title: z.string(),
    subtitle: z.string().optional(),
    dateRange: z.string(),
    products: z.array(z.string()),
    brandPartner: z.string().optional(),
    summary: z.string(),
    heroImage: z.string().optional(),
    order: z.number().default(99),
  }),
});

export const collections = { resume, campaigns };
