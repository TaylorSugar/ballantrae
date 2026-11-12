# -*- coding: utf-8 -*-
"""All copy and fixed facts for ballantrae.ca. Sales numbers are NOT here — they come from data/sales.json
(built from the official Excel workbook). For-sale homes come from data/for_sale.json.
Anything marked PLACEHOLDER is intentionally unconfirmed."""

SITE = dict(
  name="Ballantrae.ca", title="Real Estate Guide to Ballantrae Golf and Country Club",
  fullname="Ballantrae.ca : Real Estate Guide to Ballantrae Golf and Country Club", sugarteam_url="https://sugarteam.ca/",
  tagline="Sweeten the Deal with Sugar Team.",
  brand_lines=["Smart Real Estate", "Sweet People", "Successful Transitions"],
  preview_note="Preview build. ballantrae.ca is not connected to this preview.",
)

# Sugar Team contact details already confirmed on sugarteam.ca / Sugar Cubed reference build.
CONTACT = dict(
  taylor=dict(name="Taylor Sugar", phone="(416) 569-8919", tel="+14165698919", email="Taylor@sugarteam.ca", role="Broker / Team Manager"),
  leigh=dict(name="Leigh Sugar", phone="(416) 505-3040", tel="+14165053040", email="leigh@sugarteam.ca", role="Broker"),
  tollfree="1-866-773-9595", tollfree_tel="+18667739595", fax="(905) 836-0820",
  office="17360 Yonge Street, Newmarket, Ontario, L3Y 7R6",  # as published on sugarteam.ca (Contact page and footer)
  brokerage_line="Brokerage line to confirm",  # sugarteam.ca still shows Royal LePage RCR Realty, so no brokerage name is used here
  disclaimer=("All information displayed is believed to be accurate but is not guaranteed and should be independently verified. No warranties or representations are made of any kind. Not intended to solicit properties currently listed for sale. "
    "The trademarks REALTOR®, REALTORS® and the REALTOR® logo are controlled by The Canadian Real Estate Association (CREA) and identify real estate professionals who are members of CREA. "
    "The trademarks MLS®, Multiple Listing Service® and the associated logos are owned by CREA and identify the quality of services provided by real estate professionals who are members of CREA."),
)

# slug, display name (as in the Excel workbook), builder sq ft (printed on the brochure floor plan), elevation files, plan file
MODELS = [
  dict(slug="grand-cypress", name="Grand Cypress", sqft=2065, elev=["grand-cypress-elev1"]),
  dict(slug="doral",         name="Doral",         sqft=2025, elev=["doral-elev1","doral-elev2"]),
  dict(slug="augusta",       name="Augusta",       sqft=1910, elev=["augusta-elev1","augusta-elev2"]),
  dict(slug="castle-pines",  name="Castle Pines",  sqft=1855, elev=["castle-pines-elev1","castle-pines-elev2"]),
  dict(slug="innisbrook",    name="Innisbrook",    sqft=1704, elev=["innisbrook-elev1","innisbrook-elev2"]),
  dict(slug="pinehurst",     name="Pinehurst",     sqft=1700, elev=["pinehurst-elev1","pinehurst-elev2"]),
  dict(slug="pebble-beach",  name="Pebble Beach",  sqft=1470, elev=["pebble-beach-elev1","pebble-beach-elev2"]),
]

CONDOS = [  # unit counts as printed on the condominium map in Taylor's Dropbox folder
  dict(n=1, corp="968",  units=250, streets="Masters Tournament winners"),
  dict(n=2, corp="1002", units=205, streets="U.S. Open winners"),
  dict(n=3, corp="1066", units=108, streets="CPGA champions"),
  dict(n=4, corp="1079", units=172, streets="British Open winners"),
  dict(n=5, corp="1193", units=159, streets="'Lady' legends of golf"),
]

# Public sources actually used for the community text. Text on the site is written in our own words.
SOURCES = dict(
  club=dict(label="Ballantrae Golf Club (official site)", url="https://www.ballantraegolfclub.com/"),
  rates=dict(label="Ballantrae Golf Club: 2026 rates", url="https://www.ballantraegolfclub.com/rates/"),
  dining=dict(label="Ballantrae Golf Club: dining", url="https://www.ballantraegolfclub.com/dining/"),
  packages=dict(label="Ballantrae Golf Club: multiple play packages", url="https://www.ballantraegolfclub.com/multiple-play-packages/"),
  golfcanada=dict(label="Golf Canada facility listing", url="https://www.golfcanada.ca/golf-facility/ballantrae-golf-club-en/"),
  fairways=dict(label="Fairways Golf & Travel: Your Next Round, Ballantrae", url="https://fairwaysgolf.ca/your-next-round-ballantrae-golf-club-stouffville-ontario/"),
  fairways2=dict(label="Fairways Golf & Travel: Doing it well at Ballantrae", url="https://fairwaysgolf.ca/doing-it-well-at-ballantrae/"),
)

TEAM = [  # names/titles exactly as supplied by Taylor, left to right in the team photo (photo from sugarteam.ca)
  ("Sarah Lawrence","Sales Representative"),("Martin Wales","Marketing Manager / Sales Representative"),("Leigh Sugar","Broker"),
  ("Taylor Sugar","Broker / Team Manager"),("David Fletcher","Sales Representative"),("Blair Dunlop","Mortgage Broker / Broker")]

# Stock photography (Pexels, free under the Pexels License; generic golf scenery, NOT Ballantrae)
STOCK = {
  "fairway": ("Michael Francis Redmond","https://www.pexels.com/photo/golf-course-fairways-with-bunkers-8218725/","Fairway under blue sky"),
  "lush":    ("Calvin Seng","https://www.pexels.com/photo/lush-green-golf-course-landscape-under-clear-sky-32401757/","Lush golf course landscape"),
  "bunkers": ("Kindel Media","https://www.pexels.com/photo/photo-of-a-golf-course-6573872/","Golf course with bunkers"),
  "sunset":  ("cottonbro studio","https://www.pexels.com/photo/green-grass-field-under-the-white-clouds-6256829/","Golf course at sunset"),
  "flag":    ("Rushay Booysen","https://www.pexels.com/photo/golf-hole-with-red-flag-4398355/","Red flag on the green"),
}
