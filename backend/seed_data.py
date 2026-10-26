import uuid
from datetime import datetime, timedelta, timezone

CATEGORIES = [
    {"slug": "video-editing", "label": "Video Editors"},
    {"slug": "motion-3d", "label": "3D & Motion"},
    {"slug": "thumbnails", "label": "Thumbnail Design"},
    {"slug": "scriptwriting", "label": "Scriptwriting"},
    {"slug": "ugc", "label": "UGC Creators"},
    {"slug": "strategy", "label": "Creative Strategy"},
]

WELCOME_GRANT = 40
UNLOCK_COST = 5
BOOST_COST = 10
BUNDLES = [
    {"id": "starter", "label": "Starter pack", "tokens": 20, "display_price": "$19 (demo)"},
    {"id": "studio", "label": "Studio pack", "tokens": 60, "display_price": "$49 (demo)"},
    {"id": "agency", "label": "Agency pack", "tokens": 150, "display_price": "$109 (demo)"},
]


def _days(n):
    return (datetime.now(timezone.utc) + timedelta(days=n)).isoformat()


def _p(pid, title, client, cover, views, duration, tools):
    return {"id": pid, "title": title, "client": client, "cover": cover, "views": views,
            "duration": duration, "format": "9:16", "tools": tools}


TALENTS = [
    {
        "id": "tal-sophia-vance", "name": "Sophia Vance", "handle": "@sophiacuts", "avatar": "/media/a1.jpg",
        "headline": "Short-form editor for DTC beauty & lifestyle brands", "category": "video-editing",
        "skills": ["Premiere Pro", "CapCut", "Hook writing", "Captions"], "location": "Lisbon, PT",
        "timezone": "WET", "day_rate": 420, "project_rate_from": 900, "rating": 4.9, "reviews_count": 61,
        "completed_projects": 148, "response_time": "~1 hr", "availability": "Available now", "verified": True,
        "languages": ["English", "Portuguese"],
        "bio": "I turn raw UGC into scroll-stopping 9:16 ads. Former agency lead editor; I obsess over the first 1.5 seconds.",
        "portfolio": [
            _p("pf-1", "Glow serum launch — 3 hook variants", "Lumen Skin", "/media/p12.jpg", "2.4M", "0:28", ["Premiere", "AE"]),
            _p("pf-2", "Founder story cutdown", "Haven Home", "/media/p8.jpg", "860K", "0:45", ["CapCut"]),
            _p("pf-3", "Holiday gifting reel", "Oakline", "/media/p6.jpg", "1.1M", "0:19", ["Premiere"]),
        ],
        "services": [
            {"name": "3 short-form ad edits", "price": 900, "turnaround": "4 days"},
            {"name": "Monthly retainer (12 edits)", "price": 3200, "turnaround": "Ongoing"},
        ],
        "reviews": [
            {"author": "Maya R.", "company": "Lumen Skin", "rating": 5, "text": "Our CTR doubled on her first batch of hooks."},
            {"author": "Jon P.", "company": "Oakline", "rating": 5, "text": "Fast, clear communication, zero hand-holding."},
        ],
        "contact": {"email": "sophia.vance@demo-creator.example", "calendar": "cal.example/sophia-vance"},
    },
    {
        "id": "tal-marcus-chen", "name": "Marcus Chen", "handle": "@marcus3d", "avatar": "/media/a7.jpg",
        "headline": "3D product animation & motion systems", "category": "motion-3d",
        "skills": ["Blender", "Cinema 4D", "Octane", "After Effects"], "location": "Toronto, CA",
        "timezone": "EST", "day_rate": 650, "project_rate_from": 2400, "rating": 4.8, "reviews_count": 38,
        "completed_projects": 72, "response_time": "~3 hrs", "availability": "Booked until next month", "verified": True,
        "languages": ["English", "Mandarin"],
        "bio": "Photoreal product renders and looping motion for launches. I build reusable scene kits so your team can iterate.",
        "portfolio": [
            _p("pf-4", "Glass bottle hero loop", "Nimbus Water", "/media/p2.jpg", "540K", "0:12", ["Blender", "Octane"]),
            _p("pf-5", "Abstract brand ident", "Kinetic Labs", "/media/p4.jpg", "310K", "0:08", ["C4D"]),
            _p("pf-6", "Wearable feature explainer", "Pulse Band", "/media/p1.jpg", "1.9M", "0:30", ["Blender", "AE"]),
        ],
        "services": [
            {"name": "Product hero animation", "price": 2400, "turnaround": "10 days"},
            {"name": "Motion scene kit", "price": 4800, "turnaround": "3 weeks"},
        ],
        "reviews": [{"author": "Priya S.", "company": "Pulse Band", "rating": 5, "text": "Renders looked better than our actual photos."}],
        "contact": {"email": "marcus.chen@demo-creator.example", "calendar": "cal.example/marcus-chen"},
    },
    {
        "id": "tal-elena-rostova", "name": "Elena Rostova", "handle": "@elenathumbs", "avatar": "/media/a3.jpg",
        "headline": "YouTube thumbnails engineered for CTR", "category": "thumbnails",
        "skills": ["Photoshop", "A/B testing", "Typography", "Retouching"], "location": "Warsaw, PL",
        "timezone": "CET", "day_rate": 300, "project_rate_from": 180, "rating": 5.0, "reviews_count": 112,
        "completed_projects": 640, "response_time": "~30 min", "availability": "Available now", "verified": True,
        "languages": ["English", "Polish", "Russian"],
        "bio": "Designed thumbnails for channels from 50K to 8M subscribers. Every design ships with 2 test variants.",
        "portfolio": [
            _p("pf-7", "Tech review series refresh", "Byte Bench", "/media/p3.jpg", "4.2M", "Static", ["Photoshop"]),
            _p("pf-8", "Travel vlog pack", "Nomad Notes", "/media/p9.jpg", "980K", "Static", ["Photoshop"]),
        ],
        "services": [
            {"name": "Thumbnail + 2 variants", "price": 180, "turnaround": "48 hrs"},
            {"name": "Channel rebrand (10)", "price": 1500, "turnaround": "7 days"},
        ],
        "reviews": [{"author": "Ade O.", "company": "Byte Bench", "rating": 5, "text": "CTR went from 4.1% to 9.8% in a month."}],
        "contact": {"email": "elena.rostova@demo-creator.example", "calendar": "cal.example/elena"},
    },
    {
        "id": "tal-david-kim", "name": "David Kim", "handle": "@kimvfx", "avatar": "/media/a8.jpg",
        "headline": "VFX & compositing for music and fashion", "category": "motion-3d",
        "skills": ["Nuke", "After Effects", "Rotoscoping", "Color"], "location": "Seoul, KR",
        "timezone": "KST", "day_rate": 580, "project_rate_from": 1800, "rating": 4.7, "reviews_count": 27,
        "completed_projects": 55, "response_time": "~6 hrs", "availability": "Available now", "verified": False,
        "languages": ["English", "Korean"],
        "bio": "Compositing, beauty work and stylised VFX for vertical music videos and fashion drops.",
        "portfolio": [
            _p("pf-9", "Light-tunnel music teaser", "Neon Hours", "/media/p6.jpg", "3.3M", "0:15", ["Nuke"]),
            _p("pf-10", "Runway glitch edit", "Atelier Nine", "/media/p10.jpg", "720K", "0:22", ["AE"]),
        ],
        "services": [{"name": "VFX shot package (5 shots)", "price": 1800, "turnaround": "8 days"}],
        "reviews": [{"author": "Lea M.", "company": "Atelier Nine", "rating": 4, "text": "Stunning work, slightly over timeline."}],
        "contact": {"email": "david.kim@demo-creator.example", "calendar": "cal.example/davidkim"},
    },
    {
        "id": "tal-amara-okafor", "name": "Amara Okafor", "handle": "@amarawrites", "avatar": "/media/a4.jpg",
        "headline": "Scripts & hooks for educational creators", "category": "scriptwriting",
        "skills": ["Scriptwriting", "Research", "Story structure", "Hooks"], "location": "Lagos, NG",
        "timezone": "WAT", "day_rate": 280, "project_rate_from": 350, "rating": 4.9, "reviews_count": 44,
        "completed_projects": 210, "response_time": "~2 hrs", "availability": "Available now", "verified": True,
        "languages": ["English", "Yoruba"],
        "bio": "I write retention-first scripts for long-form and Shorts. Science, finance and history channels are my sweet spot.",
        "portfolio": [
            _p("pf-11", "Finance explainer Shorts", "Coin Clarity", "/media/p11.jpg", "1.4M", "0:58", ["Docs"]),
            _p("pf-12", "History deep-dive script", "Past Forward", "/media/p5.jpg", "620K", "12:40", ["Docs"]),
        ],
        "services": [
            {"name": "Short-form script pack (5)", "price": 350, "turnaround": "3 days"},
            {"name": "Long-form script", "price": 600, "turnaround": "5 days"},
        ],
        "reviews": [{"author": "Tom H.", "company": "Coin Clarity", "rating": 5, "text": "Average view duration up 22%."}],
        "contact": {"email": "amara.okafor@demo-creator.example", "calendar": "cal.example/amara"},
    },
    {
        "id": "tal-jade-moreau", "name": "Jade Moreau", "handle": "@jadeugc", "avatar": "/media/a2.jpg",
        "headline": "On-camera UGC for fashion & wellness", "category": "ugc",
        "skills": ["On-camera", "Self-shot", "Voiceover", "Unboxing"], "location": "Paris, FR",
        "timezone": "CET", "day_rate": 350, "project_rate_from": 450, "rating": 4.8, "reviews_count": 53,
        "completed_projects": 190, "response_time": "~1 hr", "availability": "Available now", "verified": True,
        "languages": ["English", "French"],
        "bio": "Natural, unscripted-feeling UGC. Studio-lit at home, delivered with raw files and usage rights options.",
        "portfolio": [
            _p("pf-13", "Morning routine try-on", "Linen & Co", "/media/p12.jpg", "2.0M", "0:34", ["iPhone"]),
            _p("pf-14", "Supplement unboxing", "Root Daily", "/media/p7.jpg", "410K", "0:25", ["iPhone"]),
        ],
        "services": [{"name": "3 UGC videos + raw", "price": 450, "turnaround": "6 days"}],
        "reviews": [{"author": "Ana L.", "company": "Root Daily", "rating": 5, "text": "Felt authentic — best-performing ad this quarter."}],
        "contact": {"email": "jade.moreau@demo-creator.example", "calendar": "cal.example/jade"},
    },
    {
        "id": "tal-rafael-ortiz", "name": "Rafael Ortiz", "handle": "@rafaelstrat", "avatar": "/media/a5.jpg",
        "headline": "Creative strategist for paid social", "category": "strategy",
        "skills": ["Ad testing", "Briefs", "Meta Ads", "TikTok Ads"], "location": "Mexico City, MX",
        "timezone": "CST", "day_rate": 700, "project_rate_from": 2000, "rating": 4.9, "reviews_count": 19,
        "completed_projects": 41, "response_time": "~4 hrs", "availability": "2 slots this month", "verified": True,
        "languages": ["English", "Spanish"],
        "bio": "I build creative testing roadmaps and briefs your editors can actually execute. Ex-performance lead at a DTC unicorn.",
        "portfolio": [
            _p("pf-15", "Q4 testing roadmap", "Oakline", "/media/p9.jpg", "—", "Deck", ["Figma"]),
            _p("pf-16", "Hook library build", "Haven Home", "/media/p8.jpg", "—", "Deck", ["Notion"]),
        ],
        "services": [{"name": "Creative audit + roadmap", "price": 2000, "turnaround": "1 week"}],
        "reviews": [{"author": "Chris B.", "company": "Haven Home", "rating": 5, "text": "Cut our CPA by a third in six weeks."}],
        "contact": {"email": "rafael.ortiz@demo-creator.example", "calendar": "cal.example/rafael"},
    },
    {
        "id": "tal-noah-becker", "name": "Noah Becker", "handle": "@noahedits", "avatar": "/media/a6.jpg",
        "headline": "Long-form YouTube editor, documentary style", "category": "video-editing",
        "skills": ["DaVinci Resolve", "Sound design", "Color grading", "Pacing"], "location": "Berlin, DE",
        "timezone": "CET", "day_rate": 480, "project_rate_from": 1200, "rating": 4.6, "reviews_count": 33,
        "completed_projects": 88, "response_time": "~5 hrs", "availability": "Available next week", "verified": False,
        "languages": ["English", "German"],
        "bio": "Cinematic pacing for 15–40 minute videos. I also cut the Shorts from every long-form I edit.",
        "portfolio": [
            _p("pf-17", "City at night mini-doc", "Urban Lens", "/media/p10.jpg", "1.2M", "18:22", ["Resolve"]),
            _p("pf-18", "Studio tour cutdown", "Byte Bench", "/media/p5.jpg", "340K", "0:50", ["Resolve"]),
        ],
        "services": [{"name": "Long-form edit + 3 Shorts", "price": 1200, "turnaround": "7 days"}],
        "reviews": [{"author": "Sam K.", "company": "Urban Lens", "rating": 5, "text": "Retention graph has never looked this good."}],
        "contact": {"email": "noah.becker@demo-creator.example", "calendar": "cal.example/noah"},
    },
]

