from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import hashlib
import database
from config import config

app = Flask(__name__)
CORS(app)

serverParams = config('server')





# Creates a connection to postgresql database
# psycopg2.connect(dbOptions)


@app.route('/')
def hello_world():
    return "Uh oh, you shouldn't be here!!"


# ===========
#  API views
# ===========

@app.route('/api/plans/', defaults={'plan_id': None}, methods=['GET', 'POST'])
@app.route('/api/plans/<int:plan_id>', methods=['GET', 'PUT', 'DELETE'])
def plan(plan_id):
    if request.method == 'GET':
        fetched_plans = database.fetch_from_table(table="Plans", field_value=plan_id)
        return make_response(jsonify({'status': 200, 'message': fetched_plans}))

    elif request.method == 'POST':
        try:
            form_data = request.form

            new_plan = {
                "Name": form_data["Name"],
                "PlaylistSize": form_data["PlaylistSize"]
            }

            new_plan = database.insert_into_table("Plans", new_plan)
            return make_response(jsonify({'status': 200, 'message': new_plan}))
        except (Exception, IndexError) as error:
            print(error)
            return make_response(jsonify({'status': 400, 'message': 'Invalid form data'}), 400)

    elif request.method == 'PUT':
        try:
            form_data = request.form

            # TODO: With more time, convert this into database function update_table
            # Build query values and query update fields by using arrays
            query_values = []
            updated_fields = []

            # Check if fields exist in form to be updated
            if "Name" in form_data:
                query_values.append(form_data["Name"])
                updated_fields.append('"Name" = %s')

            if "PlaylistSize" in form_data:
                query_values.append(form_data["PlaylistSize"])
                updated_fields.append('"PlaylistSize" = %s')

            # Merge all fields with ", " and convert values into a tuple to be used by psycopg2
            updated_fields = ", ".join(updated_fields)
            query_values = tuple(query_values)

            # Build query string
            query = f'UPDATE public."Users" SET {updated_fields} WHERE "ID" = %s;'

            database.execute_query(query, query_values)
            updated_plan = database.fetch_from_table(table="Plans", field_value=plan_id)

            return make_response(jsonify({'status': 200, 'message': updated_plan}))
        except (Exception, IndexError) as error:
            print(error)
            return make_response(jsonify({'status': 400, 'message': 'Invalid form data'}), 400)

    elif request.method == 'DELETE':
        # TODO: With more time, convert this into database function delete_from_table
        query = f'DELETE FROM public."Plans" WHERE "ID" = %s;'

        deleted_plan = database.fetch_from_table(table="Plans", field_value=plan_id)
        database.execute_query(query, plan_id)

        return make_response(jsonify({'status': 200, 'message': deleted_plan}))


