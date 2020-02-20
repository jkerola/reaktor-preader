import os
import pytest
import tempfile
from sqlalchemy.engine import Engine
from sqlalchemy import event
from preader.models import Package, File
from preader import db
from app import app
from io import BytesIO
from .dummy_data import RealDummy, FakeDummy


# Code example from the Programmable Web Project Course at
# https://lovelace.oulu.fi/ohjelmoitava-web/programmable-web-project-spring-2020/testing-flask-applications/
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@pytest.fixture
def db_handle():
    db_fd, db_fname = tempfile.mkstemp()
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + db_fname
    app.config["TESTING"] = True
    context = app.app_context()
    context.push()

    with context:
        db.create_all()
    yield db

    db.session.remove()
    os.close(db_fd)
    os.unlink(db_fname)
# End of example code


# Unit test class with test, setup methods
class TestApp(object):
    '''Class object that holds database and route tests'''
    def get_client(self):
        return app.test_client()

    def get_file(self, name='test.file', session_id='999999'):
        '''Creates a sample file object'''
        return File(name=name, session_id=session_id)

    def get_package(self, file_id, name='test-package', depends='test-package',
                    description='test-package description'):
        '''Creates a sample package object'''
        return Package(name=name, depends=depends, description=description, package_file=file_id)

    def test_create_instances(self, db_handle):
        '''Create instances of models for testing'''
        # Add file to database
        test_file = self.get_file()
        db_handle.session.add(test_file)
        db_handle.session.commit()
        # Test if file exist in database
        assert File.query.count() == 1
        # Add package to database
        test_package = self.get_package(file_id=test_file.id)
        db_handle.session.add(test_package)
        db_handle.session.commit()
        # Test if package exists in database
        assert Package.query.count() == 1

    def test_model_relationships(self, db_handle):
        '''Test model relationships functionality'''
        self.test_create_instances(db_handle)
        test_file = File.query.first()
        test_package = Package.query.first()
        # Test file/package relationships function
        assert test_package in test_file.packages
        assert test_package.package_file == test_file.id

    def test_multiple_relationships(self, db_handle):
        '''Test if multiple separate relationships function'''
        self.test_create_instances(db_handle)
        test_file = File.query.first()
        test_package = Package.query.first()
        # Extra file
        second_file = self.get_file(name='second_test.file', session_id='999998')
        db_handle.session.add(second_file)
        db_handle.session.commit()
        # Extra packages
        second_package = self.get_package(name='second-test-package', file_id=second_file.id)
        third_package = self.get_package(name='third-test-package', file_id=test_file.id)
        db_handle.session.add(second_package)
        db_handle.session.add(third_package)
        db.session.commit()
        # Fetch packages from db
        second_package = Package.query.filter_by(name='second-test-package').first()
        third_package = Package.query.filter_by(name='third-test-package').first()
        second_file = File.query.filter_by(name='second_test.file').first()
        # Test relationships
        assert test_package, third_package in test_file.packages
        assert second_package in second_file.packages

        assert second_file not in test_file.packages
        assert test_package, third_package not in second_file.packages

    def test_object_deletion(self, db_handle):
        '''Test object removal cascade functionality'''
        self.test_create_instances(db_handle)
        test_file = File.query.first()
        test_package = Package.query.first()
        db_handle.session.delete(test_package)
        db_handle.session.commit()
        # Test file exists, package does not
        assert Package.query.count() == 0
        assert File.query.count() == 1
        assert test_file.packages == []
        # Recreate package
        test_package = self.get_package(file_id=test_file.id)
        db_handle.session.add(test_package)
        db_handle.session.commit()
        test_package = Package.query.first()
        assert test_package in test_file.packages
        # Delete file
        db_handle.session.delete(test_file)
        db_handle.session.commit()
        # Check if both file and package are destroyed
        assert File.query.count() == 0
        assert Package.query.count() == 0

    # Route tests
    def test_route_index(self):
        '''Test index route'''
        client = self.get_client()
        response = client.get('/')
        assert response.status_code == 200

    def test_route_package(self, db_handle):
        '''Test package route'''
        self.test_create_instances(db_handle)
        client = self.get_client()
        with client.session_transaction() as session:
            session['_file_id'] = File.query.first().session_id
        response = client.get('/test-package')
        assert response.status_code == 200

    def test_file_upload(self, db_handle):
        '''Test uploading a file'''
        self.test_create_instances(db_handle)
        client = self.get_client()
        # Dummy data
        test_file = (BytesIO(RealDummy.data), RealDummy.name)
        data = {
            'file': test_file
        }
        response = client.post(
            '/',
            data=data,
            follow_redirects=True,
            content_type='multipart/form-data'
        )
        assert response.status_code == 200
        
        # test if package urls exist
        response = client.get('/test-package')
        assert response.status_code == 200

    def test_corrupt_file_upload(self, db_handle):
        '''Test uploading a file that is correct type, but no suitable data to read'''
        self.test_create_instances(db_handle)
        client = self.get_client()
        # Test false positive data upload
        corrupt_file = (BytesIO(FakeDummy.data), FakeDummy.name)
        data = {
            'file': corrupt_file
        }
        response = client.post(
            '/',
            data=data,
            follow_redirects=True,
            content_type='multipart/form-data'
        )
        # This will pass the file upload check
        assert response.status_code == 200
        # But should display the error message
        html = response.get_data()
        assert b'Could not load' in html
