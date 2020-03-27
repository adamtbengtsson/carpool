from flask import request, jsonify, abort, make_response, Response
from flaskblog import app, db, bcrypt
from flaskblog.models import Token, Post, User, Car
import datetime


# method used to create a token that can be used for some time defined by the delta
@app.route('/api/token/public', methods=['GET'])
def token():
	expired = datetime.datetime.now() + datetime.timedelta(minutes=60)
	token_string = bcrypt.generate_password_hash(str(expired)).decode('utf-8')
	new_token = Token(token=token_string, date_expired=expired)
	db.session.add(new_token)
	try:
		db.session.commit()
		return jsonify({'token': token_string, 'expire': expired.strftime('%Y-%m-%d %H:%M:%S')})
	except:
		db.session.rollback()
		return abort(400)


# method used to inform the user of the webservice regarding its capabilities
@app.route('/api/', methods=['GET'])
def api():
	info = dict()
	info['message'] = 'This is the API to consume blog posts'
	info['services'] = []
	info['services'].append({'url': '/api/posts', 'method': 'GET', 'description': 'Gets a list of posts'})
	print(info)
	return jsonify(info)


@app.route('/api/users', methods=['GET'])
def api_get_users():
	users = User.query.all()
	return jsonify(users)

#GET CARS
@app.route('/api/cars', methods=['GET'])
def api_get_cars():
	cars = Car.query.all()
	return jsonify(cars)

@app.route('/api/posts', methods=['GET'])
def api_get_posts():
	posts = Post.query.all()
	return jsonify(posts)

#GET CAR
@app.route('/api/car/<int:car_id>', methods=['GET'])
def api_get_car(car_id):
	car = Car.query.get_or_404(car_id)
	return jsonify(car)


@app.route('/api/post/<int:post_id>', methods=['GET'])
def api_get_post(post_id):
	post = Post.query.get_or_404(post_id)
	return jsonify(post)


@app.route('/api/posts', methods=['POST'])
def api_create_post():
	data = request.json
	if 'title' in data and 'content_type' in data and 'content' in data and 'user' in data:
		post = Post(title=data['title'],
					content_type=data['content_type'],
					content=data['content'],
					user_id=int(data['user']))
		db.session.add(post)
		try:
			db.session.commit() # how would you improve this code?
			return jsonify(post), 201 # status 201 means "CREATED"
		except:
			db.session.rollback()
			abort(400)
	else:
		return abort(400) # 400 is bad request


# CREATE CAR
@app.route('/api/cars', methods=['POST'])
def api_create_car():
    data = request.json
    if 'car_name' in data and 'model' in data and 'license_plate' in data and 'fuel' in data and 'seats' in data and 'user' in data:
		car = Car(car_name=data['car_name'],
                  model=data['model'],
                  license_plate=data['license_plate'],
                  fuel=data['fuel'],
                  seats=data['seats'],
				  user_id=int(data['user'])
				  )
		db.session.add(car)
		try:
			db.session.commit() # how would you improve this code?
			return jsonify(car), 201 # status 201 means "CREATED"
		except:
			db.session.rollback()
			abort(400)
	else:
		return abort(400) # 400 is bad request



# method PUT replaces the entire object
@app.route('/api/post/<int:post_id>', methods=['PUT'])
def api_update_post(post_id):
	post = Post.query.get_or_404(post_id)
	data = request.json
	if 'title' in data and 'content_type' in data and 'content' in data and 'user' in data:
		post.title = data['title']
		post.content_type = data['content_type']
		post.content = data['content']
		post.user_id = data['user']
		try:
			db.session.commit()
			return jsonify(post), 200
		except:
			db.session.rollback()
			abort(400)
	else:
		return abort(400) # bad request

#UPDATE CAR
@app.route('/api/car/<int:car_id>', methods=['PUT'])
def api_update_car(car_id):
	car = Car.query.get_or_404(car_id)
	data = request.json
	if 'car_name' in data and 'model' in data and 'license_plate' in data and 'fuel' in data and 'seats' in data and 'user' in data:
		car.car_name = data['car_name']
		car.model = data['model']
		car.license_plate = data['license_plate']
		car.fuel = data['fuel']
		car.seats = data['seats']
		car.user_id = data['user']
		try:
			db.session.commit()
			return jsonify(car), 200
		except:
			db.session.rollback()
			abort(400)
	else:
		return abort(400) # bad request


@app.route('/api/post/<int:post_id>', methods=['PATCH'])
def api_replace_post(post_id):
	post = Post.query.get_or_404(post_id)
	data = request.json
	# you should have at least one of the columns to be able to perform an update
	if 'title' in data or 'content_type' in data or 'content' in data or 'user' in data:
		if 'title' in data:
			post.title = data['title']
		if 'content_type' in data:
			post.content_type = data['content_type']
		if 'content' in data:
			post.content = data['content']
		if 'user' in data:
			post.user_id = data['user']
		try:
			db.session.commit()
			return jsonify(post), 200
		except:
			db.sesion.rollback()
			abort(400)
	else:
		return abort(400) # bad request

#REPLACE CAR
@app.route('/api/car/<int:car_id>', methods=['PATCH'])
def api_replace_car(car_id):
	car = Car.query.get_or_404(car_id)
	data = request.json
	# you should have at least one of the columns to be able to perform an update
	if 'car_name' in data and 'model' in data and 'license_plate' in data and 'fuel' in data and 'seats' in data and 'user' in data:
		if 'car_name' in data:
			car.car_name = data['car_name']
		if 'model' in data:
			car.model = data['model']
		if 'license_plate' in data:
			car.license_plate = data['license_plate']
		if 'fuel' in data:
			car.fuel = data['fuel']
		if 'seats' in data:
			car.seats = data['seats']
		if 'user' in data:
			car.user_id = data['user']
		try:
			db.session.commit()
			return jsonify(car), 200
		except:
			db.sesion.rollback()
			abort(400)
	else:
		return abort(400) # bad request


@app.route('/api/post/<int:post_id>', methods=['DELETE'])
def api_delete_post(post_id):
	post = db.session.query(Post).get(post_id)
	db.session.delete(post)
	try:
		db.session.commit()
		return jsonify({'message': f'Post {post_id} deleted'}), 200
	except:
		db.session.rollback()
		abort(400)


#DELETE CAR
@app.route('/api/car/<int:car_id>', methods=['DELETE'])
def api_delete_car(car_id):
	car = db.session.query(Car).get(car_id)
	db.session.delete(car)
	try:
		db.session.commit()
		return jsonify({'message': f'Car {car_id} deleted'}), 200
	except:
		db.session.rollback()
		abort(400)