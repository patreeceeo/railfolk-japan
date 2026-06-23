# Summary

The app lets users manually create Japan transit itineraries using trains and buses. Users can attach prefabricated culturally meaningful visits and prefabricated education cards to their itineraries. Itineraries are public or unlisted. Public itineraries can be browsed and sorted. Other signed-in users can upvote or downvote an itinerary, but they must select one or more predefined reasons. Aggregate vote reason counts are visible only to admins.

This is not a general transit app. It does not calculate routes, validate schedules, book travel, reserve seats, sell passes, optimize fares, or fetch live transit data.

# Goals

The main goal is to be so good at promoting over-land Japan tourism that Japan's rail companies want to sponsor it. In order to do that, the app must be intuitive, useful and fun to use.

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
* Admin management for:
  - curated visits
  - education cards
  - transit legs

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

It contains:

* User
* Short bio

The displayed avatar should come from Gravatar using the user’s email address.

A public user page should show:

* Gravatar
* Username
* Short bio
* List of itineraries created by that user

No followers, no activity feed, no badges.

### Itinerary

An itinerary is created by a user.

It contains:

* Title
* Optional description
* Visibility: private, unlisted, public
* Created timestamp
* Updated timestamp

Do not manually create “days” as stored objects.

The itinerary’s day-by-day display is derived from the start/end dates of attached transit legs and attached visits.

The itinerary’s total duration should be derived from the earliest start date and latest end date among its attached transit legs and visits.

If an itinerary has no dated items, show duration as empty or “not scheduled.”

### Transit leg

A transit leg is manually entered by the user and attached directly to an itinerary.

Fields:

* Itinerary
* Mode:

  * train
  * shinkansen
  * limited express
  * local train
  * tram
  * bus
* Origin name
* Destination name
* Optional operator
* Optional line name
* Optional notes
* Start date
* End date

No departure time required. No arrival time required. No fare. No schedule lookup.

### Visit

A visit is prefabricated curated content managed by admins.

Normal users do not create visits.

Fields should include:

* English name
* Japanese name
* Optional reading
* Region
* Type
* Nearest station or stop
* Access note
* Suggested visit length
* Cultural significance
* Etiquette note
* Seasonality note
* Published/unpublished status

Visits can be attached to an itinerary with:

* Itinerary
* Visit
* Start date
* End date
* Optional user note

### Time-sensitive visits

Some visits are time-sensitive, such as festivals or seasonal events.

Support simple editorial timing metadata on visits.

Timing categories:

* Always available
* Fixed annual date range
* Seasonal window
* Variable annual dates
* Irregular or limited

For fixed annual date ranges, store enough information to represent recurring month/day ranges, for example August 2 through August 7.

For seasonal windows, store an editorial note and approximate timing information if useful.

When a time-sensitive visit is attached to an itinerary, display timing guidance on the itinerary page.

If the attached date range appears outside a fixed annual date range, show a clear warning:

“This visit is usually available August 2–7. The attached dates may not match the event period.”

Do not block the user from attaching or publishing the visit.

Do not fetch official event calendars. Do not guarantee availability.

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
* Optional region
* Published/unpublished status

Education cards can be attached to an itinerary.

Support attaching an education card either:

* To the itinerary as a whole
* To a date range

Keep this simple. Do not attach cards to arbitrary internal objects unless that is easier than date-range attachment.

### Voting

Signed-in users can upvote or downvote a public itinerary.

A vote must include one or more predefined reasons.

Each user may have only one current vote per itinerary. They may change or remove their vote.

Public users should see only the score, not the aggregate reason breakdown.

Admins should be able to view aggregate vote counts by reason.

Upvote reasons:

* Clear transit structure
* Useful cultural context
* Good regional focus
* Good pacing
* Helpful education cards
* Interesting destination choices
* Easy to understand
* Good use of trains/buses

Downvote reasons:

* Transit details unclear
* Too little cultural context
* Too generic
* Hard to follow
* Seems unrealistic
* Overloaded itinerary
* Weak education cards
* Poor regional focus
* Missing important transit notes

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
* Creator username
* Total duration
* Last updated
* Public score

### `/itineraries/<id>/`

Public itinerary detail page.

Respect visibility:

* Public: visible to everyone
* Unlisted: visible to anyone with the URL
* Private: visible only to owner and admins

Display:

* Title
* Author
* Description
* Visibility if owner/admin
* Total duration
* Last updated
* Public score
* Vote controls if signed in and not owner
* Date-grouped itinerary content

Date-grouped content should show:

* Transit legs for that date
* Visits active on that date
* Education cards active on that date or attached to the itinerary as a whole

For each visit, show culturally meaningful information:

* English name
* Japanese name
* Reading if present
* Cultural significance
* Access note
* Etiquette note if present
* Seasonality/timing note if present
* Timing warning if applicable

### `/itineraries/new/`

Create itinerary.

Signed-in users only.

### `/itineraries/<id>/edit/`

Edit itinerary.

Owner and admins only.

Must support:

* Editing title, description, visibility
* Adding/editing/deleting transit legs
* Attaching/removing visits with start/end dates
* Attaching/removing education cards with optional start/end dates

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

Use Django admin heavily.

Admins should be able to manage:

* Visits
* Education cards
* Itineraries
* Transit legs
* Visit attachments
* Education card attachments
* Votes
* User profiles

Admin-only vote reason aggregates can be implemented as a simple admin page, model admin method, or read-only admin display. Keep it simple.

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

Include at least one time-sensitive visit, such as:

* Hakata Gion Yamakasa

  * Fixed annual range: July 1–15
  * Climax: July 15
  * Timing note: Major Hakata festival; itinerary dates should align with the festival period.

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
* Time-sensitive visits display timing notes and warnings when appropriate
* A public itinerary can be browsed from the itinerary index
* Public itinerary index can sort by name, user, last updated, and total duration
* A user profile shows Gravatar, short bio, and that user’s itineraries
* A signed-in user can upvote/downvote a public itinerary with required reasons
* Normal users do not see aggregate vote reason counts
* Admins can see aggregate vote reason counts
* Admins can manage visits and education cards through Django admin
* The app runs locally with a single documented setup command sequence
