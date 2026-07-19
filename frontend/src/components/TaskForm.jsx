import { useState } from 'react';

const CATEGORIES = [
  { id: 'writing', label: 'Writing & Content' },
  { id: 'coding', label: 'Coding & Development' },
  { id: 'image', label: 'Image Generation' },
  { id: 'audio', label: 'Audio & Music' },
  { id: 'video', label: 'Video & Animation' },
  { id: 'data', label: 'Data & Analytics' },
  { id: 'research', label: 'Research & Learning' },
  { id: 'productivity', label: 'Productivity' },
];

const MIN_LENGTH = 10;
const MAX_LENGTH = 5000;

function TaskForm({ onSubmit, loading, task, setTask, category, setCategory }) {
  const [validationError, setValidationError] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    setValidationError('');

    if (task.length < MIN_LENGTH) {
      setValidationError(`Please enter at least ${MIN_LENGTH} characters`);
      return;
    }

    if (task.length > MAX_LENGTH) {
      setValidationError(`Maximum ${MAX_LENGTH} characters allowed`);
      return;
    }

    onSubmit(task, category);
  };

  const handleTaskChange = (e) => {
    setTask(e.target.value);
    if (validationError) setValidationError('');
  };

  const charCount = task.length;
  const isValid = charCount >= MIN_LENGTH;

  return (
    <section className="task-form-section">
      <form onSubmit={handleSubmit} className="task-form">
        <div className="form-group">
          <label htmlFor="category" className="form-label">
            Task Category (optional)
          </label>
          <select
            id="category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="form-select"
          >
            <option value="">All Categories</option>
            {CATEGORIES.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.label}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label htmlFor="task" className="form-label">
            Describe your task in detail
          </label>
          <textarea
            id="task"
            value={task}
            onChange={handleTaskChange}
            placeholder="e.g., Write a blog post about AI trends in 2024, around 1500 words, SEO-optimized for tech professionals"
            className="form-textarea"
            rows={6}
            disabled={loading}
          />
          <div className="char-count">
            <span className={charCount < MIN_LENGTH ? 'text-error' : charCount > MAX_LENGTH ? 'text-error' : 'text-success'}>
              {charCount}
            </span>
            <span className="char-limit">/ {MAX_LENGTH}</span>
          </div>
        </div>

        {validationError && (
          <div className="validation-error">
            {validationError}
          </div>
        )}

        <button
          type="submit"
          className="submit-button"
          disabled={!isValid || loading}
        >
          {loading ? (
            <span className="loading-spinner">Getting Recommendation...</span>
          ) : (
            'Get Recommendation'
          )}
        </button>
      </form>
    </section>
  );
}

export default TaskForm;
