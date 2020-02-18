from flask import Blueprint, render_template

error = Blueprint('error', __name__)


@error.app_errorhandler(404)
def error_404(error):
    '''404 File not found error handler'''
    return render_template('errors/404.html'), 404


@error.app_errorhandler(500)
def error_500(error):
    '''500 Internal logic error handler'''
    return render_template('errors/500.html'), 500
