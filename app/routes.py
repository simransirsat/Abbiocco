from app import app
from flask import request
from flask import render_template, flash, redirect, url_for, request, g, session
from app.forms import LoginForm
from flask_login import logout_user
from flask_login import current_user, login_user, login_required
from werkzeug.urls import url_parse
from app.models import User
from app import db
from app.forms import RegistrationForm, EditProfileForm
from app import api_calls
import helper_functions
@app.route('/')
@app.route('/index', methods=['GET','POST'])
def index():
	if request.method == "POST":
		result = request.form
		recipe_search = result['top-search']
		results_json = api_calls.recipe_search(recipe_search, 6)
		print(results_json)

		for recipe in results_json['results']:
			recipe_id = str(recipe['id'])
			summary_response = api_calls.summary_info(recipe_id)
			summary_json = summary_response
			summary_text = summary_json['summary']
			recipe['summary'] = summary_text
			recipe['imgUrl'] = results_json['baseUri'] + recipe['image']
		result = results_json['results']
		return render_template('catagory-post.html',result=result)
	else:
		return render_template('index.html')

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form=LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is None or not user.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(user,remember=False)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc!= '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html',form=form)

@app.route('/register', methods=['GET','POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('index'))
	form = RegistrationForm()
	if form.validate_on_submit():
		user = User(username=form.username.data, email=form.email.data,  dob=form.dob.data, name=form.name.data, height=form.height.data, weight=form.weight.data, gender= form.gender.data)
		user.set_password(form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Congratulations, you are now a registered user!')
		return redirect(url_for('login'))
	return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/bookmarks')
@login_required
def quickView():
	bookmarked_recipes = current_user.recipes
	bookmarks = []
	for recipe in bookmarked_recipes:
		bookmarks.append({
			'title' : recipe.recipe_name,
			'image' : recipe.img_url,
			'servings' : '3 servings',
			'id': recipe.recipe_id
			})

	return render_template('explore.html',bookmarks=bookmarks)

@app.route('/recipe/<recipe_id>',methods=['GET','POST'])
def recipe(recipe_id):
	user = User.query.filter_by(username=current_user.username).first()
	bookmark = False
	if helper_functions.check_if_bookmark_exists(recipe_id,current_user.id):
		bookmark = True
	else:
		bookmark = False
	recipe_info_json = api_calls.recipe_info(recipe_id)

	title = recipe_info_json['title']
	img = recipe_info_json['image']
	ingredients = recipe_info_json['extendedIngredients']
	cooking_instructions = recipe_info_json['analyzedInstructions'][0]
	servings = recipe_info_json['servings']
	source = recipe_info_json['sourceName']
	time = 100
	likes = recipe_info_json['aggregateLikes']
	ins = []
	print(cooking_instructions['steps'])
	for element in cooking_instructions['steps']:
		ins.append(
		{
			'step': element['number'],
			'val': element['step']
		})
	if request.method == 'POST':
		if helper_functions.check_if_bookmark_exists(recipe_id,current_user.id):
			bookmark = True
		else:
			bookmark = False
		message = process_recipe_bookmark_button(recipe_id)
		flash(message)
	return render_template("receipe.html",bookmark=bookmark,user=user,title=title,source=source,img=img,ingredients=ingredients,ins=ins,servings=servings,time=time,likes=likes)
@app.route('/view/details')
def details():
	return render_template('single-post.html')

@app.route('/contact')
def contacts():
	return render_template('contact.html')

@app.route('/category')
def category():
	return render_template('catagory.html')

@app.route('/search')
def recipe_search(result):
	
	return render_template('catagory-post.html',result=result)

@app.route("/bookmark.json", methods=["POST"])
@login_required
def process_recipe_bookmark_button(recipe_id):
    """Adds bookmark to DB, returning either a success or error message
    back to ajax success function."""

    # Unpack info from ajax

    # Check if recipe in DB. If not, add new recipe to DB.
    current_recipe = helper_functions.check_if_recipe_exists(recipe_id)

    if not current_recipe:
        current_recipe = helper_functions.add_recipe(recipe_id,current_user)

    # Check if user already bookmarked recipe. If not, add to DB.
    bookmark_exists = (helper_functions
                       .check_if_bookmark_exists(recipe_id,
                                                 current_user.id))

    if not bookmark_exists:
        helper_functions.add_bookmark(current_user.id,
                                      recipe_id)
        # Return success message to bookmark-recipe.js ajax success fn
        success_message = "This recipe has been bookmarked!"
        return success_message

    # Return error message to bookmark-recipe.js ajax success fn
    error_message = "You've already bookmarked this recipe."
    return error_message

@app.route("/profile/",  methods=["GET","POST"])
@login_required
def view_profile():
	profile = User.query.filter_by(username=current_user.username).first()
	form = RegistrationForm()
	#try:
	# 	if request.method == "POST" and form.validate():
	# 		current_user.weight= form.weight.data
	# 		current_user.height = form.height.data
	# 		current_user.dob = form.dob.data
	# 		current_user.gender = form.gender.data
	# 		db.session.commit()
	# 		return render_template("profile.html", form=form)
	# except:
	#	pass
	if request.method == "GET":
		form.weight.data = current_user.weight
		form.height.data = current_user.height
		form.dob.data = current_user.dob
		form.gender.data = current_user.gender
	return render_template("profile.html", form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
	form = EditProfileForm()
	if form.validate_on_submit():
		current_user.weight= form.weight.data
		current_user.height = form.height.data
		current_user.dob = form.dob.data
		current_user.gender = form.gender.data
		current_user.name = form.name.data
		current_user.username = form.username.data
		current_user.email = form.email.data
		current_user.set_password(form.password.data)
		db.session.commit()
		return redirect(url_for('view_profile'))
	elif request.method == 'GET':
		form.weight.data = current_user.weight
		form.height.data = current_user.height
		form.dob.data = current_user.dob
		form.gender.data = current_user.gender
		form.name.data = current_user.name
		form.username.data = current_user.username
		form.email.data = current_user.email
		#form.password.data = current_user.password
	return render_template('edit_profile.html', title='Edit Profile',form=form)

@app.route('/pantry')
def pantry():
	return render_template('pantry.html')