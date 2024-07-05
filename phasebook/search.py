from flask import Blueprint, request

from .data.search_data import USERS

bp = Blueprint("search", __name__, url_prefix="/search")

@bp.route("")
def search():
    return {"results": search_users(**request.args)}, 200

def search_users(id=None, name=None, age=None, occupation=None):
    result = []

    # Convert age to an integer if it is provided
    if age is not None:
        try:
            age = int(age)
        except ValueError:
            return {"error": "Invalid age parameter"}, 400

    for user in USERS:
        if id and user['id'] == id:
            result.append(user)
            continue

        if name and name.lower() in user['name'].lower():
            result.append(user)
            continue

        if age is not None and age - 1 <= user['age'] <= age + 1:
            result.append(user)
            continue

        if occupation and occupation.lower() in user['occupation'].lower():
            result.append(user)
            continue

    # Remove duplicates
    result = [dict(t) for t in {tuple(d.items()) for d in result}]
    
    # Sort the results based on the priority
    result.sort(key=lambda x: (
        1 if x.get('id') == id else 0,
        1 if name and name.lower() in x.get('name').lower() else 0,
        1 if age is not None and age - 1 <= x.get('age') <= age + 1 else 0,
        1 if occupation and occupation.lower() in x.get('occupation').lower() else 0
    ), reverse=True)
    
    return result
