from collections import namedtuple

from flask import Flask
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, ForeignKey

Quote = namedtuple("Quote", ("text", "author"))

quotes = [
    Quote("Talk is cheap. Show me the code.", "Linus Torvalds"),
    Quote("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    Quote("Always code as if the guy who ends up maintaining your code will be a violent psychopath who knows where you live",
          "John Woods"),
    Quote("Give a man a program, frustrate him for a day. Teach a man to program, frustrate him for a lifetime.", "Muhammad Waseem"),
    Quote("Progress is possible only if we train ourselves to think about programs without thinking of them as pieces of executable code. ",
          "Edsger W. Dijkstra")
]

app = Flask(__name__)
api = Api(app, version='1.0', title='mmmp', description='mmmp')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://admin:12345678@mmmp.coqfv9yqcn7m.us-east-1.rds.amazonaws.com:3306/mmmp'
db = SQLAlchemy(app)

recipe_image = api.model('recipe-image', {
    'id': fields.Integer,
    'recipe_id': fields.Integer,
    'url': fields.String
})

recipe_ingredient_coupon = api.model('recipe-ingredient-coupon', {
    'id': fields.Integer,
    'recipe_ingredient_id': fields.Integer,
    'image_url': fields.String,
    'savings_amount': fields.Float,
    'short_description': fields.String
})

recipe_ingredient = api.model('recipe-ingredient', {
    'id': fields.Integer,
    'recipe_id': fields.Integer,
    'description': fields.String,
    'coupons': fields.Nested(recipe_ingredient_coupon)
})

recipe = api.model('recipe', {
    'id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'instructions': fields.String,
    'recipe_1': fields.String,
    'recipe_2': fields.String,
    'images': fields.Nested(recipe_image),
    'ingredients': fields.Nested(recipe_ingredient)
})

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.String())
    instructions = db.Column(db.String())
    recipe_1 = db.Column(db.String())
    recipe_2 = db.Column(db.String())

class RecipeImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(Integer, ForeignKey('recipe.id'))
    url = db.Column(db.String())
    recipe = db.relationship(Recipe, lazy='select', backref=db.backref('images', lazy='joined'))

class RecipeIngredient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(Integer, ForeignKey('recipe.id'))
    description = db.Column(db.String())
    recipe = db.relationship(Recipe, lazy='select', backref=db.backref('ingredients', lazy='joined'))

class RecipeIngredientCoupon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    recipe_ingredient_id = db.Column(Integer, ForeignKey('recipe_ingredient.id'))
    image_url = db.Column(db.String())
    savings_amount = db.Column(db.Float())
    short_description = db.Column(db.String())
    ingredient = db.relationship(RecipeIngredient, lazy='select', backref=db.backref('coupons', lazy='joined'))

@api.route('/recipes/')
class RecipeResource(Resource):
    @api.marshal_list_with(recipe)
    def get(self):
        return Recipe.query.all(), 200, {'Access-Control-Allow-Origin': '*'}

    @api.expect(recipe)
    @api.marshal_list_with(recipe)
    def post(self):
        ri = Recipe(**api.payload)
        db.session.add(ri)
        db.session.commit()
        return ri, 201, {'Access-Control-Allow-Origin': '*'}

@api.route('/recipes/<int:id>')
class RecipeResource(Resource):
    @api.marshal_with(recipe)
    def get(self, id):
        ri = Recipe.query.get(id)

        if ri:
            return ri, 200, {'Access-Control-Allow-Origin': '*'}

        return {'message': 'not found'}, 400, {'Access-Control-Allow-Origin': '*'}

    def delete(self, id):
        ri = Recipe.query.get(id)

        if ri:
            db.session.delete(ri)
            db.session.commit()

            return 'successfully deleted', 204, {'Access-Control-Allow-Origin': '*'}
        else:
            return {'message': 'not found'}, 400, {'Access-Control-Allow-Origin': '*'}

