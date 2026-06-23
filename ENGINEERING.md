## Overview

See [./PRD.md] for information about the product requirements.

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
* Gravatar for user profile image

Avoid React, Next.js, API-first architecture, background jobs, paid APIs, file uploads, and complex frontend state.

## Engineering priorities

Priority order:

1. Data model
2. Admin content management
3. Public itinerary display
4. Itinerary creation/editing
5. Visit/card attachment
6. Date grouping and derived duration
7. Voting
8. Seed data
9. Basic styling

Do not spend time on polish until the full core flow works.
