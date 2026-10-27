(() => {
  const API_BASE_URL = (window.MODEL_EVALUATION_API_BASE_URL || window.location.origin).replace(/\/$/, '');
  const STORAGE_KEY = 'model-lens.current';
  const HISTORY_KEY = 'model-lens.history';

  const metricConfig = {
    classification: [
      { name: 'accuracy', label: 'Accuracy', min: 0, max: 1, step: '0.0001' },
      { name: 'precision', label: 'Precision', min: 0, max: 1, step: '0.0001' },
      { name: 'recall', label: 'Recall', min: 0, max: 1, step: '0.0001' },
      { name: 'f1_score', label: 'F1 score', min: 0, max: 1, step: '0.0001' },
      { name: 'roc_auc', label: 'ROC AUC', min: 0, max: 1, step: '0.0001' },
      { name: 'log_loss', label: 'Log loss', min: 0, max: 1, step: '0.0001' },
    ],
    regression: [
      { name: 'mae', label: 'MAE', min: 0, step: 'any' },
      { name: 'mse', label: 'MSE', min: 0, step: 'any' },
      { name: 'rmse', label: 'RMSE', min: 0, step: 'any' },
      { name: 'r2_score', label: 'R² score', step: 'any' },
    ],
  };

  const escapeHtml = (value) => String(value ?? '').replace(/[&<>"']/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
  }[character]));

  document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('metrics-dynamic-form');
    if (!form) return;

    const taskType = document.getElementById('task-type');
    const fields = document.getElementById('metric-fields');
    const helper = document.getElementById('metric-helper');
    const error = document.getElementById('metrics-error');
    const submit = document.getElementById('metrics-submit');

    const showError = (message) => { error.textContent = message; error.hidden = false; };
    const clearError = () => { error.textContent = ''; error.hidden = true; };

    const renderMetrics = () => {
      const selected = taskType.value;
      const metrics = metricConfig[selected];

      // Replacing the field container removes every old value before rendering the new task type.
      fields.replaceChildren();
      clearError();

      if (!metrics) {
        fields.hidden = true;
        helper.hidden = false;
        helper.textContent = 'Select a task type to enter relevant metrics.';
        return;
      }

      helper.hidden = false;
      helper.textContent = `Enter one or more ${selected} metrics. Only these values will be submitted.`;
      fields.hidden = false;

      metrics.forEach((metric) => {
        const label = document.createElement('label');
        label.htmlFor = `metric-${metric.name}`;
        label.textContent = metric.label;

        const input = document.createElement('input');
        input.id = `metric-${metric.name}`;
        input.name = metric.name;
        input.type = 'number';
        input.step = metric.step;
        input.placeholder = metric.name === 'r2_score' ? '0.82' : '0.0000';
        if (metric.min !== undefined) input.min = metric.min;
        if (metric.max !== undefined) input.max = metric.max;

        label.append(input);
        fields.append(label);
      });
    };

    taskType.addEventListener('change', renderMetrics);
    renderMetrics();

    form.addEventListener('submit', async (event) => {
      event.preventDefault();
      clearError();

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      const selected = taskType.value;
      const configuredMetrics = metricConfig[selected];
      if (!configuredMetrics) {
        showError('Select Classification or Regression before entering metrics.');
        taskType.focus();
        return;
      }

      const metrics = configuredMetrics.reduce((result, metric) => {
        const value = form.elements[metric.name].value.trim();
        if (value !== '') result[metric.name] = Number(value);
        return result;
      }, {});

      if (!Object.keys(metrics).length) {
        showError(`Enter at least one ${selected} metric.`);
        return;
      }

      const metadata = {};
      ['dataset_name', 'framework', 'target_column', 'dataset_size', 'feature_count'].forEach((name) => {
        const value = form.elements[name].value.trim();
        if (value !== '') metadata[name] = ['dataset_size', 'feature_count'].includes(name) ? Number(value) : value;
      });

      const payload = {
        task_type: selected,
        model_name: form.elements.model_name.value.trim(),
        metrics,
        ...(Object.keys(metadata).length ? { experiment_metadata: metadata } : {}),
      };

      submit.disabled = true;
      submit.textContent = 'Working…';
      try {
        const response = await fetch(`${API_BASE_URL}/evaluate`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });
        const result = await response.json();
        if (!response.ok || result.status === 'error') throw new Error(result.detail || result.message || `Server returned ${response.status}`);

        const item = { response: result, input: { kind: 'metrics', payload }, savedAt: new Date().toISOString() };
        sessionStorage.setItem(STORAGE_KEY, JSON.stringify(item));
        const history = JSON.parse(sessionStorage.getItem(HISTORY_KEY) || '[]');
        sessionStorage.setItem(HISTORY_KEY, JSON.stringify([item, ...history.filter((entry) => entry.response.report_id !== result.report_id)].slice(0, 5)));
        window.location.href = 'report.html';
      } catch (exception) {
        showError(`We could not generate this evaluation. ${exception.message}`);
      } finally {
        submit.disabled = false;
        submit.textContent = 'Generate evaluation →';
      }
    });
  });
})();
