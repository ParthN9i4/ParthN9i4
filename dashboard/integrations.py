"""Integration modules for Notion, Obsidian, Discord, and Email."""

import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date, datetime
import requests


# ============================================================
# NOTION INTEGRATION
# ============================================================

class NotionSync:
    """Sync events and todos to a Notion database."""

    def __init__(self, api_key, events_db_id=None, todos_db_id=None):
        self.api_key = api_key
        self.events_db_id = events_db_id
        self.todos_db_id = todos_db_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        self.base_url = "https://api.notion.com/v1"

    def _post(self, endpoint, data):
        resp = requests.post(f"{self.base_url}/{endpoint}",
                             headers=self.headers, json=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def _patch(self, endpoint, data):
        resp = requests.patch(f"{self.base_url}/{endpoint}",
                              headers=self.headers, json=data, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def sync_event(self, event):
        """Create or update an event in Notion."""
        if not self.events_db_id:
            return None
        properties = {
            "Title": {"title": [{"text": {"content": event.title}}]},
            "Category": {"select": {"name": event.category}},
            "Status": {"select": {"name": event.status}},
            "Website": {"url": event.website} if event.website else {"url": None},
        }
        if event.relevance_tags:
            tags = [{"name": t.strip()} for t in event.relevance_tags.split(",")]
            properties["Tags"] = {"multi_select": tags}
        if event.location:
            properties["Location"] = {"select": {"name": event.location}}
        if event.submission_deadline:
            properties["Submission Deadline"] = {"date": {"start": event.submission_deadline.isoformat()}}
        if event.event_start_date:
            date_obj = {"start": event.event_start_date.isoformat()}
            if event.event_end_date:
                date_obj["end"] = event.event_end_date.isoformat()
            properties["Event Date"] = {"date": date_obj}

        return self._post("pages", {
            "parent": {"database_id": self.events_db_id},
            "properties": properties,
        })

    def sync_todo(self, todo):
        """Create or update a todo in Notion."""
        if not self.todos_db_id:
            return None
        properties = {
            "Title": {"title": [{"text": {"content": todo.title}}]},
            "Status": {"select": {"name": todo.status}},
            "Priority": {"select": {"name": todo.priority}},
        }
        if todo.due_date:
            properties["Due Date"] = {"date": {"start": todo.due_date.isoformat()}}
        if todo.category:
            properties["Category"] = {"select": {"name": todo.category}}

        return self._post("pages", {
            "parent": {"database_id": self.todos_db_id},
            "properties": properties,
        })

    def create_events_database(self, parent_page_id):
        """Create a new Notion database for events."""
        return self._post("databases", {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": "PPML/FHE Events"}}],
            "properties": {
                "Title": {"title": {}},
                "Category": {"select": {"options": [
                    {"name": "conference", "color": "blue"},
                    {"name": "journal", "color": "green"},
                    {"name": "workshop", "color": "purple"},
                    {"name": "seminar", "color": "yellow"},
                    {"name": "school", "color": "orange"},
                    {"name": "call_for_chapters", "color": "pink"},
                ]}},
                "Status": {"select": {"options": [
                    {"name": "upcoming", "color": "blue"},
                    {"name": "cfp_open", "color": "green"},
                    {"name": "cfp_closed", "color": "yellow"},
                    {"name": "ongoing", "color": "orange"},
                    {"name": "past", "color": "gray"},
                ]}},
                "Tags": {"multi_select": {}},
                "Location": {"select": {}},
                "Website": {"url": {}},
                "Submission Deadline": {"date": {}},
                "Event Date": {"date": {}},
            }
        })


# ============================================================
# OBSIDIAN INTEGRATION
# ============================================================

class ObsidianExport:
    """Export data as Obsidian-compatible markdown files."""

    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.base_dir = os.path.join(vault_path, "PPML-FHE-Dashboard")

    def _ensure_dir(self, path):
        os.makedirs(path, exist_ok=True)

    def _write_file(self, filepath, content):
        self._ensure_dir(os.path.dirname(filepath))
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

    def export_event(self, event):
        """Export a single event as an Obsidian note."""
        category_dir = os.path.join(self.base_dir, "Events", event.category.title() + "s")
        safe_title = "".join(c for c in event.title if c.isalnum() or c in (' ', '-', '_')).strip()
        filepath = os.path.join(category_dir, f"{safe_title}.md")

        frontmatter = [
            "---",
            f"title: \"{event.title}\"",
            f"category: {event.category}",
            f"status: {event.status}",
        ]
        if event.website:
            frontmatter.append(f"website: \"{event.website}\"")
        if event.submission_deadline:
            frontmatter.append(f"submission_deadline: {event.submission_deadline.isoformat()}")
        if event.event_start_date:
            frontmatter.append(f"event_start: {event.event_start_date.isoformat()}")
        if event.event_end_date:
            frontmatter.append(f"event_end: {event.event_end_date.isoformat()}")
        if event.relevance_tags:
            tags = [f"  - {t.strip()}" for t in event.relevance_tags.split(",")]
            frontmatter.append("tags:")
            frontmatter.extend(tags)
        if event.location:
            frontmatter.append(f"location: {event.location}")
        frontmatter.append("---")
        frontmatter.append("")

        body = [f"# {event.title}", ""]
        if event.website:
            body.append(f"**Website:** [{event.website}]({event.website})")
        if event.association:
            body.append(f"**Association:** {event.association}")
        if event.location:
            body.append(f"**Location:** {event.location}")
        body.append("")

        if any([event.submission_deadline, event.notification_date, event.event_start_date]):
            body.append("## Key Dates")
            if event.submission_deadline:
                body.append(f"- **Submission Deadline:** {event.submission_deadline.isoformat()}")
            if event.notification_date:
                body.append(f"- **Notification:** {event.notification_date.isoformat()}")
            if event.camera_ready_date:
                body.append(f"- **Camera Ready:** {event.camera_ready_date.isoformat()}")
            if event.event_start_date:
                end = f" to {event.event_end_date.isoformat()}" if event.event_end_date else ""
                body.append(f"- **Event Date:** {event.event_start_date.isoformat()}{end}")
            body.append("")

        if event.description:
            body.append("## Description")
            body.append(event.description)
            body.append("")

        if event.notes:
            body.append("## Notes")
            body.append(event.notes)
            body.append("")

        content = "\n".join(frontmatter) + "\n".join(body)
        self._write_file(filepath, content)

    def export_researcher(self, researcher):
        """Export a researcher profile as an Obsidian note."""
        filepath = os.path.join(self.base_dir, "Researchers",
                                f"{researcher.name.replace('/', '-')}.md")
        lines = [
            "---",
            f"name: \"{researcher.name}\"",
            f"affiliation: \"{researcher.affiliation or ''}\"",
        ]
        if researcher.research_areas:
            tags = [f"  - {t.strip()}" for t in researcher.research_areas.split(",")]
            lines.append("tags:")
            lines.extend(tags)
        lines.extend(["---", "", f"# {researcher.name}", ""])
        if researcher.affiliation:
            lines.append(f"**Affiliation:** {researcher.affiliation}")
        if researcher.website:
            lines.append(f"**Website:** [{researcher.website}]({researcher.website})")
        if researcher.research_areas:
            lines.append(f"**Research Areas:** {researcher.research_areas}")
        if researcher.notes:
            lines.extend(["", "## Notes", researcher.notes])
        self._write_file(filepath, "\n".join(lines))

    def export_daily_log(self, log):
        """Export a daily log as an Obsidian daily note."""
        filepath = os.path.join(self.base_dir, "Daily Notes",
                                f"{log.log_date.isoformat()}.md")
        lines = [
            "---",
            f"date: {log.log_date.isoformat()}",
            f"hours_worked: {log.hours_worked}",
        ]
        if log.mood:
            lines.append(f"mood: {log.mood}")
        if log.tags:
            tag_list = [f"  - {t.strip()}" for t in log.tags.split(",")]
            lines.append("tags:")
            lines.extend(tag_list)
        lines.extend(["---", "", f"# {log.log_date.isoformat()}", ""])
        if log.hours_worked:
            lines.append(f"**Hours worked:** {log.hours_worked}")
        if log.mood:
            lines.append(f"**Mood:** {log.mood}")
        lines.extend(["", log.content or ""])
        self._write_file(filepath, "\n".join(lines))

    def export_all(self, events, researchers, daily_logs):
        """Export all data to Obsidian vault."""
        for event in events:
            self.export_event(event)
        for researcher in researchers:
            self.export_researcher(researcher)
        for log in daily_logs:
            self.export_daily_log(log)

        # Create an index file
        index_lines = ["# PPML/FHE Research Dashboard", "",
                       "## Quick Links",
                       "- [[Events]]", "- [[Researchers]]", "- [[Daily Notes]]",
                       "", "## Event Categories"]
        categories = set(e.category for e in events)
        for cat in sorted(categories):
            index_lines.append(f"- [[Events/{cat.title()}s/]]")
        self._write_file(os.path.join(self.base_dir, "Index.md"), "\n".join(index_lines))


# ============================================================
# DISCORD INTEGRATION
# ============================================================

class DiscordNotifier:
    """Send notifications via Discord webhook."""

    def __init__(self, webhook_url):
        self.webhook_url = webhook_url

    def send_message(self, content, embeds=None):
        """Send a simple message or embed to Discord."""
        payload = {"content": content}
        if embeds:
            payload["embeds"] = embeds
        resp = requests.post(self.webhook_url, json=payload, timeout=30)
        resp.raise_for_status()

    def send_deadline_reminder(self, event):
        """Send a deadline reminder embed."""
        color = 0xFF0000 if event.days_until_deadline <= 3 else 0xFFAA00
        embed = {
            "title": f"Deadline Reminder: {event.title}",
            "color": color,
            "fields": [
                {"name": "Category", "value": event.category.title(), "inline": True},
                {"name": "Days Left", "value": str(event.days_until_deadline), "inline": True},
                {"name": "Deadline", "value": event.submission_deadline.isoformat(), "inline": True},
            ],
        }
        if event.website:
            embed["url"] = event.website
        if event.relevance_tags:
            embed["fields"].append({"name": "Tags", "value": event.relevance_tags, "inline": False})
        self.send_message("", embeds=[embed])

    def send_todo_reminder(self, todos):
        """Send a todo list reminder."""
        if not todos:
            return
        lines = []
        for t in todos:
            icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(t.priority, "⚪")
            due = f" (due: {t.due_date.isoformat()})" if t.due_date else ""
            lines.append(f"{icon} {t.title}{due}")
        embed = {
            "title": "Pending Tasks",
            "description": "\n".join(lines),
            "color": 0x5865F2,
        }
        self.send_message("", embeds=[embed])

    def send_daily_digest(self, upcoming_deadlines, pending_todos, log_summary=None):
        """Send a daily digest."""
        embeds = []
        if upcoming_deadlines:
            dl_lines = []
            for e in upcoming_deadlines[:10]:
                dl_lines.append(f"**{e.title}** — {e.days_until_deadline} days left ({e.submission_deadline.isoformat()})")
            embeds.append({
                "title": "Upcoming Deadlines",
                "description": "\n".join(dl_lines),
                "color": 0xFFAA00,
            })
        if pending_todos:
            todo_lines = [f"• {t.title}" for t in pending_todos[:10]]
            embeds.append({
                "title": f"Pending Todos ({len(pending_todos)})",
                "description": "\n".join(todo_lines),
                "color": 0x5865F2,
            })
        if embeds:
            self.send_message(f"**Daily Digest — {date.today().isoformat()}**", embeds=embeds)


# ============================================================
# EMAIL INTEGRATION
# ============================================================

class EmailNotifier:
    """Send notifications via email (SMTP)."""

    def __init__(self, smtp_server, smtp_port, username, password, to_email):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.to_email = to_email

    def _send(self, subject, html_body):
        msg = MIMEMultipart("alternative")
        msg["Subject"] = subject
        msg["From"] = self.username
        msg["To"] = self.to_email
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.username, self.password)
            server.sendmail(self.username, self.to_email, msg.as_string())

    def send_deadline_reminder(self, event):
        """Send a deadline reminder email."""
        color = "#dc2626" if event.days_until_deadline <= 3 else "#f59e0b"
        html = f"""
        <div style="font-family: sans-serif; max-width: 600px; margin: 0 auto;">
            <div style="background: {color}; color: white; padding: 16px; border-radius: 8px 8px 0 0;">
                <h2 style="margin:0;">Deadline Reminder</h2>
            </div>
            <div style="border: 1px solid #e5e7eb; padding: 16px; border-radius: 0 0 8px 8px;">
                <h3>{event.title}</h3>
                <p><strong>Deadline:</strong> {event.submission_deadline.isoformat()}</p>
                <p><strong>Days remaining:</strong> {event.days_until_deadline}</p>
                <p><strong>Category:</strong> {event.category.title()}</p>
                {"<p><a href='" + event.website + "'>Visit website</a></p>" if event.website else ""}
            </div>
        </div>
        """
        self._send(f"[PPML Dashboard] Deadline: {event.title} ({event.days_until_deadline} days left)", html)

    def send_daily_digest(self, upcoming_deadlines, pending_todos):
        """Send a daily digest email."""
        deadline_rows = ""
        for e in upcoming_deadlines[:15]:
            color = "#dc2626" if e.days_until_deadline <= 3 else ("#f59e0b" if e.days_until_deadline <= 7 else "#10b981")
            link = f"<a href='{e.website}'>{e.title}</a>" if e.website else e.title
            deadline_rows += f"<tr><td>{link}</td><td>{e.category}</td><td style='color:{color};font-weight:bold;'>{e.days_until_deadline} days</td><td>{e.submission_deadline.isoformat()}</td></tr>"

        todo_items = ""
        for t in pending_todos[:10]:
            icon = {"high": "🔴", "medium": "🟡", "low": "🟢"}.get(t.priority, "⚪")
            due = f" — due {t.due_date.isoformat()}" if t.due_date else ""
            todo_items += f"<li>{icon} {t.title}{due}</li>"

        html = f"""
        <div style="font-family: sans-serif; max-width: 700px; margin: 0 auto;">
            <div style="background: #4f46e5; color: white; padding: 16px; border-radius: 8px 8px 0 0;">
                <h2 style="margin:0;">PPML/FHE Dashboard — Daily Digest</h2>
                <p style="margin:4px 0 0 0; opacity:0.8;">{date.today().strftime('%A, %B %d, %Y')}</p>
            </div>
            <div style="border: 1px solid #e5e7eb; padding: 16px;">
                <h3>Upcoming Deadlines</h3>
                {"<table style='width:100%;border-collapse:collapse;'><tr style='background:#f3f4f6;'><th style='text-align:left;padding:8px;'>Event</th><th style='padding:8px;'>Type</th><th style='padding:8px;'>Remaining</th><th style='padding:8px;'>Date</th></tr>" + deadline_rows + "</table>" if deadline_rows else "<p>No upcoming deadlines.</p>"}
            </div>
            <div style="border: 1px solid #e5e7eb; padding: 16px; border-radius: 0 0 8px 8px;">
                <h3>Pending Tasks ({len(pending_todos)})</h3>
                {"<ul>" + todo_items + "</ul>" if todo_items else "<p>No pending tasks.</p>"}
            </div>
        </div>
        """
        self._send(f"[PPML Dashboard] Daily Digest — {date.today().isoformat()}", html)