JOBS = [
    {"id": "job-lumen-hooks", "title": "Short-form ad editor for skincare launch", "brand": "Lumen Skin",
     "owner_id": "seed-brand-lumen", "category": "video-editing", "budget_min": 1500, "budget_max": 2500,
     "budget_type": "fixed", "deadline": _days(12), "location": "Remote", "urgency": "hot", "boosted": True,
     "description": "We need 6 vertical ad edits from existing UGC footage with 3 hook variants each.",
     "deliverables": ["6 x 9:16 edits (15–30s)", "3 hook variants per edit", "Burned-in captions"],
     "skills": ["Premiere Pro", "Hook writing", "Captions"], "posted_at": _days(-1), "applicants_count": 14},
    {"id": "job-pulse-3d", "title": "3D product animation for wearable", "brand": "Pulse Band",
     "owner_id": "seed-brand-pulse", "category": "motion-3d", "budget_min": 3000, "budget_max": 5000,
     "budget_type": "fixed", "deadline": _days(25), "location": "Remote", "urgency": "standard", "boosted": False,
     "description": "Photoreal hero animation plus 4 feature callouts for our Gen-3 launch.",
     "deliverables": ["30s hero (16:9 + 9:16)", "4 x 8s feature loops", "Project files"],
     "skills": ["Blender", "Octane"], "posted_at": _days(-3), "applicants_count": 6},
    {"id": "job-bytebench-thumbs", "title": "Thumbnail designer — 8 videos/month", "brand": "Byte Bench",
     "owner_id": "seed-brand-bytebench", "category": "thumbnails", "budget_min": 120, "budget_max": 200,
     "budget_type": "per item", "deadline": _days(5), "location": "Remote", "urgency": "hot", "boosted": True,
     "description": "Tech review channel (1.2M subs) looking for a long-term thumbnail partner.",
     "deliverables": ["8 thumbnails / month", "2 variants each for testing"],
     "skills": ["Photoshop", "A/B testing"], "posted_at": _days(-2), "applicants_count": 31},
    {"id": "job-coin-scripts", "title": "Scriptwriter for finance Shorts", "brand": "Coin Clarity",
     "owner_id": "seed-brand-coin", "category": "scriptwriting", "budget_min": 60, "budget_max": 90,
     "budget_type": "per item", "deadline": _days(9), "location": "Remote", "urgency": "standard", "boosted": False,
     "description": "Write punchy 45–60s scripts explaining personal finance concepts for Gen Z.",
     "deliverables": ["10 scripts / month", "Hook + CTA options"], "skills": ["Scriptwriting", "Research"],
     "posted_at": _days(-5), "applicants_count": 9},
    {"id": "job-rootdaily-ugc", "title": "UGC creators for supplement brand", "brand": "Root Daily",
     "owner_id": "seed-brand-root", "category": "ugc", "budget_min": 400, "budget_max": 700,
     "budget_type": "fixed", "deadline": _days(14), "location": "Remote (EU/US)", "urgency": "standard",
     "boosted": False, "description": "Looking for 5 creators to film morning-routine style videos featuring our greens powder.",
     "deliverables": ["3 videos per creator", "Raw footage", "90-day paid usage"],
     "skills": ["On-camera", "Self-shot"], "posted_at": _days(-4), "applicants_count": 22},
    {"id": "job-haven-strategy", "title": "Creative strategist (contract, 3 months)", "brand": "Haven Home",
     "owner_id": "seed-brand-haven", "category": "strategy", "budget_min": 650, "budget_max": 800,
     "budget_type": "day", "deadline": _days(20), "location": "Remote (Americas)", "urgency": "hot", "boosted": False,
     "description": "Own our paid-social creative testing roadmap and brief 3 freelance editors weekly.",
     "deliverables": ["Weekly briefs", "Monthly test readout", "Hook library"],
     "skills": ["Meta Ads", "Briefs", "Ad testing"], "posted_at": _days(-1), "applicants_count": 4},
    {"id": "job-urbanlens-doc", "title": "Long-form documentary editor", "brand": "Urban Lens",
     "owner_id": "seed-brand-urban", "category": "video-editing", "budget_min": 1800, "budget_max": 2600,
     "budget_type": "fixed", "deadline": _days(30), "location": "Remote", "urgency": "standard", "boosted": False,
     "description": "Edit a 25-minute mini-doc about night-shift workers, plus 3 vertical cutdowns.",
     "deliverables": ["25 min edit", "Color + sound mix", "3 x 9:16 cutdowns"],
     "skills": ["DaVinci Resolve", "Sound design"], "posted_at": _days(-6), "applicants_count": 11},
]