@app.route('/api/users/', defaults={'user_id': None}, methods=['GET', 'POST'])
@app.route('/api/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    if request.method == 'GET':
        fetched_users = database.fetch_from_table(table="Users", field_value=user_id)
        return make_response(jsonify({'status': 200, 'message': fetched_users}))

    elif request.method == 'POST':
        try:
            form_data = request.form

            # Check if email is unique
            email = f'\'{form_data["Email"]}\''
            test_user = database.fetch_from_table(table="Users", field_name="Email", field_value=email)

            if len(test_user) > 0:
                return make_response(jsonify({"status": 409, "message": "User already exists"}), 409)

            # Hash password with sha256
            encrypted_password = hashlib.sha256(form_data["Password"].encode())

            new_user = {
                "Email": form_data["Email"],
                "Password": encrypted_password.hexdigest(),
                "PlanID": form_data["PlanID"]
            }

            new_user = database.insert_into_table("Plans", new_user)
            return make_response(jsonify({'status': 200, 'message': new_user}))
        except (Exception, IndexError) as error:
            print(error)
            return make_response(jsonify({'status': 400, 'message': 'Invalid form data'}), 400)

    elif request.method == 'PUT':
        try:
            form_data = request.form

            # TODO: With more time, convert this into database function update_table
            # Build query values and query update fields by using arrays
            query_values = []
            updated_fields = []
            if "Email" in form_data:
                query_values.append(form_data["Email"])
                updated_fields.append('"Email" = %s')

            if "Password" in form_data:
                # Hash password with sha256
                encrypted_password = hashlib.sha256(form_data["Password"].encode())
                encrypted_password = encrypted_password.hexdigest()

                query_values.append(encrypted_password)
                updated_fields.append('"Password" = %s')

            if "PlanID" in form_data:
                query_values.append(form_data["PlanID"])
                updated_fields.append('"PlanID" = %s')

            # Merge all fields with ", " and convert values into a tuple to be used by psycopg2
            updated_fields = ", ".join(updated_fields)
            query_values = tuple(query_values)

            # Build query string
            query = f'UPDATE public."Users" SET {updated_fields} WHERE "ID" = %s;'

            database.execute_query(query, query_values)
            updated_user = database.fetch_from_table(table="Users", field_value=user_id)

            return make_response(jsonify({'status': 200, 'message': updated_user}))
        except (Exception, IndexError) as error:
            print(error)
            return make_response(jsonify({'status': 400, 'message': 'Invalid form data'}), 400)

    elif request.method == 'DELETE':
        # TODO: With more time, convert this into database function delete_from_table
        query = f'DELETE FROM public."Users" WHERE "ID" = %s;'

        deleted_plan = database.fetch_from_table(table="Users", field_value=user_id)
        database.execute_query(query, user_id)

        return make_response(jsonify({'status': 200, 'message': deleted_plan}))


@app.route('/api/music/', defaults={'music_id': None}, methods=['GET', 'POST'])
@app.route('/api/music/<int:music_id>', methods=['GET', 'PUT', 'DELETE'])
def music(music_id):
    if request.method == 'GET':
        fetched_music = database.fetch_from_table(table="Music", field_value=music_id)
        return make_response(jsonify({'status': 200, 'message': fetched_music}))

    elif request.method == 'POST':
        try:
            form_data = request.form

            new_music = {
                "Name": form_data["Name"],
                "PlanID": form_data["PlanID"]
            }

            new_music = database.insert_into_table("Music", new_music)
            return make_response(jsonify({'status': 200, 'message': new_music}))
        except (Exception, IndexError) as error:
            print(error)
            return make_response(jsonify({'status': 400, 'message': 'Invalid form data'}), 400)

    elif request.method == 'PUT':
        try:
            form_data = request.form

            # TODO: With more time, convert this into database function update_table
            # Build query values and query update fields by using arrays
            query_values = []
            updated_fields = []
            if "Name" in form_data:
                query_values.append(form_data["Name"])
                updated_fields.append('"Name" = %s')

            if "PlanID" in form_data:
                query_values.append(form_data["PlanID"])
                updated_fields.append('"PlanID" = %s')

            # Merge all fields with ", " and convert values into a tuple to be used by psycopg2
            updated_fields = ", ".join(updated_fields)
            query_values = tuple(query_values)

            # Build query string
            query = f'UPDATE public."Music" SET {updated_fields} WHERE "ID" = %s;'

            database.execute_query(query, query_values)
            updated_user = database.fetch_from_table(table="Music", field_value=music_id)

            return make_response(jsonify({'status': 200, 'message': updated_user}))
        except (Exception, IndexError) as error:
            print(error)
            return make_response(jsonify({'status': 400, 'message': 'Invalid form data'}), 400)

    elif request.method == 'DELETE':
        # TODO: With more time, convert this into database function delete_from_table
        query = f'DELETE FROM public."Music" WHERE "ID" = %s;'

        deleted_plan = database.fetch_from_table(table="Music", field_value=music_id)
        database.execute_query(query, music_id)

        return make_response(jsonify({'status': 200, 'message': deleted_plan}))


@app.route('/api/user_music/<int:user_id>', defaults={'music_id': None}, methods=['GET', 'POST'])
@app.route('/api/user_music/<int:user_id>/<int:music_id>', methods=['GET', 'DELETE'])
def user_music(user_id, music_id):
    # current_user = authenticate_user(request.authorization)

    if request.method == 'GET':
        condition = f'and "MusicID" = {music_id}' if (music_id is not None) else ""

        fetched_user_music = database.fetch_from_query(f'SELECT * FROM public."User_Music" where "UserID" = {user_id} {condition}')
        return make_response(jsonify({'status': 200, 'message': fetched_user_music}))

    elif request.method == 'POST':
        try:
            form_data = request.form

            new_music = {
                "Name": form_data["Name"],
                "PlanID": form_data["PlanID"]
            }

            new_music = database.insert_into_table("Music", new_music)
            return make_response(jsonify({'status': 200, 'message': new_music}))
        except (Exception, IndexError) as error:
            print(error)
            return make_response(jsonify({'status': 400, 'message': 'Invalid form data'}), 400)

    elif request.method == 'DELETE':
        # TODO: With more time, convert this into database function delete_from_table
        # Fetch result to be deleted
        condition = f'and "MusicID" = {music_id}' if (music_id is not None) else ""
        query = f'SELECT * FROM public."User_Music" where "UserID" = {user_id} {condition}'
        fetched_user_music = database.fetch_from_query(query)

        query = f'DELETE FROM public."User_Music" WHERE "UserID" = %s and "MusicID" = %s;'
        database.execute_query(query, (user_id, music_id, ))

        return make_response(jsonify({'status': 200, 'message': fetched_user_music}))


def authenticate_user(request_auth):
    if request_auth is None:
        return None

    password = hashlib.md5(request_auth.password)

    fetched_user = database.fetch_from_query(
        f'SELECT * FROM public."User" WHERE '
        f'"Email"="{request_auth.username}" AND '
        f'"Password"="{password}"')

    return fetched_user


if __name__ == "__main__":
    app.run(**serverParams)
