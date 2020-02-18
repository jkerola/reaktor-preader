from preader import db


class File(db.Model):
    '''Model for the uploaded file with session information'''
    # Attributes
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    session_id = db.Column(db.String, nullable=False, unique=True)
    # Relationships
    packages = db.relationship(
        'Package', backref='file', cascade='all, delete-orphan', lazy=True
        )


class Package(db.Model):
    '''Model for individual packages listed in file'''
    # Attributes
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(), nullable=False)
    depends = db.Column(db.String(), nullable=False, default='None')
    description = db.Column(db.String, nullable=False)
    # Relationships
    package_file = db.Column(
        db.Integer, db.ForeignKey('file.id'), nullable=False
        )
