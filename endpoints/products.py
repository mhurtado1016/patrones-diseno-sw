from flask import request
from flask_restful import Resource, reqparse

from auth.decorators import require_auth


class ProductsResource(Resource):
    def __init__(self, repository, categories):
        self.repo = repository
        self.categories = categories

    @require_auth
    def get(self, product_id=None):
        category = request.args.get("category")
        if category:
            return self.repo.find_by_category(category)
        if product_id is not None:
            product = self.repo.find_by_id(product_id)
            return product if product else ({"message": "Product not found"}, 404)
        return self.repo.all()

    @require_auth
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("name", type=str, required=True, help="Name of the product")
        parser.add_argument("category", type=str, required=True, help="Category of the product")
        parser.add_argument("price", type=float, required=True, help="Price of the product")
        args = parser.parse_args()
        if args["price"] <= 0:
            return {"message": "Price must be greater than 0"}, 400
        if not self.categories.exists(args["category"]):
            return {"message": "Category does not exist"}, 400
        product = self.repo.add(args)
        return {"message": "Product added", "product": product}, 201
