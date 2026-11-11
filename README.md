# Screenlane — Cinema Booking Website

A complete, customizable Python/Flask cinema application with responsive HTML/CSS, UC3M MariaDB database, SQLAlchemy ORM, customer accounts, booking logic, food bundles and a staff management dashboard.

**Classic cinema edition:** Restyled from the basic prototype you supplied: black navigation bar, charcoal cards, red headings and buttons, compact movie grid and simplified forms. All original customer and management features remain part of the application.

> **Development project:** The default configuration is for local development. Configure HTTPS, persistent secrets, backups and production-grade hosting before exposing it publicly.

## Features

| Customer / visitor | Management staff |
| --- | --- |
| See all movies and search by title or genre | Add movies, including poster images |
| See details and future showtimes by day | Add screens and set their seating capacities |
| Register and sign in securely | Schedule screenings in specific rooms |
| Reserve one or more available seats without choosing seat numbers | Reject overlapping screen schedules (15-minute turnover) |
| Get a ticket price based on screening weekday | Update ticket prices for Monday–Sunday |
| Book discounted one-ticket-and-food bundles | Add and edit drinks, snacks and ticket bundles |
| Add individual snacks and drinks | Deactivate menu items while preserving historic receipts |
| View upcoming bookings and past receipts | See an overview of screenings and customers |
| Pay on arrival, no card information required | Staff access is restricted by server-side role checks |

### Booking package pricing

Each package includes **one admission ticket** plus bundled snacks/drinks. Its stored `FoodBeverage.price` is the **discounted FOOD add-on**, not the admission charge.

Example with admission €10 and popcorn (€4.50) + cola (€3.50) package food add-on €6:

- One regular ticket: €10.
- One combo ticket: €10 ticket + €6 discounted food = **€16** (instead of €18 separately).
- Three seats with two combos: 1 × €10 regular ticket + 2 × €16 combos = **€42**.
- Any separately booked extras are then added. Packages may not exceed the seat count.

All prices and availability checks are recalculated **on the server**. Changing browser input values cannot change prices.

## Requirements and UC3M lab compatibility

- Python **3.11+** and pip
- Access from a **UC3M Telematic Engineering lab computer or Aula Virtual** (the university MariaDB server rejects connections from outside the lab)
- The assigned MariaDB user `27_webapp_03` and database `27_webapp_03a`
- No locally installed MySQL/MariaDB server is required

The application uses **Flask-SQLAlchemy** and the **PyMySQL** MariaDB connector. It reads `SQLALCHEMY_DATABASE_URI` and `SECRET_KEY` from a local `.env` file using `python-dotenv`. No SQLite database or demo-data seeding is needed for deployment.

## Install and configure on Aula Virtual / a lab computer

Open the project folder (the one containing `app.py`) in a terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