@api.route('/recipe-images/')
class RecipeImageResource(Resource):
    @api.marshal_list_with(recipe_image)
    def get(self):
        return RecipeImage.query.all(), 200, {'Access-Control-Allow-Origin': '*'}

    @api.expect(recipe_image)
    @api.marshal_list_with(recipe_image)
    def post(self):
        ri = RecipeImage(**api.payload)
        db.session.add(ri)
        db.session.commit()
        return ri, 201, {'Access-Control-Allow-Origin': '*'}

@api.route('/recipe-images/<int:id>')
class RecipeImageResource(Resource):
    @api.marshal_with(recipe_image)
    def get(self, id):
        ri = RecipeImage.query.get(id)

        if ri:
            return ri, 200, {'Access-Control-Allow-Origin': '*'}

        return {'message': 'not found'}, 400, {'Access-Control-Allow-Origin': '*'}

    def delete(self, id):
        ri = RecipeImage.query.get(id)

        if ri:
            db.session.delete(ri)
            db.session.commit()

            return 'successfully deleted', 204, {'Access-Control-Allow-Origin': '*'}
        else:
            return {'message': 'not found'}, 400, {'Access-Control-Allow-Origin': '*'}

@api.route('/recipe-ingredients/')
class RecipeIngredientResource(Resource):
    @api.marshal_list_with(recipe_ingredient)
    def get(self):
        return RecipeIngredient.query.all(), 200, {'Access-Control-Allow-Origin': '*'}

    @api.expect(recipe_image)
    @api.marshal_list_with(recipe_ingredient)
    def post(self):
        ri = RecipeIngredient(**api.payload)
        db.session.add(ri)
        db.session.commit()
        return ri, 201, {'Access-Control-Allow-Origin': '*'}

@api.route('/recipe-ingredients/<int:id>')
class RecipeIngredientResource(Resource):
    @api.marshal_with(recipe_ingredient)
    def get(self, id):
        ri = RecipeIngredient.query.get(id)

        if ri:
            return ri, 200, {'Access-Control-Allow-Origin': '*'}

        return {'message': 'not found'}, 400, {'Access-Control-Allow-Origin': '*'}

    def delete(self, id):
        ri = RecipeIngredient.query.get(id)

        if ri:
            db.session.delete(ri)
            db.session.commit()

            return 'successfully deleted', 204, {'Access-Control-Allow-Origin': '*'}
        else:
            return {'message': 'not found'}, 400, {'Access-Control-Allow-Origin': '*'}

@api.route('/recipe-ingredient-coupons/')
class RecipeIngredientCouponResource(Resource):
    @api.marshal_list_with(recipe_ingredient_coupon)
    def get(self):
        return RecipeIngredientCoupon.query.all(), 200, {'Access-Control-Allow-Origin': '*'}

    @api.expect(recipe_ingredient_coupon)
    @api.marshal_list_with(recipe_ingredient_coupon)
    def post(self):
        ri = RecipeIngredientCoupon(**api.payload)
        db.session.add(ri)
        db.session.commit()
        return ri, 201, {'Access-Control-Allow-Origin': '*'}

@api.route('/recipe-ingredient-coupons/<int:id>')
class RecipeIngredientCouponResource(Resource):
    @api.marshal_with(recipe_ingredient_coupon)
    def get(self, id):
        ri = RecipeIngredientCoupon.query.get(id)

        if ri:
            return ri, 200, {'Access-Control-Allow-Origin': '*'}

        return {'message': 'not found'}, 400, {'Access-Control-Allow-Origin': '*'}

    @api.response(204, 'delete')
    def delete(self, id):
        ri = RecipeIngredientCoupon.query.get(id)

        if ri:
            db.session.delete(ri)
            db.session.commit()

            return 'successfully deleted', 200, {'Access-Control-Allow-Origin': '*'}
        else:
            return {'message': 'not found'}, 400
