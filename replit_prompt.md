# Replit Prompt: PPML/FHE Research PA — Conference Deadline Tracker & Calendar Assistant

## What to Build

Build a **full-stack Python web app** that acts as a personal research assistant (PA) for a PhD researcher working in Privacy-Preserving Machine Learning (PPML), Fully Homomorphic Encryption (FHE), and related cryptography/security fields. The app must:

1. Track **90+ conferences, workshops, journals, and events** with verified deadlines
2. Integrate with **Google Calendar** to create/update reminder events automatically
3. Run a **daily background scheduler** that checks deadlines and sends tiered reminders
4. Send **email notifications** (via Gmail SMTP or SendGrid) for approaching deadlines
5. Provide a **responsive web dashboard** showing upcoming deadlines, countdowns, and status
6. Auto-update event statuses (`cfp_open` → `cfp_closed` → `ongoing` → `past`) daily

The user's email is: `parthanupamnagar@gmail.com`

---

## Tech Stack

- **Backend**: Python 3.11+, Flask, SQLAlchemy, APScheduler (for daily cron jobs)
- **Frontend**: Jinja2 templates, Bootstrap 5, vanilla JS (no React/Vue needed)
- **Database**: SQLite (via Flask-SQLAlchemy)
- **Calendar**: Google Calendar API (via `google-api-python-client`, OAuth2)
- **Email**: Gmail SMTP (`smtplib`) or SendGrid API
- **Scheduler**: APScheduler (`BackgroundScheduler`) running inside the Flask app
- **Deployment**: Replit (always-on, with Replit secrets for API keys)

---

## Core Features

### 1. Conference Database (Pre-seeded)

Seed the database on first run with ALL of the following events. Each event has these fields:

```python
class Event:
    id: int (primary key)
    title: str
    category: str  # conference, workshop, journal, seminar, school, call_for_chapters
    edition: str (optional)
    website: str (optional)
    association: str (optional)  # ACM, IEEE, IACR, USENIX, AAAI
    relevance_tags: str  # comma-separated: "FHE, PPML, MPC, DP, FL"
    location: str  # "India", "Outside", "Online"
    city: str (optional)
    submission_deadline: date (optional)
    notification_date: date (optional)
    camera_ready_date: date (optional)
    event_start_date: date (optional)
    event_end_date: date (optional)
    description: str
    notes: str (optional)
    status: str  # upcoming, cfp_open, cfp_closed, ongoing, past
    pinned: bool (default False)
    reminder_90d_sent: bool (default False)
    reminder_60d_sent: bool (default False)
    reminder_30d_sent: bool (default False)
    reminder_14d_sent: bool (default False)
    reminder_7d_sent: bool (default False)
    reminder_3d_sent: bool (default False)
    reminder_1d_sent: bool (default False)
    calendar_event_id: str (optional)  # Google Calendar event ID for dedup
```

### COMPLETE SEED DATA — International Conferences

