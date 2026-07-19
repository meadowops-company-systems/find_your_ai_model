function AlternativesList({ tools }) {
  return (
    <div className="alternatives-section">
      <h2 className="section-title">Alternative Options</h2>

      <div className="alternatives-grid">
        {tools.map((tool, index) => (
          <div key={index} className="tool-card alternative">
            <div className="tool-header">
              <h3 className="tool-name">{tool.name}</h3>
              <span className="match-score">{tool.matchScore}% Match</span>
            </div>

            <p className="tool-description">{tool.description}</p>

            <div className="tool-features">
              {tool.features?.slice(0, 3).map((feature, idx) => (
                <span key={idx} className="feature-tag">
                  {feature}
                </span>
              ))}
            </div>

            <a
              href={tool.website}
              target="_blank"
              rel="noopener noreferrer"
              className="tool-link"
            >
              Learn More
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default AlternativesList;
