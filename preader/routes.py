from preader import db
from flask import Blueprint, render_template, request, redirect, session, url_for
from .forms import FileUploadForm
from .utils import read_file
from .models import File, Package
import secrets


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index(package_file=None):
    '''App index, upload and analyze file. Displays package names as links.'''
    file_form = FileUploadForm()
    try:
        if session['_file_id']:
            current_file = File.query.\
                filter_by(session_id=session['_file_id']).\
                first()
            return render_template(
                'index.html',
                session=session['_file_id'],
                current_file=current_file,
                form=file_form
                )
    except(KeyError):
        pass
    if request.method == 'POST':
        session_id = secrets.token_hex(16)
        session['_file_id'] = session_id
        print(session_id)
        package_file = file_form.file.data
        name, data = read_file(package_file)
        if not data:
            name = f"Could not read file '{name}'. Please check file validity."
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
    '''Displays information about package, its dependecies and what packages depend on it.'''
    package_file = File.query.\
        filter_by(session_id=session['_file_id']).\
        first()
    package_names = [package.name for package in package_file.packages]
    package = Package.query.\
        filter_by(package_file=package_file.id).\
        filter_by(name=name).first_or_404()
    dependencies = package.depends.split(',')
    alternatives_list = []
    for package in dependencies:
        if '|' in package:
            alternatives = []
            alternatives = package.split('|')
            alternatives_list.append(alternatives)
            dependencies.remove(package)
    print(alternatives_list)
    packages_depending = Package.query.\
        filter(Package.depends.contains(name)).\
        all()
    return render_template(
        'package.html',
        package=package,
        dependencies=dependencies,
        alternatives_list=alternatives_list,
        packages_depending=packages_depending,
        package_names=package_names
        )