```
NeurIPS 2026
  website: https://neurips.cc/Conferences/2026/Dates
  tags: ML, DL, PPML, FL, DP
  location: Outside | city: Sydney, Australia
  submission_deadline: 2026-05-06
  notification_date: 2026-09-24
  event_start: 2026-12-06 | event_end: 2026-12-12
  notes: Abstract deadline May 4, 2026. Full paper deadline May 6, 2026 AOE. Position Papers track shares same deadlines (2nd year). Satellites in Atlanta & Paris.
  status: upcoming

ICML 2026 - International Conference on Machine Learning
  website: https://icml.cc/Conferences/2026/Dates
  tags: ML, DL, PPML, FL, DP
  location: Outside | city: Seoul, South Korea
  submission_deadline: 2026-05-23
  event_start: 2026-07-06 | event_end: 2026-07-11
  notes: Abstract deadline May 16, 2026. Full paper deadline May 23, 2026.
  status: upcoming

ICLR 2026 - International Conference on Learning Representations
  website: https://iclr.cc/Conferences/2026/Dates
  tags: ML, DL, PPML, Representation Learning
  location: Outside | city: Rio de Janeiro, Brazil
  submission_deadline: 2025-09-24
  notification_date: 2026-01-25
  event_start: 2026-04-23 | event_end: 2026-04-27
  notes: Abstract Sep 19, full paper Sep 24, 2025 AOE.
  status: upcoming

AAAI 2026
  website: https://aaai.org/conference/aaai/aaai-26/
  association: AAAI
  tags: AI, ML, PPML, PPAI Workshop
  location: Outside | city: Singapore
  submission_deadline: 2025-08-01
  notification_date: 2025-11-08
  event_start: 2026-01-20 | event_end: 2026-01-27
  notes: Abstract Jul 25, full paper Aug 1, 2025 AOE. Workshops Jan 26-27.
  status: upcoming

IEEE SaTML 2026 - Secure and Trustworthy Machine Learning
  edition: 4th
  website: https://satml.org/
  association: IEEE
  tags: Secure ML, Trustworthy ML, Adversarial ML, PPML
  location: Outside | city: Munich, Germany
  submission_deadline: 2025-09-24
  notification_date: 2025-12-10
  event_start: 2026-03-23 | event_end: 2026-03-25
  notes: Early reject notification Oct 29, 2025.
  status: upcoming

ACM PQQS 2026 - Post-Quantum and Quantum-based Security
  website: https://pqqs.org/
  association: ACM
  tags: Post-Quantum Cryptography, Quantum Security, PQC
  location: Outside | city: San Jose, CA, USA
  submission_deadline: 2026-07-26
  notification_date: 2026-09-15
  event_start: 2026-11-02 | event_end: 2026-11-04
  notes: First edition. Camera-ready deadline TBD.
  status: upcoming

CRYPTO 2026
  website: https://crypto.iacr.org/2026/
  association: IACR
  tags: Cryptography, FHE, MPC, ZKP
  location: Outside | city: Santa Barbara, CA
  submission_deadline: 2026-02-13
  notification_date: 2026-05-04
  event_start: 2026-08-17 | event_end: 2026-08-20
  status: upcoming

EUROCRYPT 2026
  website: https://eurocrypt.iacr.org/2026/
  association: IACR
  tags: Cryptography, FHE, MPC, PKC
  location: Outside | city: Italy
  submission_deadline: 2025-10-03
  event_start: 2026-05-10 | event_end: 2026-05-14
  status: upcoming

ASIACRYPT 2025
  website: https://asiacrypt.iacr.org/2025/
  association: IACR
  tags: Cryptography, FHE, MPC, Lattice
  location: Outside | city: Melbourne, Australia
  submission_deadline: 2025-05-16
  notification_date: 2025-08-10
  event_start: 2025-12-08 | event_end: 2025-12-12
  notes: Two-round review: 1st notify Jul 13, rebuttal Jul 18, final notify Aug 10.
  status: upcoming

ACM CCS 2026 - Computer and Communications Security
  website: https://sigsac.org/ccs/CCS2026/
  association: ACM
  tags: Security, Privacy, MPC, PPML
  location: Outside | city: The Hague, Netherlands
  submission_deadline: 2026-04-29
  event_start: 2026-11-15 | event_end: 2026-11-19
  notes: Two cycles: Cycle A deadline Jan 14, Cycle B deadline Apr 29, 2026.
  status: upcoming

USENIX Security 2026
  website: https://www.usenix.org/conference/usenixsecurity26
  association: USENIX
  tags: Security, Privacy, PPML, Systems Security
  location: Outside | city: Baltimore, MD
  submission_deadline: 2026-02-05
  event_start: 2026-08-12 | event_end: 2026-08-14
  notes: Two cycles: Cycle 1 submit Aug 26, 2025. Cycle 2 submit Feb 5, 2026.
  status: upcoming

NDSS 2026 - Network and Distributed System Security
  website: https://www.ndss-symposium.org/ndss2026/
  tags: Network Security, Distributed Systems, FL, PPML
  location: Outside | city: San Diego, CA
  submission_deadline: 2025-08-07
  event_start: 2026-02-23 | event_end: 2026-02-27
  notes: Two cycles: Summer deadline Apr 24, Fall deadline Aug 7, 2025.
  status: upcoming

IEEE S&P 2026 - Symposium on Security and Privacy
  website: https://sp2026.ieee-security.org/cfpapers.html
  association: IEEE
  tags: Security, Privacy, PPML, MPC, FHE
  location: Outside | city: San Francisco, CA
  submission_deadline: 2025-11-14
  notification_date: 2026-03-19
  event_start: 2026-05-18 | event_end: 2026-05-21
  notes: Cycle 1: Jun 6, 2025. Cycle 2: Nov 14, 2025.
  status: upcoming

PETS / PoPETs 2026 - Privacy Enhancing Technologies
  website: https://petsymposium.org/cfp26.php
  tags: PETs, DP, PPML, Anonymity, FHE
  location: Outside
  notes: 4 rolling deadlines: Issue 1 (May 31, 2025), Issue 2 (Aug 31, 2025), Issue 3 (Nov 30, 2025), Issue 4 (Feb 28, 2026). All 23:59 AoE.
  status: cfp_open

PETS / PoPETs 2027 - Privacy Enhancing Technologies
  website: https://petsymposium.org/cfp27.php
  tags: PETs, DP, PPML, Anonymity, FHE
  location: Outside | city: Europe (TBD)
  submission_deadline: 2026-05-31
  notification_date: 2026-08-01
  event_start: 2027-07-15 | event_end: 2027-07-20
  notes: Issue 1: May 31 2026 (notify Aug 1). Issue 2: Aug 31 2026 (notify Nov 1). Issue 3: Nov 30 2026 (notify Feb 1). Issue 4: Feb 28 2027 (notify May 1). All 23:59 AoE.
  status: cfp_open

Real World Crypto (RWC) 2026
  website: https://rwc.iacr.org/2026/
  association: IACR
  tags: Applied Cryptography, FHE, MPC, Industry
  location: Outside | city: Taipei, Taiwan
  submission_deadline: 2025-10-10
  event_start: 2026-03-07 | event_end: 2026-03-09
  notes: Contributed talks deadline Oct 10, 2025.
  status: upcoming

FHE.org Conference 2026
  website: https://fhe.org/conferences/conference-2026/call-for-presentations
  tags: FHE, Homomorphic Encryption, Applications
  location: Outside | city: Taipei, Taiwan
  submission_deadline: 2025-11-01
  notification_date: 2025-12-19
  event_start: 2026-03-08 | event_end: 2026-03-08
  notes: Extended abstract deadline Nov 1, 2025 AoE.
  status: upcoming

ACSAC 2025 - Annual Computer Security Applications Conference
  website: https://www.acsac.org/2025/
  tags: Applied Security, PPML, Systems
  location: Outside | city: Honolulu, HI
  submission_deadline: 2025-05-30
  notification_date: 2025-09-03
  event_start: 2025-12-08 | event_end: 2025-12-12
  notes: Early reject notification Jul 14, 2025.
  status: upcoming
```

