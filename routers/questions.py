from flask import Blueprint

questions_bp = Blueprint(
    "questions",
    __name__,  # questions.py
    url_prefix="/questions"
)

# В декораторе route метод по умолчанию -- GET метод
# Если мы явно не указываем метод запроса для декоратора -- по умолчанию система будет ловить именно GET


# Read (list)
@questions_bp.route("")
def get_all_questions():
    return "List of all questions"


# Read (one by ID)
@questions_bp.route("/<int:question_id>")
def get_question_by_id(question_id: int):
    return f"Retrieve one question by ID: {question_id}"


# Create
@questions_bp.route("/create", methods=["POST"])
def create_new_question():
    return "CREATE NEW QUESTION"


# Update
@questions_bp.route("/<int:question_id>/update", methods=["PUT", "PATCH"])
def update_question_by_id(question_id: int):
    return f"Update question by it's ID: {question_id}"


# Delete
@questions_bp.route("/<int:question_id>/delete", methods=["DELETE"])
def delete_question_by_id(question_id: int):
    return f"Delete question by it's ID: {question_id}"
