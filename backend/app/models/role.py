from app.core.extensions import db

class Role(db.Model):
    """
    Role model for RBAC.
    Roles: USER, ADMIN, SUPER_ADMIN
    """
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True, nullable=False)

    users = db.relationship("User", backref="role", lazy=True)

    def __repr__(self):
        return f"<Role {self.name}>"