### COMPLETE SEED DATA — Additional International Conferences (no specific dates yet)

```
PEPR - Privacy Engineering Practice and Respect (USENIX)
TCC - Theory of Cryptography Conference (IACR)
PKC - International Conference on Public-Key Cryptography (IACR)
CT-RSA - Cryptographers' Track at RSA
FC - Financial Cryptography and Data Security (IFCA)
ESORICS - European Symposium on Research in Computer Security
IEEE EuroS&P - European Symposium on Security and Privacy
ACNS - Applied Cryptography and Network Security
CODASPY - ACM Conference on Data and Application Security and Privacy
MLSys - Conference on ML and Systems
PST - International Conference on Privacy, Security and Trust
ISC - International Security Conference (MPC, HE, PKC, PQC)
IEEE CSR - Cyber Security and Resilience (Chania, Crete, Greece)
STOC 2026 - ACM Symposium on Theory of Computing
HLF - Heidelberg Laureate Forum
CAMLIS - Conference on Applied ML in Information Security
XAI for Privacy-Preserving Machine Learning
```

### COMPLETE SEED DATA — India Conferences

```
CASML 2025 - International Conference on Applied AI and Scientific ML
  website: https://casml.cc/
  tags: Applied AI, Scientific ML
  location: India | city: IISc Bangalore
  submission_deadline: 2025-10-24
  notification_date: 2025-11-03
  event_start: 2025-12-08 | event_end: 2025-12-11
  notes: Extended abstract deadline. Early registration ends Nov 30.
  status: upcoming

CODS-COMAD 2025 (ACM India)
  website: https://ikdd.acm.org/cods-2025/
  tags: Data Science, ML, Data Management
  location: India | city: IISER Pune
  event_start: 2025-12-17 | event_end: 2025-12-20
  notes: 2026 CFP not yet announced.
  status: upcoming

INDOCRYPT 2025
  website: https://www.indocrypt2025.in/
  tags: Cryptography, Indian Crypto Community
  location: India | city: Bhubaneswar
  submission_deadline: 2025-09-01
  notification_date: 2025-10-10
  event_start: 2025-12-14 | event_end: 2025-12-17
  notes: 26th International Conference on Cryptology in India. IACR. Springer LNCS.
  status: upcoming

SPACE 2025 - Security, Privacy, and Applied Cryptography Engineering
  website: https://event.iitg.ac.in/space2025/
  tags: Security, Privacy, Applied Cryptography
  location: India | city: IIT Guwahati
  submission_deadline: 2025-09-15
  notification_date: 2025-10-29
  event_start: 2025-12-16 | event_end: 2025-12-19
  notes: Two rounds: Round 1 deadline May 8, Round 2 deadline Sep 15 (extended). LNCS proceedings.
  status: upcoming

ICSP 2026 - 5th International Conference on Security & Privacy
  website: https://icsp.co.in/2026/dates.html
  tags: Security, Privacy
  location: India | city: NIT Warangal
  submission_deadline: 2026-07-15
  notification_date: 2026-09-25
  event_start: 2026-11-26 | event_end: 2026-11-28
  notes: Notification date estimated from ICSP 2025 pattern.
  status: upcoming

ICMC - International Conference on Mathematics and Computing (IIT Bhilai)
ICCNSML - Conference on Cryptology and Network Security with ML
MIND-2025 - ML, Image Processing, Network Security and Data Sciences
ANTIC 2025 - Advanced Network Technologies and Intelligent Computing
ISCS2025 - Intelligent Systems for Cybersecurity
ISEA-ISAP 2026 - International Conference on Security and Privacy (IIT Madras)
XAI-2025
3rd Symposium on Data for Public Good
ICACSDF2025 - Applied Computing, Security and Digital Forensics
```

