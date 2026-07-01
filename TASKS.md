# Railfolk Japan — Implementation Tasks

> Read `PRD.md`, `ENGINEERING.md`, and `AGENTS.md` before starting any task.
> Stack: Django · Django templates · Django admin · SQLite (local) · Nix flake · minimal JS · no CSS unless asked.
> Write unit tests except where noted.
> Work on **one task at a time**. Do not gold-plate.

---

## T1 · Project Foundation

### T1-A · Django project scaffold
- [x] complete?
- **Depends on:** nothing
- Create the `railfolk_japan` Django project and a single app (`core`).
- Add `manage.py`, `settings.py` (SQLite, `DEBUG=True` locally), `urls.py`.
- The app runs only in the production environment; no local runserver setup required.
- Verify: `python manage.py check` passes with no errors.

### T1-B · CI/CD pipeline
- [x] complete?
- **Depends on:** T1-A
- Add `.github/workflows/ci.yml`:
  - Triggered on every push to `main`.
  - Uses the Nix flake (`flake.nix` already exists) to install deps.
  - Runs `python manage.py test`.
  - On test pass, deploy
- No secrets baked in; use GitHub Actions secrets for deploy credentials.

---

## T2 · Data Models

### T2-A · User profile
- [x] complete?
- **Depends on:** T1-A
- Use a chosen username for public identity.
- Add an internal `avatar_key` generated server-side for provider-agnostic avatar lookup.
- No avatar upload field.

### T2-B · Admin-managed content models
- [x] complete?
- **Depends on:** T1-A
- Add models (admin-only creation):
  - `Location`: `name`, `description`, `latitude`, `longitude`, `address (optional)`
  - `TransitLeg`: `mode` (choices: train/shinkansen/limited-express/bus), `origin` → `Location`, `destination` → `Location`, `operator (optional)`, `line_name (optional)`, `fare_yen`, `duration_hours`
  - `VisitCard`: `location` → `Location`, `suggested_hours`, `admission_yen`
  - `EducationCard`: `title`, `category` (choices: rail/culture/language/regional-context), `body`, `location (optional)` → `Location`
- Include migrations.

### T2-C · Itinerary models
- [x] complete?
- **Depends on:** T2-A, T2-B
- Add models:
  - `Itinerary`: `title`, `description`, `visibility` (choices: public/unlisted), `owner` → `User`, `created_at`, `updated_at`, `education_cards` M2M → `EducationCard`
  - `AttachedTransitLeg`: `itinerary`, `transit_leg`, `start_date`
  - `AttachedVisitCard`: `itinerary`, `visit_card`, `start_date`, `note (optional)`
- Do **not** store day records. Duration and date grouping are derived.
- Include migrations.

### T2-D · Derived date helpers
- [x] complete?
- **Depends on:** T2-C
- On `Itinerary`, add:
  - `total_duration()` → returns `(earliest_start, latest_end)` tuple across `AttachedTransitLeg` and `AttachedVisitCard`; returns `None` if no dated items.
  - `grouped_by_date()` → returns an ordered dict of `date → {transit_legs: [...], visit_cards: [...]}`.
- Cover both helpers with unit tests, including edge cases (no items, single item, overlapping dates).

---

## T3 · Admin & Seed Data

### T3-A · Django admin registration
- [x] complete?
- **Depends on:** T2-C
- Register in `admin.py`:
  - `User` (with profile fields)
  - `Location`, `TransitLeg`, `VisitCard`, `EducationCard`
  - `Itinerary` (with inlines for `AttachedTransitLeg`, `AttachedVisitCard`, education-card M2M)
  - `Vote` (once T7 is done)
- Add a custom `Itinerary` admin change view that shows aggregate vote-reason counts.

### T3-B · Northern Kyushu seed data
- [x] complete?
- **Depends on:** T2-C
- Add a management command `python manage.py seed`.
- Must create:
  - 3 users
  - 10 `Location` records (Kushida Shrine, Dejima, Sofukuji Temple, Nagasaki Peace Park, Suizenji Garden, Kumamoto Castle area, Takeo Onsen, Yufuin, Beppu jigoku area, Dazaifu Tenmangu)
  - 10 `EducationCard` records (Shinkansen vs limited express, Local train vs rapid train, Rural bus caution, Station vocabulary, Shrine etiquette, Temple etiquette, Onsen basics, Ekiben, Omiyage, Kyushu regional context)
  - Representative `TransitLeg` records connecting the locations
  - 3 public `Itinerary` records with attached legs, visits, and education cards
- Command must be idempotent (safe to re-run).

---

## T4 · Auth Pages

### T4-A · Sign-up and sign-in
- [x] complete?
- **Depends on:** T2-A
- Use Django's built-in auth views for login/logout.
- Add a minimal sign-up form (username, email, password).
- Add URL routes: `/accounts/login/`, `/accounts/logout/`, `/accounts/signup/`.
- Templates: plain HTML, no CSS.

