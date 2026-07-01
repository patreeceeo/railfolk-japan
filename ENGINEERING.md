## Overview

See [./PRD.md](./PRD.md) for information about the product requirements.

## Recommended stack

Use:

* Django
* Django templates
* Django admin
* SQLite for local development
* PostgreSQL-compatible design for later deployment
* Minimal JavaScript
* HTMX only if it clearly reduces complexity
* No CSS unless explicitly requested!
* App-served avatar endpoint for user profile image

Avoid React, Next.js, API-first architecture, background jobs, paid APIs, file uploads, and complex frontend state.

## Engineering priorities

Priority order:

1. Set up CI/CD using a Nix flake and GitHub action
2. Data model
3. Admin content management
4. Public itinerary display
5. Itinerary creation/editing
6. Visit/card attachment
7. Date grouping and derived duration
8. Voting
9. Seed data
10. Basic styling

Do not spend time on polish until the full core flow works.
