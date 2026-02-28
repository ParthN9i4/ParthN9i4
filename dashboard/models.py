"""Database models for the PPML/FHE Research Dashboard."""

from datetime import datetime, date
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Event(db.Model):
    """Conferences, journals, workshops, seminars, schools, webinars, talks, call for chapters."""
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    category = db.Column(db.String(50), nullable=False)  # conference, journal, workshop, seminar, school, webinar, talk, call_for_chapters
    edition = db.Column(db.String(300))
    website = db.Column(db.String(500))
    association = db.Column(db.String(300))
    relevance_tags = db.Column(db.String(500))  # comma-separated tags
    location = db.Column(db.String(50))  # India, Outside, Online
    city = db.Column(db.String(200))

    # Key dates
    submission_deadline = db.Column(db.Date)
    notification_date = db.Column(db.Date)
    camera_ready_date = db.Column(db.Date)
    event_start_date = db.Column(db.Date)
    event_end_date = db.Column(db.Date)

    description = db.Column(db.Text)
    notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='upcoming')  # upcoming, cfp_open, cfp_closed, past, ongoing
    pinned = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def days_until_deadline(self):
        if self.submission_deadline:
            delta = self.submission_deadline - date.today()
            return delta.days
        return None

    @property
    def is_deadline_soon(self):
        d = self.days_until_deadline
        return d is not None and 0 <= d <= 14

    @property
    def is_deadline_passed(self):
        d = self.days_until_deadline
        return d is not None and d < 0

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'edition': self.edition,
            'website': self.website,
            'association': self.association,
            'relevance_tags': self.relevance_tags,
            'location': self.location,
            'city': self.city,
            'submission_deadline': self.submission_deadline.isoformat() if self.submission_deadline else None,
            'notification_date': self.notification_date.isoformat() if self.notification_date else None,
            'camera_ready_date': self.camera_ready_date.isoformat() if self.camera_ready_date else None,
            'event_start_date': self.event_start_date.isoformat() if self.event_start_date else None,
            'event_end_date': self.event_end_date.isoformat() if self.event_end_date else None,
            'description': self.description,
            'notes': self.notes,
            'status': self.status,
            'pinned': self.pinned,
            'days_until_deadline': self.days_until_deadline,
        }


class Researcher(db.Model):
    __tablename__ = 'researchers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    website = db.Column(db.String(500))
    affiliation = db.Column(db.String(300))
    research_areas = db.Column(db.String(500))
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'website': self.website,
            'affiliation': self.affiliation,
            'research_areas': self.research_areas,
            'notes': self.notes,
        }


class Resource(db.Model):
    """Libraries, companies, platforms, frameworks, code repos, organisations."""
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    resource_type = db.Column(db.String(50), nullable=False)  # library, company, platform, framework, code_repo, organisation
    website = db.Column(db.String(500))
    description = db.Column(db.Text)
    tags = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'resource_type': self.resource_type,
            'website': self.website,
            'description': self.description,
            'tags': self.tags,
        }


class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    priority = db.Column(db.String(10), default='medium')  # high, medium, low
    due_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    category = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def is_overdue(self):
        if self.due_date and self.status != 'completed':
            return self.due_date < date.today()
        return False

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'status': self.status,
            'category': self.category,
            'is_overdue': self.is_overdue,
        }


class DailyLog(db.Model):
    __tablename__ = 'daily_logs'
    id = db.Column(db.Integer, primary_key=True)
    log_date = db.Column(db.Date, nullable=False, unique=True)
    content = db.Column(db.Text)
    hours_worked = db.Column(db.Float, default=0)
    mood = db.Column(db.String(20))  # great, good, okay, bad
    tags = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'log_date': self.log_date.isoformat(),
            'content': self.content,
            'hours_worked': self.hours_worked,
            'mood': self.mood,
            'tags': self.tags,
        }


class PhDMilestone(db.Model):
    __tablename__ = 'phd_milestones'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text)
    target_date = db.Column(db.Date)
    completed_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed, delayed
    category = db.Column(db.String(100))  # coursework, research, publication, presentation, thesis, other
    sort_order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'completed_date': self.completed_date.isoformat() if self.completed_date else None,
            'status': self.status,
            'category': self.category,
            'sort_order': self.sort_order,
        }


class AppSetting(db.Model):
    __tablename__ = 'app_settings'
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)

    @staticmethod
    def get(key, default=None):
        setting = AppSetting.query.filter_by(key=key).first()
        return setting.value if setting else default

    @staticmethod
    def set(key, value):
        setting = AppSetting.query.filter_by(key=key).first()
        if setting:
            setting.value = value
        else:
            setting = AppSetting(key=key, value=value)
            db.session.add(setting)
        db.session.commit()
