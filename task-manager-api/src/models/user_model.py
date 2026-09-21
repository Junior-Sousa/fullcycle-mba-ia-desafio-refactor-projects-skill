from src.database.connection import db
from datetime import datetime, timezone
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='user')
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'active': self.active,
            'created_at': str(self.created_at)
        }

    def set_password(self, pwd):
        self.password = generate_password_hash(pwd)

    def check_password(self, pwd):
        if len(self.password) == 32 and all(c in '0123456789abcdefABCDEF' for c in self.password):
            md5_hash = hashlib.md5(pwd.encode()).hexdigest()
            if self.password == md5_hash:
                # Upgrade hash to pbkdf2/scrypt on successful login
                self.set_password(pwd)
                db.session.commit()
                return True
        return check_password_hash(self.password, pwd)

    def is_admin(self):
        return self.role == 'admin'
