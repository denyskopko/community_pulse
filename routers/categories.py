from flask import Blueprint, jsonify, request
from sqlalchemy import select
from models import Category
from pydantic import ValidationError
from core.db import db
from schemas.questions import CategoryBase , CategoryResponse

"""POST /categories: создание новой категории.
GET /categories: получение списка всех категорий.
PUT /categories/{id}: обновление категории по ID.
DELETE /categories/{id}: удаление категории по ID.
Обновите существующие эндпоинты вопросов, чтобы они поддерживали работу с категориями.
GET /questions: должен возвращать вопросы с информацией о категориях.
POST /questions: должен позволять указывать категорию при создании вопроса."""


categories_bp = Blueprint("categories", __name__, url_prefix="/categories")


@categories_bp.route("/", methods=["GET"])
def get_all_categories():
    #GET /categories: получение списка всех категорий
    stmt = select(Category)
    categories = db.session.execute(stmt).scalars().all()
    serialized = [CategoryResponse.model_validate(cat).model_dump()for cat in categories]
    return jsonify(serialized), 200


@categories_bp.route("/", methods=["POST"])
def create_new_category():
    raw_data = request.get_json(silent=True)
    if not raw_data:
        return jsonify({"error": "Request body is missing or not valid JSON"}), 400  # 400 BAD REQUEST
    try:
        validated_data = CategoryBase.model_validate(raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    try:
        new_category = Category(**validated_data.model_dump())
        db.session.add(new_category)
        db.session.commit()

        return jsonify(CategoryResponse.model_validate(new_category).model_dump()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to create new category", "detail": str(e)}), 500


@categories_bp.route("/<int:category_id>", methods=["PUT", "PATCH"])
def update_category_by_id(category_id: int):
    raw_data = request.get_json(silent=True)
    if not raw_data:
        return jsonify({"error": "Request body is missing or not valid JSON"}), 400  # 400 BAD REQUEST

    try:
        validated_data = CategoryBase.model_validate(raw_data)
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400

    stmt = select(Category).where(Category.id == category_id)
    category = db.session.execute(stmt).scalars().one_or_none()

    if not category:
        return jsonify({"error": f"Category with ID {category_id} not found"}), 404

    try:
        for key, value in validated_data.model_dump().items():
            setattr(category, key, value)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Failed to update category with ID {category_id}",
            "detail": str(e)
        }), 500  # 500 INTERNAL SERVER ERROR

    return jsonify(CategoryResponse.model_validate(category).model_dump()), 200



@categories_bp.route("/<int:category_id>", methods=["DELETE"])
def delete_category(category_id: int):
    category = db.session.get(Category, category_id)
    if not category:
        return jsonify({"error": f"Category with ID {category_id} not found"}), 404

    try:
        db.session.delete(category)
        db.session.commit()
        return jsonify({"message": f"Category with ID {category_id} deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "error": f"Failed to delete category with ID {category_id}",
            "detail": str(e)
        }), 500