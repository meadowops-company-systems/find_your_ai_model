import PrimaryRecommendation from './PrimaryRecommendation';
import AlternativesList from './AlternativesList';
import CostBreakdown from './CostBreakdown';

function RecommendationDisplay({ recommendation }) {
  const { primary, alternatives, processingTime } = recommendation;

  return (
    <section className="recommendation-section">
      <div className="processing-time">
        Generated in {processingTime}ms
      </div>

      <PrimaryRecommendation tool={primary} />

      {alternatives && alternatives.length > 0 && (
        <AlternativesList tools={alternatives} />
      )}

      {primary.cost && (
        <CostBreakdown cost={primary.cost} />
      )}
    </section>
  );
}

export default RecommendationDisplay;