---

## T5 · Public Pages

### T5-A · Landing page `/`
- [x] complete?
- **Depends on:** T1-A
- Render `mocks/index.html` as a reference.
- One-paragraph product description + link to `/itineraries/`.
- No unit tests required.

### T5-B · Itinerary index `/itineraries/`
- [ ] complete?
- **Depends on:** T2-D
- Show only public itineraries.
- Columns: title, creator (username + `/avatar/<user_id>` image), total duration, last updated, description (truncated to 140 chars).
- Sorting by: name, user, last updated, total duration (query-param `?sort=`).
- Reference: `mocks/itineraries.html`.

### T5-C · Itinerary detail `/itineraries/<id>/`
- [ ] complete?
- **Depends on:** T2-D
- Respect visibility: public = everyone; unlisted = anyone with the URL; private = owner/admin only (404 for others).
- Display: title, author (`/avatar/<user_id>` image + username), description, total duration, last updated.
- Show visibility badge only to owner/admin.
- Date-grouped content sections: transit legs and visit cards grouped by date (use `grouped_by_date()`).
- Education cards shown below (not date-grouped).
- Vote controls if signed-in and not the owner (wired up in T7).
- Reference: `mocks/itinerary-detail.html` and `mocks/itinerary-in-progress.html`.

### T5-D · User profile `/users/<username>/`
- [ ] complete?
- **Depends on:** T2-A, T2-C
- Show: `/avatar/<user_id>` image, username, short bio, list of itineraries.
- Non-owner/non-admin: show only public itineraries. Owner/admin: show all.
- Reference: `mocks/user-profile.html`.

---

## T6 · Itinerary Editing

### T6-A · Create and edit forms
- [ ] complete?
- **Depends on:** T4-A, T2-C
- `/itineraries/new/` — signed-in users only; creates `Itinerary`.
- `/itineraries/<id>/edit/` — owner/admin only; edits title, description, visibility.
- Full-page reloads; plain Django forms.
- Reference: `mocks/new-itinerary.html`, `mocks/itinerary-in-progress.html`.

### T6-B · Transit-leg attachment editing
- [ ] complete?
- **Depends on:** T6-A, T2-B
- On the edit page, allow adding/editing/removing `AttachedTransitLeg` records.
- User picks from the curated `TransitLeg` library (dropdown or search); sets `start_date`.
- Inline formset is acceptable.

### T6-C · Visit-card attachment editing
- [ ] complete?
- **Depends on:** T6-A, T2-B
- On the edit page, allow adding/editing/removing `AttachedVisitCard` records.
- User picks from `VisitCard` library; sets `start_date` and optional note.
- Inline formset is acceptable.

### T6-D · Education-card attachment editing
- [ ] complete?
- **Depends on:** T6-A, T2-B
- On the edit page, allow attaching/detaching `EducationCard` records to the itinerary M2M.
- Checkbox list or multi-select is fine.

---

## T7 · Voting

### T7-A · Vote model and submit
- [ ] complete?
- **Depends on:** T5-C, T4-A
- Add `Vote` model: `itinerary`, `user`, `direction` (up/down), `reasons` (M2M or JSON to a predefined list).
- Predefined upvote reasons: Off the beaten path, Cost-effective, Time-effective, Well-paced, Informative.
- Predefined downvote reasons: Unnecessary backtracking, Unrealistic visit timing, Unrealistic transfer, Overloaded, Generally low-quality.
- One vote per user per itinerary (enforce at DB and form level).
- Signed-in non-owners can submit/change/remove a vote on public itineraries.
- At least one reason required.
- Display vote score (upvotes − downvotes) publicly on the detail page.

### T7-B · Admin vote reason aggregates
- [ ] complete?
- **Depends on:** T7-A, T3-A
- In the `Itinerary` admin detail view, show counts per reason for up and down votes.
- Normal users never see reason breakdowns.

---

## Completion Criteria

All tasks are done when every acceptance criterion in `PRD.md` passes:

- [ ] User can sign up / sign in
- [ ] User can create an itinerary
- [ ] User can add dated transit legs
- [ ] User can attach dated curated visits
- [ ] User can attach curated education cards
- [ ] Itinerary page groups content by date (no stored day records)
- [ ] Public itinerary index sorts by name, user, last updated, total duration
- [ ] User profile shows avatar, username, and that user's itineraries
- [ ] Signed-in user can upvote/downvote with required reasons
- [ ] Normal users do not see votes
- [ ] Admins can see vote reason breakdowns
- [ ] Admins can manage visits and education cards via Django admin
- [ ] `python manage.py seed` produces working seed data
- [ ] CI runs on every push to `main` and deploys on success
