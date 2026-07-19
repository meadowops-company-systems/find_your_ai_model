import { describe, expect, it } from 'vitest';
import {
  filterAlternatives,
  normalizeRecommendation,
} from './phase2';

describe('phase2 helpers', () => {
  it('normalizes recommendation payloads', () => {
    const result = normalizeRecommendation({
      primary: { name: 'Claude', matchScore: 91, pricing: '$20/mo', features: ['Text', 'Vision'] },
      alternatives: [{ name: 'ChatGPT', score: 77 }],
    });

    expect(result.primary.name).toBe('Claude');
    expect(result.primary.score).toBe(91);
    expect(result.alternatives).toHaveLength(1);
  });

  it('filters alternatives', () => {
    const alternatives = filterAlternatives(
      [
        { name: 'Free Tool', provider: 'X', score: 50, price: 'Free tier' },
        { name: 'Paid Tool', provider: 'Y', score: 90, price: '$20/mo' },
      ],
      { query: 'tool', minScore: 60, priceMode: 'paid' },
    );

    expect(alternatives).toHaveLength(1);
    expect(alternatives[0].name).toBe('Paid Tool');
  });
});
