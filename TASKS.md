# Implementation Tasks

Stay focused and only work on what's necessary for the given task. Unless otherwise specified, use Red, Green, Refactor TDD. Prefer Django, Django templates, Django admin, minimal JavaScript and absolutely no CSS.

## 1. Project Foundation

- [ ] Create the Django project and main app.
  - Depends on: none
  - There's no local setup. For now, the app itself will only run in the production environment, and tests will only run in CI.

- [ ] Add CI/CD with a Nix flake and GitHub Actions.
  - Depends on: project foundation
  - Run tests and basic checks in CI, then deploy if successful.
  - Trigger on each commit pushed to `main` branch.

## 2. Core Data Model

- [ ] Implement accounts and user profiles.
  - Depends on: project foundation
  - Use Django auth, add short bio, and derive avatar/name display from Gravatar email data.

- [ ] Implement content models managed by admins.
  - Depends on: project foundation
  - Add Location, TransitLeg, VisitCard, and EducationCard.

- [ ] Implement itinerary models.
  - Depends on: accounts and user profiles; content models
  - Add Itinerary, AttachedTransitLeg, AttachedVisitCard, and itinerary education-card associations.
  - Do not store day records.

- [ ] Add model helpers for derived dates.
  - Depends on: itinerary models
  - Derive total duration and date-grouped content from attached transit legs and visits.
  - Include unit tests.

## 3. Admin And Seed Data

- [ ] Register admin management screens.
  - Depends on: core data model
  - Admins must manage users, itineraries, locations, transit legs, visits, education cards, attachments, and votes.

- [ ] Add Northern Kyushu seed data.
  - Depends on: core data model
  - Include at least 3 users/authors, 3 public itineraries, 10 visits, and 10 education cards.

## 4. Public Pages

- [ ] Build the landing page at `/`.
  - Depends on: project foundation
  - Match the simple mock in `mocks/index.html`.
  - No TDD

- [ ] Build the public itinerary index at `/itineraries/`.
  - Depends on: itinerary models; derived duration helper
  - Match the mock in `mocks/itineraries.html`

- [ ] Build the itinerary detail page at `/itineraries/<id>/`.
  - Depends on: itinerary models; derived date grouping
  - Respect public and unlisted visibility.
  - Match the mock in `mocks/itinerary-detail.html`.

- [ ] Build user profile pages at `/users/<username>/`.
  - Depends on: accounts and user profiles; itinerary models
  - Match mock in `mocks/user-profile.html`
  - Owner/admin can see all of the user's itineraries; others see only public itineraries.

## 5. Itinerary Editing

- [ ] Build itinerary create and edit forms.
  - Depends on: accounts and user profiles; itinerary models
  - Signed-in users can create itineraries.
  - Owners/admins can edit title, description, and visibility.
  - Refer to mocks in `mocks/new-itinerary.html` and `mocks/itinerary-in-progress.html`.

- [ ] Add transit-leg attachment editing.
  - Depends on: itinerary create/edit forms; content models
  - Owners/admins can add, edit, and remove dated transit legs from the curated transit-leg library.
  - Refer to mocks in `mocks/new-itinerary.html` and `mocks/itinerary-in-progress.html`.

- [ ] Add visit-card attachment editing.
  - Depends on: itinerary create/edit forms; content models
  - Owners/admins can add, edit, and remove dated visit cards with optional notes.
  - Refer to mocks in `mocks/new-itinerary.html` and `mocks/itinerary-in-progress.html`.

- [ ] Add education-card attachment editing.
  - Depends on: itinerary create/edit forms; content models
  - Owners/admins can attach and remove curated education cards.
  - Refer to mocks in `mocks/new-itinerary.html` and `mocks/itinerary-in-progress.html`.

## 6. Voting

- [ ] Implement itinerary voting.
  - Depends on: itinerary detail page; accounts and user profiles
  - Signed-in non-owners can upvote or downvote public itineraries.
  - One current vote per user per itinerary.
  - Vote reasons are required and must come from predefined reason lists.

- [ ] Add vote score and admin reason aggregates.
  - Depends on: itinerary voting; admin screens
  - Public users see only the score.
  - Admins can view aggregate reason counts.
