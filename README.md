# Bone Fracture Detection (Django)

Brief Django webapp for uploading medical scans (DICOM) and running a fracture detection model.

## Project structure

- `bone/` — Django project settings and URL config.
- `main/` — Django app with models, views, and URLs.
- `TEMPLATE/` — HTML templates used by the app (upload, prediction UI, home pages).
- `static/` — Static assets and two model weights: `epoch200.h5` and `epoch85.h5`.
- `media/` — (created at runtime) uploaded files; configured via `MEDIA_ROOT`.
- `db.sqlite3` — SQLite database file.

## Key files

- `main/models.py` — defines `patient_radiogram`, `CT`, and `saggital` models. `CT.image` stores uploaded DICOM files.
- `main/views.py` — handles upload endpoints and prediction logic. Prediction loads `static/epoch200.h5` and processes DICOMs into a 64x64 input.
- `main/urls.py` — app routes: `Home`, `upload`, `prediction`, `services`, `about`.
- `bone/settings.py` — Django settings (templates dir set to `TEMPLATE`, static and media settings).

## Requirements

The project uses (at least):

- Python 3.8+ (test with your environment)
- Django 4.1.x (project mentions 4.1.2)
- numpy
- pydicom
- matplotlib
- tensorflow / keras (for `load_model`)

Suggested `pip` install list (create a virtualenv first):

```
python -m venv .venv
source .venv/bin/activate
pip install django==4.1.2 numpy pydicom matplotlib tensorflow
```

If you prefer, generate `requirements.txt` using `pip freeze` once environment is working.

## Setup & Run (development)

1. Create and activate a virtual environment (see above).
2. Install dependencies.
3. Apply migrations:

```
python manage.py migrate
```

4. Create a superuser (optional, for admin site):

```
python manage.py createsuperuser
```

5. Run the dev server:

```
python manage.py runserver
```

6. Open `http://127.0.0.1:8000/` to view the app.

## Endpoints / Pages

- `/` — Home page (template: `home.html`).
- `/upload` — Upload DICOM files (template: `upload-b.html`). Use the form to upload one or multiple files (field name `images`).
- `/prediction` — Runs prediction on the uploaded DICOMs and shows results (template: `prediction-ui.html`). The view deletes uploaded files after prediction.
- `/services`, `/about`, `/Home` — other informational pages.
- `/admin/` — Django admin.

## Prediction details

- The prediction pipeline in `main/views.py`:
  - Loads the Keras model from `static/epoch200.h5`.
  - Reads the first uploaded DICOM via `pydicom.dcmread(...)` and extracts `pixel_array`.
  - A `reshape` helper downsamples 512x512 -> 64x64 by averaging 8x8 blocks.
  - The image is normalized by dividing by 255 and reshaped to `(64,64,1)` for model input.
  - If the model prediction maximum probability is > 0.99, the app sets `predicted=True` and the UI shows a fracture detected message.
  - After prediction, uploaded `CT` objects are deleted from the DB and filesystem.

Notes:
- The code currently assumes at least one uploaded `CT` exists when `/prediction` is called. Calling `/prediction` with no uploads will raise an IndexError.
- There is commented code in `predict` for an alternate processing flow and a different model (`epoch85.h5`).

## Static models

Two model files are present in `static/`:

- `epoch200.h5` — actively loaded in `predict()`.
- `epoch85.h5` — referenced in commented code.

These are Keras model weight files; ensure `tensorflow`/`keras` versions are compatible before loading.

## Media & static

- Uploaded DICOM files are saved to `media/` via `CT.image` (Django `MEDIA_ROOT`). `bone/settings.py` configures `MEDIA_ROOT` and `MEDIA_URL`.
- `STATICFILES_DIRS` points to the repository `static/` directory.
