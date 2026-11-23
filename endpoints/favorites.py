from flask_restful import Resource, reqparse
import json
from flask import request
from utils.database_connection import DatabaseConnection
from auth.decorators import require_auth


class FavoritesResource(Resource):
    def __init__(self):
        self.db = DatabaseConnection('favorites.json')
        self.db.connect()

        self.favorites = self.db.get_favorites()

    @require_auth
    def get(self):
        


        return self.db.get_favorites(), 200

    @require_auth
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')



        args = parser.parse_args()
        new_favorite = {
            'user_id': args['user_id'],
            'product_id': args['product_id']
        }

        self.favorites.append(new_favorite)
        self.db.add_favorite(new_favorite)
        return {'message': 'Product added to favorites', 'favorite': new_favorite}, 201

    @require_auth
    def delete(self):


        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help='User ID')
        parser.add_argument('product_id', type=int, required=True, help='Product ID')

        args = parser.parse_args()
        user_id = args['user_id']
        product_id = args['product_id']

        # Encuentra y elimina el producto de favoritos
        self.favorites = [favorite for favorite in self.favorites
                          if not (favorite['user_id'] == user_id and favorite['product_id'] == product_id)]
        self.db.save_favorites(self.favorites)

        return {'message': 'Product removed from favorites'}, 200