On Windows PowerShell, use:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edit the **local** `.env` file:

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
SQLALCHEMY_DATABASE_URI=mysql+pymysql://27_webapp_03:YOUR_PRIVATE_PASSWORD@mysql.lab.it.uc3m.es/27_webapp_03a
```

Replace `YOUR_PRIVATE_PASSWORD` with your assigned UC3M database password. Never upload this `.env` file to GitHub or put the password in Python source. Passwords containing URL-reserved characters must be URL-encoded in the URI.

If you want to check the database login before starting the application, use the lab terminal:

```bash
mysql -h mysql -u 27_webapp_03 -D 27_webapp_03a -p
```

Enter the password at the prompt and exit using `Ctrl-D`.

## Create tables — no sample-data seeding

```bash
python main.py init
```

This creates the application's database **tables only** in `27_webapp_03a`; it does not create example movies, screenings, food products, tickets, prices, customers, or bookings. Existing tables and their data are preserved. Running the command again is safe for unchanged schemas.

To enable management features on an empty database, create a staff login:

```bash
python main.py create-admin --admin-email manager@example.com
```

The command securely prompts twice for a staff password. No admin password is stored in source code or accepted on the command line.

Start the website:

```bash
python app.py
```

Open **http://127.0.0.1:5000/**. Log in using the staff account and use the dashboard to add:

1. Monday–Sunday admission prices (required before customer booking)
2. Cinema rooms and capacities
3. Movies and their posters
4. Screening schedules
5. Optional snacks, drinks and discounted packages

Customers can then register themselves and book screenings. With an empty database, there are initially no movies to display. The application does not require sample films or preloaded bookings to run.

The app's existing database models and booking behaviour are preserved. Changing the backend does not automatically import any records from an older SQLite database.

## Project structure

```text
screenlane/
├── app.py                     # Flask app factory, reads .env and configures MariaDB
├── main.py                    # Create tables and initial staff account (no seed)
├── models.py                  # SQLAlchemy models and relationships
├── requirements.txt           # Flask, PyMySQL, python-dotenv and dependencies
├── .env.example               # Safe, credential-free connection template
├── routes/
│   ├── auth.py                # Customer accounts and login
│   ├── public.py              # Movie and showtime pages
│   ├── bookings.py            # Reservations and private receipts
│   └── admin.py               # Staff management of catalog, rooms and prices
├── services/
│   ├── pricing.py
│   └── booking.py
├── templates/                 # Jinja2 pages
├── static/                    # CSS, JavaScript and poster images
└── tests/                     # Automated tests (isolated SQLite test databases)
```

## How to customize the website

**Colours / type / shape:** Edit the variables inside `:root { ... }` at the **top** of `static/css/classic-cinema.css`. This theme loads after the original `styles.css`, so its settings take priority.

The shared black navigation bar and footer live in `templates/base.html`. The movie catalog is in `templates/index.html`, and the redesigned login/register pages are in `templates/auth/`. Every other booking and staff view gets the same theme while retaining the original Jinja form names, CSRF tokens, data attributes and routes.

**To revert to the earlier design:** Remove the `classic-cinema.css` `<link>` from `templates/base.html`; to restore the old homepage and authentication layouts as well, copy back those templates and `base.html` from the original Screenlane ZIP.

| Variable | Controls |
| --- | --- |
| `--bg`, `--bg-card`, `--bg-elevated` | Background shades |
| `--text`, `--text-secondary` | Text colours |
| `--brand`, `--brand-hover`, `--brand-text` | Accent colour and buttons |
| `--font-body`, `--font-display` | Fonts |
| `--radius-sm`, `--radius-lg` | Rounded corners |
| `--container` | Maximum content width |

**Shared navigation and footer:** `templates/base.html`.

**Homepage layout:** `templates/index.html`.

**Movie detail and booking:** `templates/movie_detail.html` and `templates/showtime_detail.html`.

**All booking-price calculations:** `services/booking.py`; never rely on JS for security.

**New fields / database model:** Change `models.py`. **Important:** `db.create_all()` does **not** migrate existing MariaDB tables. For schema changes, use an appropriate migration process (e.g. Alembic/Flask-Migrate) and back up existing data.

**Poster images:** Staff can upload JPG/PNG/WebP posters that are converted to WebP. No sample-film generation is required.

## Security notes

- Passwords use Werkzeug's salted one-way password hashes. They cannot be decrypted, even by staff.
- Customer and staff roles are checked at the beginning of protected routes.
- Only the booking owner can view their reservation.
- SQLAlchemy uses bound parameters to prevent SQL injection.
- Jinja templates automatically HTML-escape user content; no unsafe HTML insertion is used.
- Flask-WTF requires CSRF tokens for POST forms (including logout and staff forms).
- Content Security Policy and secure response headers restrict external scripts, framing and unsafe object embeds.
- Poster uploads are limited by file extension, size and dimensions and re-encoded as raster images.
- Signed session cookies are HttpOnly and SameSite=Lax. Set `SESSION_COOKIE_SECURE=1` when serving over HTTPS.
- A reservation uses an atomic conditional UPDATE of remaining seats to reduce oversell risk during concurrent bookings.
- No payment processing or storage of card numbers is implemented, per the coursework specification.

Additional real-world production controls such as rate limiting, email verification, password recovery, audit logging, backups, external monitoring, and TLS configuration should be added before public launch.

## Run tests

Tests use isolated temporary SQLite databases for speed; the actual site uses the configured MariaDB database. No UC3M database credentials are necessary for the test suite.

Install pytest (not required to launch the site):

```bash
python -m pip install pytest
python -m pytest -q
```

The test suite covers public browsing, registration/password hashes, login, role restrictions, booking totals, packages, available-seat limits, private receipts, staff editors, price updates, CSRF rejection and XSS escaping.

## Design decisions

- **Seat selection:** Only quantity, not individual numbered seats. This is explicitly allowed by the brief.
- **Payment:** At the cinema, not online, as permitted by the brief.
- **Multiple screens:** Fixed capacity per screen and one screening at a time per room, with a 15-minute turnover.
- **Historical prices:** `Booking.ticket_unit_price`, `Booking.total_price` and booking-food snapshots avoid changing prior receipts when menu prices are edited.
- **Product removal:** Soft-delete (`is_active=False`) instead of database deletion, to preserve historic booking references. Removing a snack/drink also disables active packages containing it.
- **Showtime/movie editing:** Adding is supported; editing/removal is optional in the brief and intentionally not exposed, to avoid accidentally modifying existing bookings.

## Known limitations / possible extensions

- Admin account provisioning is CLI-only; customers cannot promote themselves.
- No seat map, checkout, refunds, cancellation, SMS, email or ratings because they aren't required.
- `datetime.now()` assumes the server is running in the cinema's local timezone. If hosting remotely across timezones, convert showtime times explicitly to a configured IANA timezone.
- The UC3M MariaDB server is reachable only from permitted lab machines. Remote/public hosting would require a different approved database host and production hardening.


## Editing an existing movie (new staff feature)

1. Sign in as a **management staff** user.
2. Open **Staff dashboard → Movies** and select **Edit** next to a movie, or visit its public details page and click **Edit this movie**.
3. Change the **title, genre, age rating**, or optionally choose a new **poster**. The preview updates immediately in your browser; no changes are saved at this stage.
4. Click **Save changes** to submit one protected POST request. Flask validates the fields and upload, then updates that **same movie** in the database.
5. **Reset draft** restores the form values to how they appeared when you opened the page. **Cancel** leaves the movie unchanged.

The new editor **does not change** the film synopsis, runtime, screens, showtimes, reservations, customers or ticket prices. Existing poster images are kept when no replacement is selected. This feature requires **no database migration**.

Client-side preview code: `static/js/movie_editor.js`  
Page: `templates/admin/movie_edit.html`  
Route: `routes/admin.py` → `movie_edit()`  
Styles: the `EDIT MOVIE` section at the end of `static/css/classic-cinema.css`

Run `python -m pytest -q` to run the included tests, including the movie editor tests.

