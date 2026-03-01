"""PPML/FHE Research Dashboard — Main Flask Application."""

import os
from datetime import date, datetime, timedelta
from functools import wraps

import bcrypt
from dotenv import load_dotenv
from flask import (Flask, render_template, request, redirect, url_for,
                   flash, jsonify, session, abort)

from models import db, User, Event, Researcher, Resource, Todo, DailyLog, PhDMilestone, AppSetting
from seed_data import seed_all

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dashboard.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=30)

db.init_app(app)


# ============================================================
# AUTH
# ============================================================

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


@app.route("/login", methods=["GET", "POST"])
def login():
    if "user_id" in session:
        return redirect(url_for("dashboard"))
    if request.method == "POST":
        password = request.form.get("password", "")
        user = User.query.first()
        if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            session.permanent = True
            session["user_id"] = user.id
            return redirect(url_for("dashboard"))
        flash("Invalid password.", "error")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ============================================================
# DASHBOARD
# ============================================================

@app.route("/")
@login_required
def dashboard():
    today = date.today()

    # Upcoming deadlines (next 60 days)
    upcoming_deadlines = Event.query.filter(
        Event.submission_deadline != None,
        Event.submission_deadline >= today,
        Event.submission_deadline <= today + timedelta(days=60)
    ).order_by(Event.submission_deadline).limit(15).all()

    # Pinned events
    pinned = Event.query.filter_by(pinned=True).all()

    # Today's todos
    pending_todos = Todo.query.filter(
        Todo.status.in_(["pending", "in_progress"])
    ).order_by(
        Todo.priority.desc(), Todo.due_date.asc().nullslast()
    ).limit(10).all()

    # Today's log
    today_log = DailyLog.query.filter_by(log_date=today).first()

    # PhD milestones (upcoming)
    milestones = PhDMilestone.query.filter(
        PhDMilestone.status.in_(["pending", "in_progress"])
    ).order_by(PhDMilestone.target_date.asc().nullslast()).limit(5).all()

    # Stats
    total_events = Event.query.count()
    total_conferences = Event.query.filter_by(category="conference").count()
    total_journals = Event.query.filter_by(category="journal").count()
    total_workshops = Event.query.filter_by(category="workshop").count()
    overdue_todos = Todo.query.filter(
        Todo.due_date < today, Todo.status != "completed"
    ).count()

    # CFP open events
    cfp_open = Event.query.filter_by(status="cfp_open").all()

    # Pre-serialize for JS charts
    deadlines_json = [e.to_dict() for e in upcoming_deadlines]

    return render_template("dashboard.html",
                           upcoming_deadlines=upcoming_deadlines,
                           deadlines_json=deadlines_json,
                           pinned=pinned,
                           pending_todos=pending_todos,
                           today_log=today_log,
                           milestones=milestones,
                           total_events=total_events,
                           total_conferences=total_conferences,
                           total_journals=total_journals,
                           total_workshops=total_workshops,
                           overdue_todos=overdue_todos,
                           cfp_open=cfp_open,
                           today=today)


# ============================================================
# EVENTS
# ============================================================

@app.route("/events")
@login_required
def events():
    category = request.args.get("category", "")
    location = request.args.get("location", "")
    status = request.args.get("status", "")
    search = request.args.get("q", "")
    sort_by = request.args.get("sort", "deadline")

    query = Event.query

    if category:
        query = query.filter_by(category=category)
    if location:
        query = query.filter_by(location=location)
    if status:
        query = query.filter_by(status=status)
    if search:
        query = query.filter(
            (Event.title.ilike(f"%{search}%")) |
            (Event.relevance_tags.ilike(f"%{search}%")) |
            (Event.description.ilike(f"%{search}%"))
        )

    if sort_by == "deadline":
        query = query.order_by(Event.submission_deadline.asc().nullslast())
    elif sort_by == "name":
        query = query.order_by(Event.title.asc())
    elif sort_by == "date_added":
        query = query.order_by(Event.created_at.desc())
    else:
        query = query.order_by(Event.submission_deadline.asc().nullslast())

    all_events = query.all()

    categories = db.session.query(Event.category).distinct().all()
    categories = sorted([c[0] for c in categories if c[0]])

    return render_template("events.html", events=all_events,
                           categories=categories,
                           current_category=category,
                           current_location=location,
                           current_status=status,
                           current_search=search,
                           current_sort=sort_by)


