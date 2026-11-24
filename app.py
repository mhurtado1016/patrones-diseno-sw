"""Patrón Factory Method (application factory) + inyección de dependencias."""
from flask import Flask
from flask_restful import Api

from endpoints.auth import AuthenticationResource
from endpoints.categories import CategoriesResource
from endpoints.favorites import FavoritesResource
from endpoints.products import ProductsResource
from auth.token_validator import StaticTokenValidator, TokenValidator
from repositories.factory import RepositoryFactory


def create_app(db_path: str = None, token_validator: TokenValidator = None) -> Flask:
    app = Flask(__name__)
    app.extensions["token_validator"] = token_validator or StaticTokenValidator()
    api = Api(app)
    repos = RepositoryFactory(db_path)

    api.add_resource(AuthenticationResource, "/auth")
    api.add_resource(ProductsResource, "/products", "/products/<int:product_id>",
                     resource_class_kwargs={"repository": repos.create("products"),
                                            "categories": repos.create("categories")})
    api.add_resource(CategoriesResource, "/categories", "/categories/<int:category_id>",
                     resource_class_kwargs={"repository": repos.create("categories")})
    api.add_resource(FavoritesResource, "/favorites",
                     resource_class_kwargs={"repository": repos.create("favorites"),
                                            "products": repos.create("products")})
    return app


if __name__ == "__main__":
    create_app().run(debug=True)
