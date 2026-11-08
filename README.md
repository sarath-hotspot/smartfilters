# Smart Filters for Outlook

Smart Filters explores a more natural alternative to manually writing Outlook rules. Instead of asking people to define conditions for every kind of message, the idea is to learn from their filing habits: when a person moves an email to a folder, the system can use that choice as feedback and learn which future messages belong there.

## Project status

This is an experimental, legacy prototype rather than a finished Outlook product. The repository contains a Windows Outlook VSTO add-in, a Flask service, and machine-learning experiments.

The current add-in watches for new messages in the Inbox, sends their subject and body to the local Flask service, and applies the predicted category in Outlook. The service has endpoints for creating filters and accepting labeled training examples. However, the add-in does not currently observe messages being moved between folders or send those moves as training feedback; learning directly from filing behavior is the project idea, not a fully implemented workflow.

## How it is organized

- `OutlookAddIn/` — C# VSTO add-in and Visual Studio solution. The add-in calls the service at `http://localhost:5000`.
- `Flask-Endpoint/` — Flask API, SVM-based prediction and training code, saved models, and training data.
- `Model/` — model experiments, training scripts, and additional sample data.

## Running the prototype

### Flask service

Run the backend on a machine with Python and the required packages installed:

```bash
cd Flask-Endpoint
python app.py
```

The service listens on port `5000`. The source imports Flask, NumPy, pandas, and scikit-learn. This repository does not include a pinned Python dependency file, so compatible package versions may need to be selected for this older codebase.

### Outlook add-in

On Windows, open `OutlookAddIn/SmartFilterAddin.sln` in a version of Visual Studio with Office/VSTO development support. The project targets .NET Framework 4.6.1 and requires desktop Outlook and the Visual Studio Tools for Office runtime. Start the Flask service before running the add-in; its backend address is currently hard-coded to `localhost:5000`.

## API overview

The Flask service provides these routes:

| Method | Route | Purpose |
|---|---|---|
| `GET` | `/listFilters` | Return the available filter names. |
| `POST` | `/createFilter` | Create a filter model from a JSON `filterName`. |
| `POST` | `/predict` | Predict filter labels from JSON `Subject` and `Body` fields. |
| `POST` | `/train` | Add a labeled example using `FilterName`, `Subject`, `Body`, and `Output` (`0` or `1`). |

These endpoints and the add-in are prototype code; they are not designed as a secure, production-ready email-processing service.

## Privacy and limitations

The add-in sends email subjects and bodies to the configured Flask service for classification. In the checked-in prototype, that service is expected to run locally, and email content should be treated as sensitive. The project does not currently provide production deployment guidance, authentication, or a completed move-to-folder learning flow.

## Contributing

Contributions that help turn the prototype into a reliable, privacy-conscious Outlook experience are welcome. Useful areas include capturing folder moves as explicit feedback, validating learned rules before applying them, documenting reproducible development dependencies, and adding tests for the add-in and API.
