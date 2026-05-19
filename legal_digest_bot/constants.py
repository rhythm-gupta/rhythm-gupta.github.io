"""Domain constants and keyword lists for the legal digest bot."""

SOURCE_URLS = [
    "https://www.livelaw.in/",
    "https://www.barandbench.com/",
    "https://www.scconline.com/blog/",
    "https://www.verdictum.in/",
]

COURT_KEYWORDS = {
    "Supreme Court of India": [
        "supreme court",
        "sc",
        "cji",
    ],
    "Delhi High Court": [
        "delhi high court",
        "dhc",
    ],
}

ACT_KEYWORDS = [
    "constitution of india",
    "code of civil procedure",
    "code of criminal procedure",
    "indian penal code",
    "indian contract act",
    "limited liability partnership act",
    "arbitration and conciliation act",
    "indian evidence act",
    "specific relief act",
    "limitation act",
    "sale of goods act",
    "partnership act",
    "transfer of property act",
    "hindu law",
    "mohammedan law",
    "delhi rent control act",
    "negotiable instruments act",
    "prevention of corruption act",
    "protection of children from sexual offences act",
    "juvenile justice",
    "information technology act",
    "prevention of money laundering act",
    "protection of women from domestic violence act",
    "dowry prohibition act",
    "bharatiya nyaya sanhita",
    "bharatiya nagarik suraksha sanhita",
    "bharatiya sakshya adhiniyam",
]

PDF_HINTS = ["judgment", "order", "verdict", "pdf"]