### COMPLETE SEED DATA — Workshops

```
WAHC 2026 - 14th Workshop on Encrypted Computing & Applied HE
  website: https://homomorphicencryption.org/workshops/
  tags: FHE, HE, Encrypted Computing, Applications
  location: Outside | city: The Hague, Netherlands
  submission_deadline: 2026-06-27
  notification_date: 2026-08-08
  event_start: 2026-11-15 | event_end: 2026-11-15
  notes: Co-located with ACM CCS 2026.
  status: upcoming

IACR PPML Workshop (co-located with CRYPTO)
PPAI - Privacy-Preserving AI @ AAAI
PML - Private ML Workshop @ ICLR
AISEC - ACM Workshop on AI Security
DLSP - Deep Learning and Security Workshop (IEEE)
DSML - Dependable and Secure ML
AISCC - NDSS Workshop on AI Systems with Confidential Computing
CSCML - Cyber Security, Cryptology and ML Symposium
RWMPC 2025 - Real World MPC Workshop (MPC Alliance)
LightSEC 2025 - Lightweight Cryptography (Istanbul, Turkey)
AAMAD 2025 - Advancing AI and ML Across Disciplines
TPDP 2025 - Theory and Practice of Differential Privacy
FL@NeurIPS - Federated Learning Workshop
WPES - Workshop on Privacy in the Electronic Society (ACM, at CCS)
```

### COMPLETE SEED DATA — Journals (status: ongoing, no deadlines)

