from datetime import date

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from itineraries.models import (
    AttachedTransitLeg,
    AttachedVisitCard,
    EducationCard,
    Itinerary,
    Location,
    TransitLeg,
    UserProfile,
    VisitCard,
)


class Command(BaseCommand):
    help = "Seed representative Railfolk Japan data."

    def handle(self, *args, **options):
        users = self.seed_users()
        locations = self.seed_locations()
        education_cards = self.seed_education_cards(locations)
        visit_cards = self.seed_visit_cards(locations)
        transit_legs = self.seed_transit_legs(locations)
        self.seed_itineraries(users, education_cards, visit_cards, transit_legs)
        self.stdout.write(self.style.SUCCESS("Seed data loaded."))

    def seed_users(self):
        User = get_user_model()
        users = {}
        user_rows = [
            {
                "username": "railfolk-aya",
                "email": "aya@example.com",
                "first_name": "Aya",
                "last_name": "Nakamura",
                "short_bio": "Kyushu rail planner focused on slower local journeys.",
            },
            {
                "username": "railfolk-ben",
                "email": "ben@example.com",
                "first_name": "Ben",
                "last_name": "Carter",
                "short_bio": "First-time Japan traveler collecting practical route notes.",
            },
            {
                "username": "railfolk-mika",
                "email": "mika@example.com",
                "first_name": "Mika",
                "last_name": "Tanaka",
                "short_bio": "Onsen and shrine etiquette guide for western Kyushu.",
            },
        ]

        for row in user_rows:
            user, created = User.objects.get_or_create(
                username=row["username"],
                defaults={
                    "email": row["email"],
                    "first_name": row["first_name"],
                    "last_name": row["last_name"],
                },
            )
            if created:
                user.set_unusable_password()
                user.save()
            else:
                user.email = row["email"]
                user.first_name = row["first_name"]
                user.last_name = row["last_name"]
                user.save(update_fields=["email", "first_name", "last_name"])

            UserProfile.objects.update_or_create(
                user=user,
                defaults={"short_bio": row["short_bio"]},
            )
            users[row["username"]] = user

        return users

    def seed_locations(self):
        rows = [
            {
                "name": "Kushida Shrine",
                "description": "Historic Hakata shrine associated with the Yamakasa festival.",
                "latitude": "33.593030",
                "longitude": "130.410716",
                "address": "1-41 Kamikawabatamachi, Hakata Ward, Fukuoka",
            },
            {
                "name": "Dejima",
                "description": "Restored fan-shaped trading post in central Nagasaki.",
                "latitude": "32.744981",
                "longitude": "129.873573",
                "address": "6-1 Dejimamachi, Nagasaki",
            },
            {
                "name": "Sofukuji Temple",
                "description": "Chinese-style Obaku Zen temple with vivid red gates.",
                "latitude": "32.742071",
                "longitude": "129.884333",
                "address": "7-5 Kajiyamachi, Nagasaki",
            },
            {
                "name": "Nagasaki Peace Park",
                "description": "Memorial park and museum district north of central Nagasaki.",
                "latitude": "32.773766",
                "longitude": "129.864708",
                "address": "Matsuyamamachi, Nagasaki",
            },
            {
                "name": "Suizenji Garden",
                "description": "Strolling garden in Kumamoto built around spring-fed ponds.",
                "latitude": "32.790577",
                "longitude": "130.733893",
                "address": "8-1 Suizenji Koen, Chuo Ward, Kumamoto",
            },
            {
                "name": "Kumamoto Castle area",
                "description": "Castle grounds and surrounding streets in central Kumamoto.",
                "latitude": "32.806186",
                "longitude": "130.705834",
                "address": "1-1 Honmaru, Chuo Ward, Kumamoto",
            },
            {
                "name": "Takeo Onsen",
                "description": "Historic hot spring town with a landmark vermilion gate.",
                "latitude": "33.193700",
                "longitude": "130.022750",
                "address": "Takeocho Takeo, Takeo, Saga",
            },
            {
                "name": "Yufuin",
                "description": "Mountain onsen town with galleries, cafes, and Kinrin Lake.",
                "latitude": "33.262617",
                "longitude": "131.354401",
                "address": "Yufuincho Kawakami, Yufu, Oita",
            },
            {
                "name": "Beppu jigoku area",
                "description": "Steam-filled hot spring sightseeing area in northern Beppu.",
                "latitude": "33.316287",
                "longitude": "131.477169",
                "address": "Kannawa, Beppu, Oita",
            },
            {
                "name": "Dazaifu Tenmangu",
                "description": "Major Tenjin shrine reached easily from Fukuoka by train.",
                "latitude": "33.521451",
                "longitude": "130.534830",
                "address": "4-7-1 Saifu, Dazaifu, Fukuoka",
            },
        ]

        locations = {}
        for row in rows:
            location, _ = Location.objects.update_or_create(
                name=row["name"],
                defaults={
                    "description": row["description"],
                    "latitude": row["latitude"],
                    "longitude": row["longitude"],
                    "address": row["address"],
                },
            )
            locations[row["name"]] = location

        return locations

    def seed_education_cards(self, locations):
        rows = [
            {
                "title": "Shinkansen vs limited express",
                "category": EducationCard.Category.RAIL,
                "body": "Shinkansen services are built for speed on dedicated lines. Limited express trains use conventional tracks and often reach smaller cities directly.",
            },
            {
                "title": "Local train vs rapid train",
                "category": EducationCard.Category.RAIL,
                "body": "Local trains stop at every station. Rapid trains skip smaller stops, so check whether your destination is served before boarding.",
            },
            {
                "title": "Rural bus caution",
                "category": EducationCard.Category.RAIL,
                "body": "Rural buses may run only a few times daily. Confirm the return trip before leaving the station area.",
            },
            {
                "title": "Station vocabulary",
                "category": EducationCard.Category.LANGUAGE,
                "body": "Useful words include eki for station, noriba for platform or boarding point, and kippu for ticket.",
            },
            {
                "title": "Shrine etiquette",
                "category": EducationCard.Category.CULTURE,
                "body": "At shrines, bow before entering, rinse hands at the basin when available, and keep photos respectful around worshippers.",
                "location": "Dazaifu Tenmangu",
            },
            {
                "title": "Temple etiquette",
                "category": EducationCard.Category.CULTURE,
                "body": "At temples, move quietly, follow posted photo rules, and avoid stepping on thresholds when entering older halls.",
                "location": "Sofukuji Temple",
            },
            {
                "title": "Onsen basics",
                "category": EducationCard.Category.CULTURE,
                "body": "Wash before entering the bath, keep towels out of the water, and check tattoo policies before arrival.",
                "location": "Takeo Onsen",
            },
            {
                "title": "Ekiben",
                "category": EducationCard.Category.CULTURE,
                "body": "Ekiben are station bento boxes. Buy before boarding longer trains because onboard food options vary by route.",
            },
            {
                "title": "Omiyage",
                "category": EducationCard.Category.CULTURE,
                "body": "Omiyage are regional gifts, usually boxed sweets or snacks, brought back for coworkers, friends, or family.",
            },
            {
                "title": "Kyushu regional context",
                "category": EducationCard.Category.REGIONAL_CONTEXT,
                "body": "Kyushu travel mixes major rail corridors with mountainous local lines, ferry history, hot springs, and layered trade routes.",
            },
        ]

        cards = {}
        for row in rows:
            card, _ = EducationCard.objects.update_or_create(
                title=row["title"],
                defaults={
                    "category": row["category"],
                    "body": row["body"],
                    "location": locations.get(row.get("location")),
                },
            )
            cards[row["title"]] = card

        return cards

    def seed_visit_cards(self, locations):
        rows = [
            ("Kushida Shrine", "1.00", 0),
            ("Dejima", "1.50", 520),
            ("Sofukuji Temple", "1.00", 300),
            ("Nagasaki Peace Park", "2.00", 0),
            ("Suizenji Garden", "1.50", 400),
            ("Kumamoto Castle area", "2.50", 800),
            ("Takeo Onsen", "2.00", 500),
            ("Yufuin", "3.00", 0),
            ("Beppu jigoku area", "3.00", 2200),
            ("Dazaifu Tenmangu", "2.00", 0),
        ]

        visit_cards = {}
        for location_name, suggested_hours, admission_yen in rows:
            visit_card, _ = VisitCard.objects.update_or_create(
                location=locations[location_name],
                defaults={
                    "suggested_hours": suggested_hours,
                    "admission_yen": admission_yen,
                },
            )
            visit_cards[location_name] = visit_card

        return visit_cards

    def seed_transit_legs(self, locations):
        rows = [
            ("Kushida Shrine", "Dazaifu Tenmangu", TransitLeg.Mode.TRAIN, "Nishitetsu", "Tenjin Omuta/Dazaifu Line", 420, 1),
            ("Dazaifu Tenmangu", "Kushida Shrine", TransitLeg.Mode.TRAIN, "Nishitetsu", "Dazaifu/Tenjin Omuta Line", 420, 1),
            ("Kushida Shrine", "Takeo Onsen", TransitLeg.Mode.SHINKANSEN, "JR Kyushu", "Relay Kamome/Nishi Kyushu Shinkansen", 3600, 1),
            ("Takeo Onsen", "Dejima", TransitLeg.Mode.SHINKANSEN, "JR Kyushu", "Nishi Kyushu Shinkansen", 3600, 1),
            ("Dejima", "Sofukuji Temple", TransitLeg.Mode.TRAIN, "Nagasaki Electric Tramway", "Line 1/5", 140, 1),
            ("Sofukuji Temple", "Nagasaki Peace Park", TransitLeg.Mode.TRAIN, "Nagasaki Electric Tramway", "Line 1", 140, 1),
            ("Nagasaki Peace Park", "Kumamoto Castle area", TransitLeg.Mode.LIMITED_EXPRESS, "JR Kyushu", "Kamome/Shinkansen transfer", 7500, 1),
            ("Kumamoto Castle area", "Suizenji Garden", TransitLeg.Mode.TRAIN, "Kumamoto City Tram", "A Line", 180, 1),
            ("Suizenji Garden", "Yufuin", TransitLeg.Mode.BUS, "Kyushu Sanko Bus", "Kyushu Odan Bus", 4500, 1),
            ("Yufuin", "Beppu jigoku area", TransitLeg.Mode.BUS, "Kamenoi Bus", "Yufuin-Beppu Line", 1000, 1),
            ("Beppu jigoku area", "Kushida Shrine", TransitLeg.Mode.LIMITED_EXPRESS, "JR Kyushu", "Sonic", 6500, 1),
        ]

        transit_legs = {}
        for (
            origin_name,
            destination_name,
            mode,
            operator,
            line_name,
            fare_yen,
            duration_days,
        ) in rows:
            transit_leg, _ = TransitLeg.objects.update_or_create(
                origin=locations[origin_name],
                destination=locations[destination_name],
                mode=mode,
                operator=operator,
                line_name=line_name,
                defaults={
                    "fare_yen": fare_yen,
                    "duration_days": duration_days,
                },
            )
            transit_legs[(origin_name, destination_name)] = transit_leg

        return transit_legs

    def seed_itineraries(self, users, education_cards, visit_cards, transit_legs):
        rows = [
            {
                "title": "Hakata shrine day",
                "description": "A public day plan pairing Hakata's central shrine with Dazaifu.",
                "owner": "railfolk-aya",
                "legs": [
                    ("Kushida Shrine", "Dazaifu Tenmangu", date(2026, 4, 3)),
                    ("Dazaifu Tenmangu", "Kushida Shrine", date(2026, 4, 3)),
                ],
                "visits": [
                    ("Kushida Shrine", date(2026, 4, 3), "Start early before Kawabata arcade gets busy."),
                    ("Dazaifu Tenmangu", date(2026, 4, 3), "Leave time for the approach street and umegae mochi."),
                ],
                "education": [
                    "Shrine etiquette",
                    "Local train vs rapid train",
                    "Omiyage",
                ],
            },
            {
                "title": "Nagasaki history loop",
                "description": "A compact public route through trading history, temple streets, and peace memorials.",
                "owner": "railfolk-ben",
                "legs": [
                    ("Kushida Shrine", "Takeo Onsen", date(2026, 5, 10)),
                    ("Takeo Onsen", "Dejima", date(2026, 5, 10)),
                    ("Dejima", "Sofukuji Temple", date(2026, 5, 11)),
                    ("Sofukuji Temple", "Nagasaki Peace Park", date(2026, 5, 11)),
                ],
                "visits": [
                    ("Takeo Onsen", date(2026, 5, 10), "Use the onsen stop as a calm transfer break."),
                    ("Dejima", date(2026, 5, 10), "Good first stop for Nagasaki trade history."),
                    ("Sofukuji Temple", date(2026, 5, 11), "Pair with nearby Teramachi streets."),
                    ("Nagasaki Peace Park", date(2026, 5, 11), "Keep the afternoon unhurried."),
                ],
                "education": [
                    "Shinkansen vs limited express",
                    "Temple etiquette",
                    "Onsen basics",
                    "Kyushu regional context",
                ],
            },
            {
                "title": "Kumamoto to Oita onsen arc",
                "description": "A public cross-Kyushu route from Kumamoto gardens to Yufuin and Beppu.",
                "owner": "railfolk-mika",
                "legs": [
                    ("Nagasaki Peace Park", "Kumamoto Castle area", date(2026, 6, 15)),
                    ("Kumamoto Castle area", "Suizenji Garden", date(2026, 6, 16)),
                    ("Suizenji Garden", "Yufuin", date(2026, 6, 17)),
                    ("Yufuin", "Beppu jigoku area", date(2026, 6, 18)),
                    ("Beppu jigoku area", "Kushida Shrine", date(2026, 6, 19)),
                ],
                "visits": [
                    ("Kumamoto Castle area", date(2026, 6, 15), "Check current access routes around restoration works."),
                    ("Suizenji Garden", date(2026, 6, 16), "Morning visit leaves the afternoon flexible."),
                    ("Yufuin", date(2026, 6, 17), "Reserve lodging before planning late arrivals."),
                    ("Beppu jigoku area", date(2026, 6, 18), "The jigoku are for viewing, not bathing."),
                ],
                "education": [
                    "Rural bus caution",
                    "Station vocabulary",
                    "Onsen basics",
                    "Ekiben",
                    "Kyushu regional context",
                ],
            },
        ]

        for row in rows:
            itinerary, _ = Itinerary.objects.update_or_create(
                title=row["title"],
                owner=users[row["owner"]],
                defaults={
                    "description": row["description"],
                    "visibility": Itinerary.Visibility.PUBLIC,
                },
            )

            itinerary.education_cards.set(
                education_cards[title] for title in row["education"]
            )

            wanted_leg_ids = set()
            for origin_name, destination_name, start_date in row["legs"]:
                attached_leg, _ = AttachedTransitLeg.objects.update_or_create(
                    itinerary=itinerary,
                    transit_leg=transit_legs[(origin_name, destination_name)],
                    start_date=start_date,
                    defaults={},
                )
                wanted_leg_ids.add(attached_leg.id)
            itinerary.attached_transit_legs.exclude(id__in=wanted_leg_ids).delete()

            wanted_visit_ids = set()
            for location_name, start_date, note in row["visits"]:
                attached_visit, _ = AttachedVisitCard.objects.update_or_create(
                    itinerary=itinerary,
                    visit_card=visit_cards[location_name],
                    start_date=start_date,
                    defaults={"note": note},
                )
                wanted_visit_ids.add(attached_visit.id)
            itinerary.attached_visit_cards.exclude(id__in=wanted_visit_ids).delete()