@app.route("/events/new", methods=["GET", "POST"])
@login_required
def event_new():
    if request.method == "POST":
        event = _event_from_form(Event())
        db.session.add(event)
        db.session.commit()
        flash("Event created.", "success")
        return redirect(url_for("events"))
    return render_template("event_form.html", event=None)


@app.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def event_edit(event_id):
    event = Event.query.get_or_404(event_id)
    if request.method == "POST":
        _event_from_form(event)
        db.session.commit()
        flash("Event updated.", "success")
        return redirect(url_for("events"))
    return render_template("event_form.html", event=event)


@app.route("/events/<int:event_id>/delete", methods=["POST"])
@login_required
def event_delete(event_id):
    event = Event.query.get_or_404(event_id)
    db.session.delete(event)
    db.session.commit()
    flash("Event deleted.", "success")
    return redirect(url_for("events"))


@app.route("/events/<int:event_id>/pin", methods=["POST"])
@login_required
def event_pin(event_id):
    event = Event.query.get_or_404(event_id)
    event.pinned = not event.pinned
    db.session.commit()
    return jsonify({"pinned": event.pinned})


def _event_from_form(event):
    event.title = request.form.get("title", "").strip()
    event.category = request.form.get("category", "conference")
    event.edition = request.form.get("edition", "").strip() or None
    event.website = request.form.get("website", "").strip() or None
    event.association = request.form.get("association", "").strip() or None
    event.relevance_tags = request.form.get("relevance_tags", "").strip() or None
    event.location = request.form.get("location", "").strip() or None
    event.city = request.form.get("city", "").strip() or None
    event.description = request.form.get("description", "").strip() or None
    event.notes = request.form.get("notes", "").strip() or None
    event.status = request.form.get("status", "upcoming")

    for date_field in ["submission_deadline", "notification_date", "camera_ready_date",
                       "event_start_date", "event_end_date"]:
        val = request.form.get(date_field, "").strip()
        setattr(event, date_field, date.fromisoformat(val) if val else None)

    event.updated_at = datetime.utcnow()
    return event


# ============================================================
# RESEARCHERS
# ============================================================

@app.route("/researchers")
@login_required
def researchers():
    search = request.args.get("q", "")
    query = Researcher.query
    if search:
        query = query.filter(
            (Researcher.name.ilike(f"%{search}%")) |
            (Researcher.affiliation.ilike(f"%{search}%")) |
            (Researcher.research_areas.ilike(f"%{search}%"))
        )
    all_researchers = query.order_by(Researcher.name).all()
    return render_template("researchers.html", researchers=all_researchers, current_search=search)


@app.route("/researchers/new", methods=["GET", "POST"])
@login_required
def researcher_new():
    if request.method == "POST":
        r = Researcher(
            name=request.form["name"].strip(),
            website=request.form.get("website", "").strip() or None,
            affiliation=request.form.get("affiliation", "").strip() or None,
            research_areas=request.form.get("research_areas", "").strip() or None,
            notes=request.form.get("notes", "").strip() or None,
        )
        db.session.add(r)
        db.session.commit()
        flash("Researcher added.", "success")
        return redirect(url_for("researchers"))
    return render_template("researcher_form.html", researcher=None)


@app.route("/researchers/<int:rid>/edit", methods=["GET", "POST"])
@login_required
def researcher_edit(rid):
    r = Researcher.query.get_or_404(rid)
    if request.method == "POST":
        r.name = request.form["name"].strip()
        r.website = request.form.get("website", "").strip() or None
        r.affiliation = request.form.get("affiliation", "").strip() or None
        r.research_areas = request.form.get("research_areas", "").strip() or None
        r.notes = request.form.get("notes", "").strip() or None
        db.session.commit()
        flash("Researcher updated.", "success")
        return redirect(url_for("researchers"))
    return render_template("researcher_form.html", researcher=r)


