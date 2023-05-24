from flask_app import app, bcrypt
from flask_app.controllers import usercontroller

if __name__ == '__main__':
    app.run(debug=True)