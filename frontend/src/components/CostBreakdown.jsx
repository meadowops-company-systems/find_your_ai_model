function CostBreakdown({ cost }) {
  if (!cost) return null;

  const formatPrice = (amount) => {
    if (amount === 0) return 'Free';
    return `$${amount.toFixed(2)}`;
  };

  return (
    <div className="cost-section">
      <h2 className="section-title">Cost Breakdown</h2>

      <div className="cost-card">
        <div className="cost-item">
          <span className="cost-label">Monthly Cost</span>
          <span className="cost-value">{formatPrice(cost.monthly)}</span>
        </div>

        {cost.yearly !== undefined && (
          <div className="cost-item">
            <span className="cost-label">Yearly Cost</span>
            <span className="cost-value">{formatPrice(cost.yearly)}</span>
          </div>
        )}

        {cost.tier && (
          <div className="cost-item">
            <span className="cost-label">Pricing Tier</span>
            <span className="cost-value tier">{cost.tier}</span>
          </div>
        )}

        {cost.notes && (
          <p className="cost-notes">{cost.notes}</p>
        )}
      </div>
    </div>
  );
}

export default CostBreakdown;
