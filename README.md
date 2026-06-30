# Railfolk Japan

Railfolk Japan is a Django application for creating and sharing Japan train and bus itineraries with curated cultural visits and education cards.

The product is intentionally narrow. It does not calculate routes, validate schedules, book travel, reserve seats, optimize fares, or fetch live transit data. See [PRD.md](PRD.md) for the full product scope.

## Stack

* Django
* SQLite by default
* Nix flake for local development, CI, and server packaging
* Gunicorn for production serving

## Requirements

Install Nix with flakes enabled.

## Local Development

Enter the development shell:

```sh
nix develop
```

Run database migrations:

```sh
python manage.py migrate
```

Start the local development server:

```sh
DJANGO_DEBUG=true python manage.py runserver
```

Open http://127.0.0.1:8000/.

## Useful Commands

Run Django's project checks:

```sh
DJANGO_DEBUG=true python manage.py check
```

Run tests:

```sh
DJANGO_DEBUG=true python manage.py test
```

Create an admin user:

```sh
DJANGO_DEBUG=true python manage.py createsuperuser
```

## Configuration

The app reads these environment variables:

* `DJANGO_DEBUG`: enables local debug behavior when set to `true`, `1`, or `yes`.
* `DJANGO_SECRET_KEY`: required when `DJANGO_DEBUG` is disabled.
* `DJANGO_ALLOWED_HOSTS`: comma-separated host allowlist. Defaults to `railfolk.zzt64.com,localhost,127.0.0.1`.
* `DJANGO_DATABASE_PATH`: SQLite database path. Defaults to `db.sqlite3` in the repo root.

## Deployment

The flake exposes:

* `railfolkJapanServer`: runs Gunicorn against `railfolk_japan.wsgi:application` on `127.0.0.1:8000`.
* `railfolkJapanInstallService`: installs and restarts the systemd service as root.

The GitHub Actions workflow runs checks and tests on pull requests. Pushes to `main` also run the deploy job, which uses the configured SSH deployment secrets and runs migrations, static collection, and service installation on the target host.

## Project Notes

* Product requirements live in [PRD.md](PRD.md).
* Engineering direction lives in [ENGINEERING.md](ENGINEERING.md).
* Planned work lives in [TASKS.md](TASKS.md).
