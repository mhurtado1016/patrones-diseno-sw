from flask_restful import Resource, reqparse

from auth.decorators import require_auth


def _name_parser():
    parser = reqparse.RequestParser()
    parser.add_argument("name", type=str, required=True, help="Name of the category")
    return parser


class CategoriesResource(Resource):
    def __init__(self, repository):
        self.repo = repository

    @require_auth
    def get(self, category_id=None):
        if category_id is None:
            return self.repo.all()
        category = self.repo.find_by_id(category_id)
        return category if category else ({"message": "Category not found"}, 404)

    @require_auth
    def post(self):
        name = _name_parser().parse_args()["name"]
        if not name:
            return {"message": "Category name is required"}, 400
        if self.repo.find_by_name(name):
            return {"message": "Category already exists"}, 400
        self.repo.add({"name": name})
        return {"message": "Category added successfully"}, 201

    @require_auth
    def delete(self):
        name = _name_parser().parse_args()["name"]
        if not name:
            return {"message": "Category name is required"}, 400
        if not self.repo.remove_by_name(name):
            return {"message": "Category not found"}, 404
        return {"message": "Category removed successfully"}, 200
