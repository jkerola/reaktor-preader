from preader import db
from flask import Blueprint, render_template, request, redirect, session, url_for
from .forms import FileUploadForm
from .utils import read_file
from .models import File, Package
import secrets


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index(package_file=None):
    file_form = FileUploadForm()
    try:
        if session['_session_id']:
            current_file = File.query.\
                filter_by(session_id=session['_session_id']).\
                first()
            return render_template('index.html', session=session['_session_id'], current_file=current_file)
    except(KeyError):
        pass
    if request.method == 'POST':
        session_id = secrets.token_hex(16)
        session['_session_id'] = session_id
        print(session_id)
        package_file = file_form.file.data
        name, data = read_file(package_file)
        session_file = File(
            name=name,
            session_id=session_id
        )
        db.session.add(session_file)
        db.session.commit()

        current_file = File.query.filter_by(session_id=session_id).first()
        for dictionary in data:
            new_package = Package(**dictionary)
            new_package.package_file = current_file.id
            db.session.add(new_package)
        db.session.commit()
        return redirect(url_for('main.index'))
    else:
        return render_template('index.html', form=file_form)


@main.route('/<string:name>')
def package(name):
    package_file = File.query.\
        filter_by(session_id=session['_session_id']).\
        first()
    package = Package.query.\
        filter_by(package_file=package_file.id).\
        filter_by(name=name).first_or_404()
    dependencies = package.depends.split(',')
    packages_depending = Package.query.\
        filter(Package.depends.contains(name)).\
        all()
    print(packages_depending)
    return render_template(
        'package.html',
        package=package,
        dependencies=dependencies,
        packages_depending=packages_depending
        )