```
IJISP - International Journal of Information Security and Privacy
Security and Privacy (Wiley)
IEEE Security and Privacy Magazine
ACM TOPS - Transactions on Privacy and Security
Foundations and Trends in ML
MAKE - Machine Learning and Knowledge Extraction (MDPI)
ML: Science and Technology (IOP)
Journal of Privacy and Confidentiality
JMLR - Journal of Machine Learning Research
PoPETs - Proceedings on Privacy Enhancing Technologies
IEEE TPAMI
AI Review (Springer)
Journal of Cryptology (IACR/Springer)
IEEE TDSC - Trans. on Dependable and Secure Computing
IEEE TIFS - Trans. on Information Forensics and Security
```

---

## 2. Google Calendar Integration

### Setup
- Use Google Calendar API with OAuth2 (store credentials in Replit Secrets)
- Create a dedicated calendar called **"Research Deadlines"** (or use a specific calendar ID from secrets)

### What to Sync
For every event with a `submission_deadline`, create **tiered reminder calendar events**:

| Reminder | When | Calendar Event Title | Color |
|----------|------|---------------------|-------|
| 90-day heads-up | 90 days before deadline | "[90d] CONF_NAME — Submission opens soon" | Blue |
| 60-day planning | 60 days before deadline | "[60d] CONF_NAME — Start planning submission" | Green |
| 30-day warning | 30 days before deadline | "[30d] CONF_NAME — 1 month to deadline" | Yellow |
| 14-day alert | 14 days before deadline | "[14d] CONF_NAME — 2 weeks left!" | Orange |
| 7-day urgent | 7 days before deadline | "[7d] CONF_NAME — 1 WEEK LEFT" | Red |
| 3-day critical | 3 days before deadline | "[3d] CONF_NAME — SUBMIT IN 3 DAYS" | Red |
| 1-day final | 1 day before deadline | "[1d] CONF_NAME — DEADLINE TOMORROW" | Red |
| D-Day | On deadline day | "DEADLINE TODAY: CONF_NAME" | Red |

Each calendar event should include in its description:
- Conference name and website URL
- Submission deadline date
- Event dates and location/city
- Relevance tags
- Any notes (e.g. abstract deadline, multi-cycle info)

Also create calendar events for:
- **Notification dates** (when to expect accept/reject)
- **Conference dates** (multi-day events)
- **Rolling deadlines** (PoPETs issues — create separate reminders for each issue)

### Deduplication
- Store `calendar_event_id` in the database to avoid creating duplicate events
- On each daily run, only create events that haven't been created yet
- If a deadline date changes, update the existing calendar event

---

## 3. Email Notifications

### Daily Digest Email (sent at 8:00 AM IST)
Send to `parthanupamnagar@gmail.com` every morning with:

```
Subject: Research PA Daily Brief — [DATE]

URGENT DEADLINES (next 7 days):
  - [3d] WAHC 2026 — Submit by Jun 27 (encrypted computing workshop)
  - [1d] PoPETs 2027 Issue 1 — Submit by May 31 (privacy technologies)

UPCOMING DEADLINES (next 30 days):
  - [28d] ICML 2026 — Submit by May 23 (ML conference, Seoul)
  - [14d] ACM PQQS 2026 — Submit by Jul 26 (post-quantum security)

NEWLY OPEN CFPs:
  - CRYPTO 2027 CFP announced — deadline TBD

CONFERENCES THIS MONTH:
  - NeurIPS 2026 — Dec 6-12, Sydney, Australia

STATUS CHANGES:
  - ICML 2026: cfp_open → cfp_closed (deadline passed)

---
Your Research PA | Manage at [dashboard_url]
```

### Milestone Emails
Send additional emails at the 30d, 14d, 7d, 3d, and 1d marks for each conference the user has **pinned**.

---

## 4. Daily Background Scheduler

Use APScheduler `BackgroundScheduler` with a cron trigger:

```python
scheduler = BackgroundScheduler()
scheduler.add_job(daily_check, 'cron', hour=2, minute=30)  # 2:30 AM UTC = 8:00 AM IST
scheduler.start()
```

