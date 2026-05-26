"""Background scheduler for deadline reminders and daily digests."""

import os
from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


scheduler = BackgroundScheduler()


def init_scheduler(app):
    """Initialize the background scheduler with reminder jobs."""

    digest_hour = int(os.getenv("DAILY_DIGEST_HOUR", "9"))
    reminder_days_str = os.getenv("REMINDER_DAYS_BEFORE", "7,3,1")
    reminder_days = [int(d.strip()) for d in reminder_days_str.split(",")]

    @scheduler.scheduled_job(CronTrigger(hour=digest_hour, minute=0))
    def daily_digest():
        with app.app_context():
            _send_daily_digest(app, reminder_days)

    @scheduler.scheduled_job(CronTrigger(hour=digest_hour, minute=30))
    def deadline_check():
        with app.app_context():
            _check_deadlines(app, reminder_days)

    scheduler.start()


def _get_notifiers():
    """Build notifier instances from environment config."""
    notifiers = []

    discord_url = os.getenv("DISCORD_WEBHOOK_URL")
    if discord_url:
        from integrations import DiscordNotifier
        notifiers.append(("discord", DiscordNotifier(discord_url)))

    smtp_server = os.getenv("SMTP_SERVER")
    smtp_user = os.getenv("SMTP_USERNAME")
    smtp_pass = os.getenv("SMTP_PASSWORD")
    email_to = os.getenv("EMAIL_TO")
    if all([smtp_server, smtp_user, smtp_pass, email_to]):
        from integrations import EmailNotifier
        notifiers.append(("email", EmailNotifier(
            smtp_server, int(os.getenv("SMTP_PORT", "587")),
            smtp_user, smtp_pass, email_to
        )))

    return notifiers


def _send_daily_digest(app, reminder_days):
    """Send daily digest via all configured channels."""
    from models import Event, Todo

    notifiers = _get_notifiers()
    if not notifiers:
        return

    today = date.today()
    max_days = max(reminder_days) + 7
    upcoming = Event.query.filter(
        Event.submission_deadline != None,
        Event.submission_deadline >= today,
        Event.submission_deadline <= today + timedelta(days=max_days)
    ).order_by(Event.submission_deadline).all()

    pending_todos = Todo.query.filter(
        Todo.status.in_(["pending", "in_progress"])
    ).order_by(Todo.due_date.asc().nullslast(), Todo.priority).all()

    for kind, notifier in notifiers:
        try:
            notifier.send_daily_digest(upcoming, pending_todos)
        except Exception as e:
            app.logger.error(f"Failed to send daily digest via {kind}: {e}")


def _check_deadlines(app, reminder_days):
    """Check for deadlines that match reminder thresholds and send alerts."""
    from models import Event

    notifiers = _get_notifiers()
    if not notifiers:
        return

    today = date.today()
    for days in reminder_days:
        target_date = today + timedelta(days=days)
        events = Event.query.filter(
            Event.submission_deadline == target_date
        ).all()

        for event in events:
            for kind, notifier in notifiers:
                try:
                    notifier.send_deadline_reminder(event)
                except Exception as e:
                    app.logger.error(f"Failed to send reminder for {event.title} via {kind}: {e}")