@app.route("/researchers/<int:rid>/delete", methods=["POST"])
@login_required
def researcher_delete(rid):
    r = Researcher.query.get_or_404(rid)
    db.session.delete(r)
    db.session.commit()
    flash("Researcher deleted.", "success")
    return redirect(url_for("researchers"))


# ============================================================
# RESOURCES
# ============================================================

@app.route("/resources")
@login_required
def resources():
    rtype = request.args.get("type", "")
    search = request.args.get("q", "")
    query = Resource.query
    if rtype:
        query = query.filter_by(resource_type=rtype)
    if search:
        query = query.filter(
            (Resource.name.ilike(f"%{search}%")) |
            (Resource.description.ilike(f"%{search}%")) |
            (Resource.tags.ilike(f"%{search}%"))
        )
    all_resources = query.order_by(Resource.resource_type, Resource.name).all()
    types = db.session.query(Resource.resource_type).distinct().all()
    types = sorted([t[0] for t in types if t[0]])
    return render_template("resources.html", resources=all_resources,
                           types=types, current_type=rtype, current_search=search)


@app.route("/resources/new", methods=["GET", "POST"])
@login_required
def resource_new():
    if request.method == "POST":
        r = Resource(
            name=request.form["name"].strip(),
            resource_type=request.form["resource_type"],
            website=request.form.get("website", "").strip() or None,
            description=request.form.get("description", "").strip() or None,
            tags=request.form.get("tags", "").strip() or None,
        )
        db.session.add(r)
        db.session.commit()
        flash("Resource added.", "success")
        return redirect(url_for("resources"))
    return render_template("resource_form.html", resource=None)


@app.route("/resources/<int:rid>/edit", methods=["GET", "POST"])
@login_required
def resource_edit(rid):
    r = Resource.query.get_or_404(rid)
    if request.method == "POST":
        r.name = request.form["name"].strip()
        r.resource_type = request.form["resource_type"]
        r.website = request.form.get("website", "").strip() or None
        r.description = request.form.get("description", "").strip() or None
        r.tags = request.form.get("tags", "").strip() or None
        db.session.commit()
        flash("Resource updated.", "success")
        return redirect(url_for("resources"))
    return render_template("resource_form.html", resource=r)


@app.route("/resources/<int:rid>/delete", methods=["POST"])
@login_required
def resource_delete(rid):
    r = Resource.query.get_or_404(rid)
    db.session.delete(r)
    db.session.commit()
    flash("Resource deleted.", "success")
    return redirect(url_for("resources"))


# ============================================================
# TODOS
# ============================================================

@app.route("/todos")
@login_required
def todos():
    status_filter = request.args.get("status", "")
    query = Todo.query
    if status_filter:
        query = query.filter_by(status=status_filter)
    all_todos = query.order_by(
        Todo.status.asc(), Todo.priority.desc(), Todo.due_date.asc().nullslast()
    ).all()
    return render_template("todos.html", todos=all_todos, current_status=status_filter)


@app.route("/todos/new", methods=["POST"])
@login_required
def todo_new():
    t = Todo(
        title=request.form["title"].strip(),
        description=request.form.get("description", "").strip() or None,
        priority=request.form.get("priority", "medium"),
        category=request.form.get("category", "").strip() or None,
    )
    due = request.form.get("due_date", "").strip()
    if due:
        t.due_date = date.fromisoformat(due)
    db.session.add(t)
    db.session.commit()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(t.to_dict())
    return redirect(url_for("todos"))


@app.route("/todos/<int:tid>/update", methods=["POST"])
@login_required
def todo_update(tid):
    t = Todo.query.get_or_404(tid)
    if "status" in request.form:
        t.status = request.form["status"]
    if "title" in request.form:
        t.title = request.form["title"].strip()
    if "priority" in request.form:
        t.priority = request.form["priority"]
    if "due_date" in request.form:
        due = request.form["due_date"].strip()
        t.due_date = date.fromisoformat(due) if due else None
    if "description" in request.form:
        t.description = request.form.get("description", "").strip() or None
    if "category" in request.form:
        t.category = request.form.get("category", "").strip() or None
    t.updated_at = datetime.utcnow()
    db.session.commit()
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify(t.to_dict())
    return redirect(url_for("todos"))


