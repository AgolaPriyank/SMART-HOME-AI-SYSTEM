from flask import Blueprint, render_template

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/')
def dashboard():
    return render_template('dashboard.html')
