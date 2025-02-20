import os
import binascii
from datetime import timedelta

from flask import Flask, jsonify
from dotenv import load_dotenv
from flask_restful import Resource, Api, reqparse
from flask_migrate import Migrate, migrate, upgrade, downgrade
from src.database.base import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, JWTManager
from src.parse_data.parse_rozetka import get_products
from src.database import db_action


load_dotenv()

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_URI")
app.config["JWT_SECRET_KEY"] = binascii.hexlify(os.urandom(24))
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
db.init_app(app)
api = Api(app)
migrate = Migrate(app, db)

with app.app_context():
#     db.drop_all()
    db.create_all()
#     get_products()


class ProductAPI(Resource):
    def get(self, prod_id: str|None = None):
        if prod_id:
            product = db_action.get_product(prod_id)
            response = jsonify(product)
            response.status_code = 200
            return response

        products = db_action.get_products()
        response = jsonify(products)
        response.status_code = 200
        return response

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("img_url")
        parser.add_argument("price")
        kwargs = parser.parse_args()
        prod_id = db_action.add_product(**kwargs)
        response = jsonify(f"Товар {prod_id} доданий")
        return response

    def put(self, prod_id: str):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("description")
        parser.add_argument("img_url")
        parser.add_argument("price")
        args = parser.parse_args()
        prod_id = db_action.update_product(
            prod_id=prod_id,
            name=args.get("name"),
            description=args.get("description"),
            img_url=args.get("img_url"),
            price=args.get("price")
        )

        return jsonify(f"Товар з id '{prod_id}' оновлено"), 200

    def delete(self, prod_id: str):
        db_action.del_product(prod_id)
        return jsonify("Товар успішно видалено"), 204

class ReviewAPI(Resource):
    pass


class UserAPI(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        user = db_action.get_user(user_id)
        куіз = куіз.json
        del user["password"]
        return куіз


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("password")
        parser.add_argument("email")
        kwargs = parser.parse_args()
        msg = db_action.add_user(**kwargs)
        resp = jsonify(msg)
        resp.status_code = 201
        return resp
    


class ToknAPI(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        token = dict(access_token = create_access_token(identity=user_id))
        resp = jsonify(token)
        resp.status_code = 200
        return resp
    




api.add_resource(ProductAPI, "/api/products", "/api/products/<prod_id>")
api.add_resource(UserAPI, "/api/users/")
api.add_resource(ToknAPI, "/api/tokens")

if __name__ == "__main__":
    app.run(debug=True, port=3000)
