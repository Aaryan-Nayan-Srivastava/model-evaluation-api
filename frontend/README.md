# Model Evaluation Reporter UI

The static UI uses only HTML, CSS, and vanilla JavaScript.

Run the FastAPI app from the project root, then open `http://127.0.0.1:8000/ui/`:

```powershell
.\model-eval-env\Scripts\python.exe -m uvicorn app.main:app --reload
```

`app/main.py` serves this directory at `/ui`, so the UI defaults to the same origin as the API and needs no CORS configuration. `assets/app.js` uses `window.MODEL_EVALUATION_API_BASE_URL || window.location.origin`; set the former before loading the script if the UI is hosted separately. The current API does not enable CORS, so a separately hosted UI requires CORS middleware on FastAPI.

The report view is deliberately transparent: `EvaluationResponse` does not return `processed_metrics`, `metric_flags`, or discrete recommendations. Manual metrics are retained in session storage; narrative sections are parsed from the returned `summary`.