The `daily_check()` function should:
1. **Update event statuses** — same logic as `update_event_statuses()` above
2. **Check each event** for approaching deadlines and send appropriate reminders
3. **Sync new calendar events** for any newly approaching milestones
4. **Send daily digest email** with all relevant updates
5. **Log the run** with timestamp and actions taken

---

## 5. Web Dashboard

### Pages

**Dashboard Home (`/`)**
- Countdown cards for the next 5 deadlines (with days remaining, color-coded)
- "This Month" section showing conferences happening this month
- "Action Required" section for deadlines in next 14 days
- Quick stats: total events, open CFPs, pinned events, past events

**Events (`/events`)**
- Filterable table of all events
- Filter by: category (conference/workshop/journal), location (India/Outside), status, tags
- Search by title
- Sort by deadline date, event date, or title
- Pin/unpin events (pinned = get extra email reminders)
- Color-coded status badges: green=cfp_open, yellow=upcoming, orange=cfp_closed, red=past, blue=ongoing

**Calendar View (`/calendar`)**
- Monthly calendar view showing all deadlines and events
- Color-coded by category
- Click to see event details

**Timeline (`/timeline`)**
- Gantt-style timeline showing submission→notification→event flow for each conference
- Visual overview of the research calendar year

**Settings (`/settings`)**
- Google Calendar connection status
- Email notification preferences (toggle daily digest, choose which reminder tiers)
- Add/edit custom events
- Manual "sync now" button for calendar
- View scheduler run history/logs

### API Endpoints
```
GET  /api/events                    — all events (JSON, filterable)
GET  /api/events/upcoming           — events with future deadlines
GET  /api/events/deadlines          — deadlines in next 90 days
POST /api/events/<id>/pin           — toggle pin
POST /api/events/<id>/update        — update event details
POST /api/sync/calendar             — trigger calendar sync
GET  /api/stats                     — dashboard statistics
```

---

## 6. Auto-Status Update Logic

Run daily. For each event not already marked `past`:

```python
today = date.today()
if event_end_date and event_end_date < today:
    status = 'past'
elif event_start_date and event_start_date <= today <= event_end_date:
    status = 'ongoing'
elif submission_deadline and submission_deadline >= today:
    status = 'cfp_open'
elif submission_deadline and submission_deadline < today:
    status = 'cfp_closed'
elif event_start_date and event_start_date > today:
    status = 'upcoming'
else:
    status = 'past'
```

---

## 7. Special Handling

### Rolling Deadlines (PoPETs)
PoPETs has 4 issues per year. Create **separate reminder chains** for each issue deadline. When Issue 1 deadline passes, automatically show Issue 2 as the next active deadline.

### Multi-Cycle Conferences (CCS, USENIX Security, IEEE S&P, NDSS)
These have 2 submission cycles. Store the latest upcoming cycle as `submission_deadline` and document all cycles in `notes`. After Cycle 1 passes, update to show Cycle 2.

### Pinned Events
Users can pin high-priority conferences. Pinned events get:
- Extra email reminders (at each tier)
- Highlighted on dashboard
- Priority sorting

---

## 8. Researchers Database (Reference)

Also seed a researchers table for reference (displayed on a `/researchers` page):

```
Craig Gentry — TripleBlind — FHE inventor
Vinod Vaikunthanathan — MIT CSAIL / Duality — FHE, Lattice
Zvika Brakerski — Weizmann Institute — FHE, BGV
Kristin Lauter — Meta AI — FHE for ML
Nigel Smart — KU Leuven / Zama — FHE, MPC, IACR
Jung Hee Cheon — Seoul National University / CryptoLab — CKKS/HEAAN
Shai Halevi — Algorand / formerly IBM — HElib, BGV
Kim Laine — Microsoft Research — SEAL, PPML
Cynthia Dwork — Harvard — Differential Privacy inventor
Brendan McMahan — Google — Federated Learning (FedAvg) inventor
Arpita Patra — IISc Bangalore — Secure MPC, PPML
J. Harshan — IIT Delhi — HE, FL
Ranjitha Prasad — IIT Delhi — FL
Andrew Trask — OpenMined — FL, PySyft
Peter Kairouz — Google Research — FL, DP
Yehuda Lindell — Bar-Ilan / Coinbase — MPC
Ran Canetti — Boston University — MPC, Universal Composability
Ilya Mironov — Apple — DP, Renyi DP
Yongsoo Song — Seoul National University — FHE, CKKS
```

