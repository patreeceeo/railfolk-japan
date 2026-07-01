# Summary

The app lets users manually create Japan transit itineraries using trains and buses. Users can attach prefabricated culturally meaningful visits and prefabricated education cards to their itineraries. Itineraries are public or unlisted. Public itineraries can be browsed and sorted. Other signed-in users can upvote or downvote an itinerary, but they must select one or more predefined reasons. Aggregate vote reason counts are visible only to admins.

This is not a general transit app. It does not calculate routes, validate schedules, book travel, reserve seats, sell passes, optimize fares, or fetch live transit data. It is focused on intercity travel within Japan rather than travel within Japan's metro areas.

# Goals

The main goal is to be so good at promoting over-land Japan tourism that Japan's rail companies want to sponsor it. In order to do that, the app must be focused, intuitive, useful and fun to use.

## Core product constraints

The app must support:

* User accounts
* Minimal user profiles
* Itinerary creation and editing
* Manually entered transit legs
* Attaching curated visits to itineraries
* Attaching curated education cards to itineraries
* Start and end dates on attached transit legs
* Start and end dates on attached visits
* Date-derived itinerary display
* Public itinerary browsing with sorting only
* Voting with required structured reasons
* Admin-only visibility of aggregate vote reason counts
* Admin management of all users and content types

The app must not support:

* Bookings
* Reservations
* Fare calculation
* Route calculation
* Live transit data
* Maps
* Comments
* Messaging
* Social feeds
* Followers
* Itinerary templates
* Plausibility checker
* Freeform user-created attractions
* Freeform user-created education cards
* Public vote-reason breakdowns
* File uploads
* User badges
* Reputation system

## Main concepts

### User profile

A user profile is minimal.

The displayed avatar and user name should come from Gravatar using the user’s email address.

Fields:

* Email address
* List of itineraries created by that user

No followers, no activity feed, no badges.

### Itinerary

An itinerary is created by a user.

Fields:

* Title
* description
* Visibility: private, unlisted (note: there is no private option for now)
* Created timestamp
* Updated timestamp
* Attached transit legs
* Attached visit cards
* Education cards

Do not manually create “days” as stored objects.

The itinerary’s day-by-day display is derived from the start/end dates of attached transit legs and attached visits.

The itinerary’s total duration should be derived from the earliest start date and latest end date among its attached transit legs and visits.

If an itinerary has no dated items, show duration as empty or “not scheduled.”

### Transit leg

Only created by admins.

Fields:

* Mode:
  * train
  * shinkansen
  * limited express
  * bus
* Origin Location
* Destination Location
* Optional operator
* Optional line name
* Estimated fare in yen
* Duration in days, rounded down, zero or more

No departure time required. No arrival time required. No fare. No schedule lookup.

### Location

A location within Japan.

Only created by admins.

Fields:

* Name
* Description
* Latitude
* Longitude
* Optional address

### Attached transit leg

An attached transit leg is manually created by the user from a transit leg and attached directly to an itinerary.

Fields:

* Transit leg
* Itenerary
* Start date

### Visit card

A visit card is prefabricated curated content managed by admins.

Normal users do not create visits.

Fields:

* Location
* Suggested visit length in hours
* Estimated cost of admission in yen

### Attached visit card

Instance of a visit card attached to an intinerary.

Fields:

* Itinerary
* Visit card
* Start date
* Optional user note

### Education card

An education card is prefabricated curated content managed by admins.

Normal users do not create education cards.

Fields:

* Title
* Category:
  * rail
  * culture
  * language
  * regional context
* Body
* Optional Location

Education cards can be attached to an itinerary.

### Voting

Signed-in users can upvote or downvote a public itinerary.

A vote must include one or more predefined reasons.

Each user may have only one current vote per itinerary. They may change or remove their vote.

Public users should see only the score, not the aggregate reason breakdown.

Admins should be able to view aggregate vote counts by reason.

