import fs from 'node:fs';
import path from 'node:path';
import yaml from 'js-yaml';

export interface Clipping {
  id: string;
  date: string;
  year: number;
  region: string | null;
  outlet: string;
  outlet_tier: number;
  outlet_category: string | null;
  outlet_logo: string | null;
  campaign_display: string | null;
  event: string | null;
  campaign: string | null;
  content_type: string | null;
  format: string | null;
  reach: number | null;
  url: string;
}

export interface CoveragePayload {
  generated_at: string;
  source_xlsx: string;
  totals: {
    clippings: number;
    outlets: number;
    regions: string[];
    cumulative_reach: number;
    by_year: Record<string, number>;
    by_campaign: Record<string, number>;
  };
  clippings: Clipping[];
}

export interface Highlights {
  overview_highlights: string[];
  campaigns: Record<
    string,
    { cover?: string; clippings_to_feature: string[] }
  >;
  awards: {
    outlet: string;
    outlet_zh?: string;
    award: string;
    issue?: string;
    products: string[];
    year: number;
    note?: string;
    badge?: string;
    badge_kind?: 'seal' | 'page';
  }[];
}

const root = path.resolve(process.cwd());

let coverageCache: CoveragePayload | null = null;
let highlightsCache: Highlights | null = null;

export function loadCoverage(): CoveragePayload {
  if (!coverageCache) {
    const raw = fs.readFileSync(path.join(root, 'src/data/coverage.json'), 'utf-8');
    coverageCache = JSON.parse(raw);
  }
  return coverageCache!;
}

export function loadHighlights(): Highlights {
  if (!highlightsCache) {
    const raw = fs.readFileSync(path.join(root, 'src/data/highlights.yaml'), 'utf-8');
    const parsed = yaml.load(raw) as Highlights;
    // Normalize defaults so consumers don't have to null-check.
    highlightsCache = {
      overview_highlights: parsed.overview_highlights ?? [],
      campaigns: parsed.campaigns ?? {},
      awards: parsed.awards ?? [],
    };
  }
  return highlightsCache!;
}

export function clippingsForCampaign(slug: string): Clipping[] {
  return loadCoverage()
    .clippings.filter((c) => c.campaign === slug)
    .sort((a, b) => (b.reach ?? 0) - (a.reach ?? 0));
}

export function formatReach(n: number | null | undefined): string {
  if (n == null || n === 0) return '—';
  if (n >= 1_000_000_000) return `${(n / 1_000_000_000).toFixed(1)}B`;
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}M`;
  if (n >= 1_000) return `${(n / 1_000).toFixed(0)}K`;
  return String(n);
}

export function formatDate(iso: string): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return d.toISOString().slice(0, 10);
}
