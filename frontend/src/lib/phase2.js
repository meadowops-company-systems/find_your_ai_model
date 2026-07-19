const EMPTY_RESULT = {
  primary: null,
  alternatives: [],
  processingTime: null,
};

export function normalizeRecommendation(data) {
  if (!data) return EMPTY_RESULT;

  const primarySource = data.primary || data.primary_tool || {};
  const alternativesSource = Array.isArray(data.alternatives) ? data.alternatives : [];

  const primary = primarySource.name
    ? {
        name: primarySource.name,
        provider: primarySource.provider || primarySource.category || 'Recommended',
        score: primarySource.matchScore ?? primarySource.match_score ?? primarySource.score ?? 0,
        price: primarySource.pricing || primarySource.price || 'Varies',
        context: primarySource.context || primarySource.context_window || '',
        logo: primarySource.logo || '🤖',
        description: primarySource.description || primarySource.reason || primarySource.why_best || '',
        reasons: Array.isArray(primarySource.reasons)
          ? primarySource.reasons
          : Array.isArray(primarySource.why_best)
            ? primarySource.why_best
            : primarySource.reason
              ? [primarySource.reason]
              : [],
        caps: primarySource.features || primarySource.capabilities || [],
        workflow: Array.isArray(primarySource.workflow)
          ? primarySource.workflow
          : primarySource.workflow?.steps || [],
        website: primarySource.website || primarySource.official_link || '',
        cost: primarySource.cost || null,
      }
    : null;

  const alternatives = alternativesSource
    .map((alt) => ({
      name: alt.name,
      provider: alt.provider || alt.category || 'Alternative',
      score: alt.matchScore ?? alt.match_score ?? alt.score ?? 0,
      price: alt.pricing || alt.price || 'Varies',
      reason: alt.reason || alt.why_alternative || alt.description || '',
      website: alt.website || alt.official_link || '',
    }))
    .filter((alt) => alt.name);

  return {
    primary,
    alternatives,
    processingTime: data.processingTime ?? data.processing_time ?? null,
  };
}

export function filterAlternatives(alternatives = [], filters = {}) {
  const query = (filters.query || '').trim().toLowerCase();
  const minScore = Number(filters.minScore || 0);
  const priceMode = filters.priceMode || 'all';

  return alternatives.filter((item) => {
    const matchesQuery =
      !query ||
      item.name.toLowerCase().includes(query) ||
      (item.provider || '').toLowerCase().includes(query) ||
      (item.reason || '').toLowerCase().includes(query);

    const matchesScore = (item.score || 0) >= minScore;
    const isFree = /free/i.test(item.price || '') || /free/i.test(item.reason || '');
    const isPaid = !isFree;
    const matchesPrice =
      priceMode === 'all' || (priceMode === 'free' && isFree) || (priceMode === 'paid' && isPaid);

    return matchesQuery && matchesScore && matchesPrice;
  });
}