@app.route("/todos/<int:tid>/delete", methods=["POST"])
@login_required
def todo_delete(tid):
    t = Todo.query.get_or_404(tid)
    db.session.delete(t)
    db.session.commit()
    return redirect(url_for("todos"))


# ============================================================
# DAILY LOG
# ============================================================

@app.route("/daily-log")
@login_required
def daily_log():
    logs = DailyLog.query.order_by(DailyLog.log_date.desc()).limit(30).all()
    today = date.today()
    today_log = DailyLog.query.filter_by(log_date=today).first()
    # Pre-serialize recent logs for JS chart
    logs_json = [l.to_dict() for l in logs[:7]]

    return render_template("daily_log.html", logs=logs, logs_json=logs_json,
                           today_log=today_log, today=today)


@app.route("/daily-log/save", methods=["POST"])
@login_required
def daily_log_save():
    log_date_str = request.form.get("log_date", date.today().isoformat())
    log_date_val = date.fromisoformat(log_date_str)
    log = DailyLog.query.filter_by(log_date=log_date_val).first()
    if not log:
        log = DailyLog(log_date=log_date_val)
        db.session.add(log)
    log.content = request.form.get("content", "").strip()
    log.hours_worked = float(request.form.get("hours_worked", 0) or 0)
    log.mood = request.form.get("mood", "").strip() or None
    log.tags = request.form.get("tags", "").strip() or None
    log.updated_at = datetime.utcnow()
    db.session.commit()
    flash("Daily log saved.", "success")
    return redirect(url_for("daily_log"))


# ============================================================
# PHD TIMELINE
# ============================================================

@app.route("/timeline")
@login_required
def timeline():
    milestones = PhDMilestone.query.order_by(PhDMilestone.sort_order, PhDMilestone.target_date.asc().nullslast()).all()
    return render_template("timeline.html", milestones=milestones)


@app.route("/timeline/new", methods=["POST"])
@login_required
def milestone_new():
    m = PhDMilestone(
        title=request.form["title"].strip(),
        description=request.form.get("description", "").strip() or None,
        category=request.form.get("category", "").strip() or None,
        status=request.form.get("status", "pending"),
    )
    td = request.form.get("target_date", "").strip()
    if td:
        m.target_date = date.fromisoformat(td)
    max_order = db.session.query(db.func.max(PhDMilestone.sort_order)).scalar() or 0
    m.sort_order = max_order + 1
    db.session.add(m)
    db.session.commit()
    flash("Milestone added.", "success")
    return redirect(url_for("timeline"))


@app.route("/timeline/<int:mid>/update", methods=["POST"])
@login_required
def milestone_update(mid):
    m = PhDMilestone.query.get_or_404(mid)
    if "title" in request.form:
        m.title = request.form["title"].strip()
    if "description" in request.form:
        m.description = request.form.get("description", "").strip() or None
    if "status" in request.form:
        m.status = request.form["status"]
        if m.status == "completed" and not m.completed_date:
            m.completed_date = date.today()
    if "target_date" in request.form:
        td = request.form["target_date"].strip()
        m.target_date = date.fromisoformat(td) if td else None
    if "category" in request.form:
        m.category = request.form.get("category", "").strip() or None
    db.session.commit()
    flash("Milestone updated.", "success")
    return redirect(url_for("timeline"))


@app.route("/timeline/<int:mid>/delete", methods=["POST"])
@login_required
def milestone_delete(mid):
    m = PhDMilestone.query.get_or_404(mid)
    db.session.delete(m)
    db.session.commit()
    flash("Milestone deleted.", "success")
    return redirect(url_for("timeline"))