---

## 9. Resources Database (Reference)

Seed a resources table (`/resources` page) with FHE/PPML libraries, companies, and tools:

**Libraries**: OpenFHE, Microsoft SEAL, TenSEAL, ConcreteML, HEAAN, PySyft, TF Federated, Flower, NVIDIA FLARE, Opacus, Google DP Library, TFHE-rs, Lattigo, HElib, MP-SPDZ, ABY/ABY3

**Companies**: Zama, Duality Technologies, CryptoLab, Opaque Systems, Arcium, Inpher, Roseman Labs, Sherpa.ai, Apheris, TII

**Organisations**: FHE.org, HomomorphicEncryption.org, MPC Alliance, OpenMined, ACL SIGSEC

**Platforms**: Cryptology ePrint Archive, Papers With Code (Privacy), FedML, NIST PPML

---

## 10. Environment Variables (Replit Secrets)

```
GOOGLE_CALENDAR_CREDENTIALS  — OAuth2 service account JSON
GOOGLE_CALENDAR_ID            — calendar ID to sync to
SMTP_EMAIL                    — sender email
SMTP_PASSWORD                 — app password for Gmail
NOTIFICATION_EMAIL            — parthanupamnagar@gmail.com
FLASK_SECRET_KEY              — random secret key
```

---

## 11. File Structure

```
/
├── app.py                  # Flask app, routes, scheduler setup
├── models.py               # SQLAlchemy models
├── seed_data.py            # All seed data (events, researchers, resources)
├── calendar_sync.py        # Google Calendar integration
├── email_service.py        # Email notification logic
├── scheduler_jobs.py       # Daily check, reminder logic
├── templates/
│   ├── base.html           # Bootstrap 5 layout
│   ├── dashboard.html      # Home dashboard with countdowns
│   ├── events.html         # Filterable events table
│   ├── calendar.html       # Monthly calendar view
│   ├── timeline.html       # Gantt-style timeline
│   ├── researchers.html    # Researchers directory
│   ├── resources.html      # Resources directory
│   └── settings.html       # Settings and sync controls
├── static/
│   ├── css/style.css
│   └── js/app.js
├── requirements.txt
└── .replit
```

---

## 12. Key Implementation Notes

1. **Always-on**: The Replit app must stay running 24/7 for the scheduler to work. Use Replit's "Always On" feature.
2. **Timezone**: All internal processing in UTC. Display in IST (UTC+5:30) for the user. Deadline comparisons use AoE (UTC-12) where noted.
3. **Idempotent**: The daily job must be idempotent — running it twice on the same day should not create duplicate calendar events or send duplicate emails. Use the `reminder_*_sent` flags.
4. **Graceful degradation**: If Google Calendar API is not configured, the app should still work as a web dashboard with email-only reminders. If email is not configured, dashboard-only mode.
5. **No authentication needed**: This is a personal tool. No login required for the web dashboard.
6. **Mobile-friendly**: The dashboard must be responsive and usable on mobile browsers.
7. **Dark mode**: Support a dark/light toggle (default dark).

---

## Summary

Build a research PA that:
- Seeds 90+ PPML/FHE/crypto conferences with verified 2025-2027 deadlines
- Runs a daily cron job at 8 AM IST to check deadlines
- Creates tiered Google Calendar reminders (90d/60d/30d/14d/7d/3d/1d)
- Sends a daily digest email with urgent deadlines and status changes
- Shows a responsive web dashboard with countdowns, filters, calendar, and timeline
- Auto-updates event statuses daily
- Handles rolling deadlines (PoPETs) and multi-cycle submissions (CCS, USENIX, etc.)
- Is always-on, idempotent, and works even if external APIs aren't configured