def user_workspace_seed(user_id: str) -> dict:
    t1, t2, t3 = (str(uuid.uuid4()) for _ in range(3))
    threads = [
        {"id": t1, "user_id": user_id, "counterpart": "Maya R. · Lumen Skin", "avatar": "/media/a1.jpg",
         "subject": "Hook variants for launch", "unread": 2, "updated_at": _days(-0.05)},
        {"id": t2, "user_id": user_id, "counterpart": "Marcus Chen", "avatar": "/media/a7.jpg",
         "subject": "Render timeline question", "unread": 0, "updated_at": _days(-0.6)},
        {"id": t3, "user_id": user_id, "counterpart": "Creator Hub Support", "avatar": None,
         "subject": "Welcome to your demo workspace", "unread": 1, "updated_at": _days(-1)},
    ]
    msgs = [
        (t1, "them", "Hi! Loved your reel. Could you share 2 more hook ideas for the serum ad?", -0.2),
        (t1, "me", "Absolutely — I'll send a rough cut with both by tomorrow.", -0.15),
        (t1, "them", "Perfect. Attaching the brand guidelines PDF (demo file).", -0.05),
        (t2, "them", "The glass bottle loop will take about 6 working days. Does that work?", -0.7),
        (t2, "me", "Yes, that fits our schedule. Thanks Marcus!", -0.6),
        (t3, "them", "Everything here is sample data. Messages you send are stored only in this demo and never delivered.", -1),
    ]
    messages = [{"id": str(uuid.uuid4()), "thread_id": tid, "user_id": user_id, "sender": s, "body": b,
                 "created_at": _days(d)} for tid, s, b, d in msgs]
    tasks_src = [
        ("Lumen Skin launch", "Collect UGC footage", "done"), ("Lumen Skin launch", "Draft 3 hook variants", "review"),
        ("Lumen Skin launch", "Caption pass", "in_progress"), ("Lumen Skin launch", "Final export 9:16", "todo"),
        ("Pulse Band animation", "Approve styleframes", "done"), ("Pulse Band animation", "Hero render v1", "in_progress"),
        ("Pulse Band animation", "Feature loop callouts", "todo"), ("Pulse Band animation", "Sound design", "todo"),
    ]
    tasks = [{"id": str(uuid.uuid4()), "user_id": user_id, "project": p, "title": t, "status": s,
              "due": _days(i + 2), "created_at": _days(-i)} for i, (p, t, s) in enumerate(tasks_src)]
    settings = {"user_id": user_id, "public_profile": True, "show_rates": True, "allow_direct_messages": True,
                "incognito_browsing": False, "show_in_search": True}
    return {"threads": threads, "messages": messages, "tasks": tasks, "settings": settings}