# ============================================================
# SETTINGS
# ============================================================

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    if request.method == "POST":
        action = request.form.get("action", "")

        if action == "change_password":
            new_pw = request.form.get("new_password", "")
            if len(new_pw) >= 4:
                user = User.query.get(session["user_id"])
                user.password_hash = bcrypt.hashpw(new_pw.encode(), bcrypt.gensalt()).decode()
                db.session.commit()
                flash("Password changed.", "success")
            else:
                flash("Password must be at least 4 characters.", "error")

        elif action == "save_integrations":
            for key in ["notion_api_key", "notion_events_db_id", "notion_todos_db_id",
                        "obsidian_vault_path", "discord_webhook_url",
                        "smtp_server", "smtp_port", "smtp_username", "smtp_password", "email_to",
                        "reminder_days_before", "daily_digest_hour"]:
                val = request.form.get(key, "").strip()
                AppSetting.set(key, val)
            flash("Integration settings saved.", "success")

        elif action == "export_obsidian":
            vault_path = AppSetting.get("obsidian_vault_path", "")
            if vault_path and os.path.isdir(vault_path):
                from integrations import ObsidianExport
                exporter = ObsidianExport(vault_path)
                exporter.export_all(
                    Event.query.all(),
                    Researcher.query.all(),
                    DailyLog.query.all()
                )
                flash("Exported to Obsidian vault.", "success")
            else:
                flash("Invalid Obsidian vault path.", "error")

        elif action == "sync_notion":
            api_key = AppSetting.get("notion_api_key", "")
            events_db = AppSetting.get("notion_events_db_id", "")
            if api_key and events_db:
                from integrations import NotionSync
                ns = NotionSync(api_key, events_db, AppSetting.get("notion_todos_db_id", ""))
                count = 0
                for event in Event.query.all():
                    try:
                        ns.sync_event(event)
                        count += 1
                    except Exception as e:
                        app.logger.error(f"Notion sync failed for {event.title}: {e}")
                flash(f"Synced {count} events to Notion.", "success")
            else:
                flash("Notion API key and Events DB ID required.", "error")

        elif action == "test_discord":
            webhook = AppSetting.get("discord_webhook_url", "")
            if webhook:
                from integrations import DiscordNotifier
                try:
                    dn = DiscordNotifier(webhook)
                    dn.send_message("Test message from PPML/FHE Dashboard!")
                    flash("Discord test message sent.", "success")
                except Exception as e:
                    flash(f"Discord test failed: {e}", "error")
            else:
                flash("Discord webhook URL not configured.", "error")

        return redirect(url_for("settings"))

    # Load current settings
    setting_keys = ["notion_api_key", "notion_events_db_id", "notion_todos_db_id",
                    "obsidian_vault_path", "discord_webhook_url",
                    "smtp_server", "smtp_port", "smtp_username", "smtp_password", "email_to",
                    "reminder_days_before", "daily_digest_hour"]
    current_settings = {k: AppSetting.get(k, "") for k in setting_keys}

    return render_template("settings.html", settings=current_settings)


# ============================================================
# API ENDPOINTS (for AJAX)
# ============================================================

@app.route("/api/events")
@login_required
def api_events():
    events = Event.query.order_by(Event.submission_deadline.asc().nullslast()).all()
    return jsonify([e.to_dict() for e in events])


@app.route("/api/deadlines")
@login_required
def api_deadlines():
    today = date.today()
    events = Event.query.filter(
        Event.submission_deadline != None,
        Event.submission_deadline >= today
    ).order_by(Event.submission_deadline).limit(30).all()
    return jsonify([e.to_dict() for e in events])


@app.route("/api/todos")
@login_required
def api_todos():
    todos = Todo.query.order_by(Todo.status, Todo.priority.desc()).all()
    return jsonify([t.to_dict() for t in todos])


# ============================================================
# INIT
# ============================================================

def create_app():
    with app.app_context():
        db.create_all()

        # Create default user if none exists
        if not User.query.first():
            default_pw = os.getenv("DASHBOARD_PASSWORD", "changeme")
            hashed = bcrypt.hashpw(default_pw.encode(), bcrypt.gensalt()).decode()
            db.session.add(User(username="admin", password_hash=hashed))
            db.session.commit()

        # Seed data
        seed_all()

        # Initialize scheduler
        from scheduler import init_scheduler
        init_scheduler(app)

    return app


if __name__ == "__main__":
    application = create_app()
    application.run(host="127.0.0.1", port=5000, debug=True)