Upvote reasons:

* Off the beaten path
* Cost-effective
* Time-effective
* Well-paced
* Informative

Downvote reasons:

* Unecessary backtracking
* Unrealistic visit timing
* Unrealistic transfer
* Overloaded
* Generally low-quality

## Public pages

Implement these pages first:

### `/`

Simple landing page.

Briefly explain the product:

A lightweight site for creating and sharing Japan train/bus itineraries with curated cultural visits and education cards.

Link to public itineraries.

### `/itineraries/`

Public itinerary index.

Show only public itineraries.

No filters.

Sorting only:

* Name
* User
* Last updated
* Total duration

Each row/card should show:

* Title
* Creator username / photo
* Total duration
* Last updated
* Description truncated to 140 chars or "no description"

### `/itineraries/<id>/`

Public itinerary detail page.

Respect visibility:

* Public: visible to everyone
* Unlisted: visible to anyone with the URL

Display:

* Title
* Author
* Description
* Visibility if owner/admin
* Total duration
* Last updated
* Vote controls if signed in and not owner
* Date-grouped itinerary content
* Education cards

Date-grouped content should show:

* Transit legs for that date
* Visits cards active on that date

### `/itineraries/new/`

Create itinerary.

Signed-in users only.

### `/itineraries/<id>/edit/`

Edit itinerary.

Owner and admins only.

Must support:

* Editing title, description, visibility
* Adding/editing/deleting transit legs
* Attaching/removing visits cards with start/end dates
* Attaching/removing education cards

Use simple forms. Full page reloads are acceptable.

### `/users/<username>/`

User profile page.

Show:

* Gravatar
* Username
* Short bio
* List of itineraries created by the user

For non-owner viewers, show only public itineraries. For owner/admin, show all their itineraries.

## Admin

Admins should be able to manage:

* Visits and attached visits
* Education cards and thier associations
* Itineraries
* Transit legs
* Visits and attached visits
* Votes
* User profiles

Admins can also view vote reason aggregates for itineraries.

## Seed data

Include a basic seed command or fixture with sample content.

Seed at least:

* 3 users or sample authors
* 3 public itineraries
* 10 curated visits
* 10 education cards

Initial content region should focus on Northern Kyushu.

Sample visits:

* Kushida Shrine
* Dejima
* Sofukuji Temple
* Nagasaki Peace Park
* Suizenji Garden
* Kumamoto Castle area
* Takeo Onsen
* Yufuin
* Beppu jigoku area
* Dazaifu Tenmangu

Sample education cards:

* Shinkansen vs limited express
* Local train vs rapid train
* Rural bus caution
* Station vocabulary
* Shrine etiquette
* Temple etiquette
* Onsen basics
* Ekiben
* Omiyage
* Kyushu regional context

## Visual/UI direction

Keep the UI plain but readable.

Prioritize:

* Clear itinerary display
* Date grouping
* Distinct transit/visit/education sections
* Japanese names shown cleanly
* Timing warnings visible but not alarming
* Simple public browsing table or cards

Avoid:

* Dense dashboards
* Overdesigned landing page
* Complex modals
* Drag-and-drop
* Maps
* Timeline widgets
* Photo-heavy design

## Acceptance criteria

The prototype is acceptable when:

* A user can sign up/sign in
* A user can create an itinerary
* A user can add dated transit legs
* A user can attach dated curated visits
* A user can attach curated education cards
* The itinerary page groups content by date without stored day records
* A public itinerary can be browsed from the itinerary index
* Public itinerary index can sort by name, user, last updated, and total duration
* A user profile shows Gravatar, short bio, and that user’s itineraries
* A signed-in user can upvote/downvote a public itinerary with required reasons
* Normal users do not see aggregate vote reason counts
* Admins can see aggregate vote reason counts
* Admins can manage visits and education cards
* The app runs locally with a single documented setup command sequence
