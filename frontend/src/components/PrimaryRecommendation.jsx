function PrimaryRecommendation({ tool }) {
  const calendlyUrl = import.meta.env.VITE_CALENDLY_URL || 'https://calendly.com/your-username';

  return (
    <div className="primary-recommendation">
      <h2 className="section-title">Best Match</h2>

      <div className="tool-card primary">
        <div className="tool-header">
          <h3 className="tool-name">{tool.name}</h3>
          <span className="match-score">{tool.matchScore}% Match</span>
        </div>

        <p className="tool-description">{tool.description}</p>

        <div className="tool-features">
          {tool.features?.map((feature, index) => (
            <span key={index} className="feature-tag">
              {feature}
            </span>
          ))}
        </div>

        <div className="tool-links">
          <a
            href={tool.website}
            target="_blank"
            rel="noopener noreferrer"
            className="tool-link primary-link"
          >
            Visit Website
          </a>
        </div>

        {tool.workflow && tool.workflow.length > 0 && (
          <div className="workflow-steps">
            <h4>How to use:</h4>
            <ol>
              {tool.workflow.map((step, index) => (
                <li key={index}>{step}</li>
              ))}
            </ol>
          </div>
        )}

        <div className="booking-section">
          <p className="booking-text">
            Want personalized help implementing this tool?
          </p>
          <a
            href={calendlyUrl}
            target="_blank"
            rel="noopener noreferrer"
            className="booking-button"
          >
            Book $100 Implementation Audit
          </a>
        </div>
      </div>
    </div>
  );
}

export default PrimaryRecommendation;
