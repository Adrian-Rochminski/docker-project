import pymongo
from flask import Flask

appflask = Flask(__name__)
appflask.config["SECRET_KEY"] = "key"
client_users = pymongo.MongoClient("database_users", 27017,username='root', password='example')
client_data = pymongo.MongoClient("database_data", 27017,username='root', password='example')
users = client_users['users']
mongo = users['users_data']
db_data = client_data['data']
users_data = db_data['users_data']
try:
    client_users.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
try:
    client_data.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


def create_app():
    from .app.views import views
    appflask.register_blueprint(views, url_prefix='/')
    return appflask
