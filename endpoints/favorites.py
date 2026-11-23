from flask_restful import Resource, reqparse

from auth.decorators import require_auth


def _favorite_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("user_id", type=int, required=True, help="User ID")
    parser.add_argument("product_id", type=int, required=True, help="Product ID")
    return parser


class FavoritesResource(Resource):
    def __init__(self, repository):
        self.repo = repository

    @require_auth
    def get(self):
        return self.repo.all(), 200

    @require_auth
    def post(self):
        args = _favorite_parser().parse_args()
        favorite = self.repo.add({"user_id": args["user_id"], "product_id": args["product_id"]})
        return {"message": "Product added to favorites", "favorite": favorite}, 201

    @require_auth
    def delete(self):
        args = _favorite_parser().parse_args()
        self.repo.remove(args["user_id"], args["product_id"])
        return {"message": "Product removed from favorites"}, 200
