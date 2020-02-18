from preader import db
from flask import Blueprint, render_template, request, redirect, session
from .forms import FileUploadForm
from .utils import read_file
from .models import File, Package
import secrets


main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def index(package_file=None):
    '''App index, upload and analyze file. Displays package names as links.'''
    file_form = FileUploadForm()
    # Checks wether a file has been uploaded this session
    try:
        if session['_file_id']:
            current_file = File.query.\
                filter_by(session_id=session['_file_id']).first()

            return render_template(
                'index.html',
                session=session['_file_id'],
                current_file=current_file,
                form=file_form
                )
    except(KeyError):
        pass
    if request.method == 'POST':
        # Files are too large for a cookie (>4k bytes),
        # so the data is stored in a serverside database
        session_id = secrets.token_hex(16)
        session['_file_id'] = session_id
        print(session_id)
        package_file = file_form.file.data
        name, data = read_file(package_file)
        if not data:  # If the file does not contain required info
            name = f"Could not read file '{name}'. Please check file validity."
        session_file = File(
            name=name,
            session_id=session_id
        )
        db.session.add(session_file)
        db.session.commit()

        # Fetch the newly created file for current session
        # and create the package tables from the data
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
    '''Displays information about package, its dependecies and
    what packages depend on it.'''
    package_file = File.query.\
        filter_by(session_id=session['_file_id']).\
        first()
    # Fetch the currently viewed package or 404
    package = Package.query.\
        filter_by(package_file=package_file.id).\
        filter_by(name=name).first_or_404()

    # Depending package name formatting
    dependencies = package.depends.split(',')
    alternatives_list = []
    for dependency in dependencies:
        if '|' in dependency:  # Check for alternative packages
            alternatives = dependency.split('|')
            alternatives_list.append(alternatives)
            dependencies.remove(dependency)

    # Fetch packages that depend ON the currently viewed package
    packages_depending = Package.query.\
        filter(Package.depends.contains(name)).\
        all()
    # Filter out duplicate packages that result from different versions
    # ex. libxxx(0.3), libxx(0.3.1) etc
    filtered_depending_packages = []
    duplicate_package_names = []
    for dependency in packages_depending:
        if dependency.name not in duplicate_package_names:
            duplicate_package_names.append(dependency.name)
            filtered_depending_packages.append(dependency)
    # Fetch all names to check wether package definition exists in file
    package_names = [package.name for package in package_file.packages]
    return render_template(
        'package.html',
        package=package,
        dependencies=dependencies,
        alternatives_list=alternatives_list,
        packages_depending=filtered_depending_packages,
        package_names=package_names
        )
