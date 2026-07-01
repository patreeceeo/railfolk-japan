# Summary

The app lets users manually create Japan transit itineraries using trains and buses. Users can attach prefabricated culturally meaningful visits and prefabricated education cards to their itineraries. Itineraries are public or unlisted. Public itineraries can be browsed and sorted. Other signed-in users can upvote or downvote an itinerary, but they must select one or more predefined reasons. Aggregate vote reason counts are visible only to admins.

This is not a general transit app. It does not calculate routes, validate schedules, book travel, reserve seats, sell passes, optimize fares, or fetch live transit data. It is focused on intercity travel within Japan rather than travel within Japan's metro areas.

# Target User

English-speaker interested in the broad array of authentic cultural experiences Japan has to offer. Other interests include trains, public transit, video games, comics/manga, animation and technology.

# Goals

The main goal is to be so good at promoting over-land Japan tourism that Japan's rail companies want to sponsor it. In order to do that, the app must be focused, intuitive, useful and fun to use for the target users.

# Competitive Framing

The category trap: Every existing tool in this space — Google Maps, Rome2Rio, Hyperdia/Jorudan, Wanderlog — is a utility. You open it because you already know where you're going and need the fastest, cheapest, or most correct way to get there. They're optimized for a single moment: departure day. Once the trip is booked, the tool's job is done, and there's nothing to return to.
Railfolk Japan isn't competing in that category. It's not trying to be a faster Rome2Rio. It's the thing people open six months before a trip exists — or with no trip planned at all — the way people browse Zillow without buying a house, or build a Steam wishlist without a paycheck to spend. The behavior it's designed around is daydreaming, not departing.
The reframe:

Most rail-planning tools assume you already know where you're going. Railfolk Japan assumes you don't — yet — and turns the discovering into the product, not a tax you pay before the "real" tool takes over.

Three ways to state the differentiation:

1. **Against the category (positioning statement)**: Rome2Rio answers 'how do I get from Fukuoka to Nagasaki.' Railfolk Japan answers 'what would three weeks discovering Kyushu by rail actually look like' — and lets you build, share, and vote on the answer before you've bought a single ticket.
2. **Against the behavior (why it's sticky)**: A trip planner is a checkout flow — you use it once per trip and leave. Railfolk Japan is a browsing surface — itineraries are content, not transactions, so there's a reason to come back even when you have no trip booked.
3. **Against the outcome**: The itinerary that comes out the other end is real and usable — but that's the receipt, not the point. The point is the hour someone spends discovering that there's a rail line through Northern Kyushu with three stops they'd never heard of, built entirely out of curiosity about the network itself.

Navigation apps have zero incentive to make a rail company's network look interesting, only to make a specific trip look fast. A tool that makes people fall in love with the shape of the rail map itself is doing marketing work no navigation app is structurally capable of doing, because it isn't trying to.

## Why Not Just Use...

### Rome2Rio or Google Maps?
These are routing engines, and they're excellent at their actual job: telling you the fastest way from point A to point B, right now, using live schedule data. But that's the whole job. The moment your route is found, the tool is finished with you — there's no reason to open it again until your next real trip. Railfolk Japan isn't trying to out-route them. It's for the six months before you have a real trip, when you're not asking "how do I get to Nagasaki" but "what's even out there in Kyushu worth getting to."

### Hyperdia or Jorudan?
These solve a narrower, more technical problem: precise timetables and transfer connections for travelers who already know their route and need it to actually work on the day. They're indispensable at departure time and irrelevant every other day of the year. Railfolk Japan deliberately doesn't compete on schedule precision — it models the network realistically enough to plan around, but the point isn't nailing your 8:42am transfer. It's discovering the transfer exists at all.

### Wanderlog or similar trip organizers?
These tools assume the hard part — deciding where to go — is already done, and their job is logistics: dates, bookings, day-by-day checklists for a trip that's already committed. Once the trip ends, the itinerary is archived and forgotten, because it was never meant to be seen by anyone but the traveler. Railfolk Japan flips that: the itinerary isn't a private checklist, it's a public, shareable piece of content that outlives the trip — browsed, voted on, and reused by people who've never met you.
The common thread: every one of these tools treats the itinerary as scaffolding you discard once the trip is over. Railfolk Japan treats the itinerary as the thing worth keeping — the trip, if it ever happens, is just proof the idea was good.

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

The displayed avatar should be served from `/avatar/<user_id>` and generated from the user's internal avatar key, not from email.

Fields:

* Email address
* User name
* List of itineraries created by that user

No followers, no activity feed, no badges.

### Itinerary

An itinerary is created by a user.

Fields:

* Title
* description
* Visibility: public, unlisted (note: there is no private option for now)
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
* Duration in hours

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
* Itinerary
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

* Uneccessary backtracking
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

* Avatar
* Username
* List of itineraries created by the user

For non-owner viewers, show only public itineraries. For owner/admin, show all their itineraries.

## Admin

Admins should be able to manage:

* Visits and attached visits
* Education cards and their associations
* Itineraries
* Transit legs
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
* A user profile shows Avatar, user name and that user’s itineraries
* A signed-in user can upvote/downvote a public itinerary with required reasons
* Normal users do not see aggregate vote reason counts
* Admins can see aggregate vote reason counts
* Admins can manage visits and education cards
* The app runs locally with a single documented setup command sequence
