from flask import current_app, Blueprint, render_template, request
from flask_login import login_required

views = Blueprint('views', __name__)

@views.route('/')
def index():
    #if request.method == "GET":
    return render_template("index.html")