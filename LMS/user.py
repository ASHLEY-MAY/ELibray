from flask import Blueprint, render_template

user = Blueprint('user', __name__, template_folder='template/user')


@user.route('/about')
def about():
    return render_template('about.html')