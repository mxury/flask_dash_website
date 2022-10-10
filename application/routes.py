from flask import render_template
from flask import current_app as flask_app



@flask_app.route('/index', methods=['POST', 'GET'])
@flask_app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')


@flask_app.route('/publications', methods=['POST', 'GET'])
def publications():
    return render_template('publications.html')


@flask_app.route('/aboutme', methods=['POST', 'GET'])
def aboutme():
    return render_template('aboutme.html')


@flask_app.route('/personalprojects', methods=['POST', 'GET'])
def personalprojects():
    return render_template('personalprojects.html')