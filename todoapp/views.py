from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout as django_logout # Use alias like "django_logout" so that django doesnt get confused on which function to use.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from .helpers import Helpers
from .models import *
from .forms import *

def user_login(request):
	# Redirect if already logged-in
	if request.user.is_authenticated:
		return redirect(Helpers.get_path('user/account'))
	
	if request.method == 'POST':
		# Process the request if posted data are available
		username = request.POST['username']
		password = request.POST['password']
		# Check username and password combination if correct
		user = authenticate(username=username, password=password)
		if user is not None:
			# Success, now let's login the user. 
			login(request, user)
			print('authenticated user')
			# Then redirect to the accounts page.
			return redirect(Helpers.get_path('user/account'))
		else:
			# Incorrect credentials, let's throw an error to the screen.
			return render(request, ('user/login.html'), {'error_message': 'Incorrect username and / or password.'})
	else:
		# No post data availabe, let's just show the page to the user.
		return render(request, ('user/login.html'))

def user_account(request):
	err_succ = {'status': 0, 'message': 'An unknown error occured'}
	
	# Create instance of the form and populate it with requests
	form = AccountForm(request.POST)
	
	# Redirect if not logged-in
	if request.user.is_authenticated == False:
		return redirect(Helpers.get_path('user/login')) 
	
	if request.method == 'POST':
		if form.is_valid():	
			# Query data of currently logged-in user.
			user = User.objects.get(username=request.user.username)
			
			# Check if username exists
			if User.objects.filter(username=form.cleaned_data['username']).exists() and user.username != form.cleaned_data['username']:
				err_succ['message'] = 'Username aleady taken, please enter a different one.'
			
			# Check if email exists		
			elif User.objects.filter(email=form.cleaned_data['email']).exists() and user.email != form.cleaned_data['email']:
				err_succ['message'] = 'Email already taken, please enter a different one'
				
			elif form.cleaned_data['old_password'] and form.cleaned_data['password_repeat'] and form.cleaned_data['password']:
				# Check if passwords match
				if form.cleaned_data['password_repeat'] != form.cleaned_data['password']:
					err_succ['message'] = 'New password do not match.'
				
				# Check if old password is correct
				elif not user.check_password(form.cleaned_data['old_password']):
					err_succ['message'] = 'Incorrect old password.'
					
			else:
				user.username = form.cleaned_data['username']
				user.first_name = form.cleaned_data['first_name']
				user.last_name = form.cleaned_data['last_name']
				
				user.member.phone_number = form.cleaned_data['phone_number']
				user.member.about = form.cleaned_data['about_me']
				
				# Save new password if passes above validations
				if form.cleaned_data['password']:
					user.set_password(form.cleaned_data['password'])
				
				# Save posted fields to their respective tables
				user.member.save()
				user.save()
				
				# Show success message
				err_succ['status'] = 1
				err_succ['message'] = 'Account successfully updated.'
			
		return JsonResponse(err_succ)
	else:
		# Let's define intial data that we are going to use to populate our account form.
		user_data = {
			'username': request.user.username, 
			'email': request.user.email, 
			'first_name': request.user.first_name, 
			'last_name': request.user.last_name, 
			'phone_number': request.user.member.phone_number, 
			'about_me': request.user.member.about 
		}
		# Render the account form
		return render(request, Helpers.get_url('user/account.html'), {'form': AccountForm(initial=user_data)})

def user_register(request):
	# Redirect if already logged-in
	if request.user.is_authenticated:
		return redirect(Helpers.get_path('user/account'))
	
	# Create instance of the form and populate it with requests
	form = RegisterForm(request.POST)
	
	# Define default values
	err_succ = {'status': 0, 'message': 'An unknown error occured'}
	
	if request.method == 'POST':
		# check whether it's valid:
		if form.is_valid():
			if User.objects.filter(username=form.cleaned_data['username']).exists():
				err_succ['message'] = 'Username already exists.'
				
			elif User.objects.filter(email=form.cleaned_data['email']).exists():
				err_succ['message'] = 'Email already exists.'
				
			elif form.cleaned_data['password'] != form.cleaned_data['password_repeat']:
				err_succ['message'] = 'Passwords do not match.'
				
			else:
				# Create the user: 
				user = User.objects.create_user(
					form.cleaned_data['username'], 
					form.cleaned_data['email'], 
					form.cleaned_data['password']
				)
				user.first_name = form.cleaned_data['first_name']
				user.last_name = form.cleaned_data['last_name']
				
				member = Member.objects.create(
					user = user,
					phone_number = form.cleaned_data['phone_number'],
					about = ''
				)
				
				member.save()
				user.save()
				
				# Login the user
				login(request, user)
				
				# return account page URL where we will be redirecting the user.
				err_succ['status'] = 1
				err_succ['message'] = 'Sucessfully registered, redirecting to your account..'
				
		return JsonResponse(err_succ)

   # No post data availabe, let's just show the page.
	else:
		return render(request, Helpers.get_url('user/register.html'), {'form': RegisterForm()})

def logout(request):
	print('in logout view...')
	django_logout(request)
	if request.user.username == 'admin':
		print('in iff......')
		return redirect('/admin_login/account')
	else:
		print('in else.......')
		return redirect(Helpers.get_path('user/login'))

def login_admin(request):
	if request.method == 'GET':
		print('in get request..',)
		return render(request, Helpers.admin_url('login.html'))
	
	if request.method == 'POST':
		print('in post methid...')
		username=request.POST.get('username')
		password =request.POST.get('pass')
		print(username,password)
		try:
			user = authenticate(username = username, password = password)
			user_obj=User.objects.get(username = username)
			if user_obj.username == 'admin':
				print('yes admin here..')
				login(request, user)
				return render(request, Helpers.admin_url('account.html'),{'info': 'You cant login here'})
				return redirect(Helpers.get_path('admin_login/orders'))
			else:
				return render(request, Helpers.admin_url('login.html'),{'info': 'You cant login here'})
		except:
			return render(request, Helpers.admin_url('login.html'),{'data': 'password or username is wrong'})

def all_todolist(request):
	# Redirect if already logged-in
	if request.user.is_authenticated:
		todolists = Todolist.objects.filter(user=request.user)
		# todolists = Todolist.objects.all()
		print(todolists)
		return render(request, ('user/todolist.html'), {'todolists':todolists})
	else:
		# No post data availabe, let's just show the page to the user.
		return render(request, ('user/login.html'))
	
def create_todo(request):
	err_succ = {'status': 0, 'message': 'An unknown error occured'}
	
	# Create instance of the form and populate it with requests
	form = TODOForm(request.POST)

	# Redirect if already logged-in
	if request.user.is_authenticated:	
		if request.method == 'POST':
			if form.is_valid():	
				# Query data of currently logged-in user.
				user = User.objects.get(username=request.user.username)

				todolist = Todolist.objects.create(
					user = user,
					title = form.cleaned_data['title'],
					description = form.cleaned_data['description'],
					status = form.cleaned_data['status']
				)
				
				# Save posted fields to their respective tables
				todolist.save()
					
				# Show success message
				err_succ['status'] = 1
				err_succ['message'] = 'TODO successfully Added.'
				
			return JsonResponse(err_succ)
		else:
			return render(request, ('user/createtodo.html'), {'form': TODOForm})
	else:
		# No post data availabe, let's just show the page to the user.
		return render(request, ('user/login.html'))

def update_todo(request, id):
	err_succ = {'status': 0, 'message': 'An unknown error occured'}
	
	# Create instance of the form and populate it with requests

	# Redirect if already logged-in
	if request.user.is_authenticated:	
		if request.method == 'POST':
			form = TODOForm(request.POST)
			if form.is_valid():	
				ttodolist = Todolist.objects.get(id=id)
				ttodolist.title = form.cleaned_data['title']
				ttodolist.status = form.cleaned_data['status']
				ttodolist.description = form.cleaned_data['description']
				# Save posted fields to their respective tables
				ttodolist.save()
					
				# Show success message
				err_succ['status'] = 1
				err_succ['message'] = 'TODO successfully Updated.'
				
			return JsonResponse(err_succ)
		else:
			ttodolist = get_object_or_404(Todolist, id=id)
			print(ttodolist)
			if ttodolist.status == 1:
				list_data = {
					'title': ttodolist.title, 
					'status': ttodolist.status, 
					'description': ttodolist.description 
				}
			else:
				list_data = {
					'title': ttodolist.title, 
					'description': ttodolist.description 
				}
			return render(request, ('user/edittodo.html'), {'listid': ttodolist.id,'form': TODOForm(initial=list_data)})
	else:
		# No post data availabe, let's just show the page to the user.
		return render(request, ('user/login.html'))

def delete_todo(request, id):
	# Redirect if already logged-in
	if request.user.is_authenticated:	
		ttodolist = get_object_or_404(Todolist, id=id)
		ttodolist.delete()
		return redirect(Helpers.get_path('user/alltodolist'))
	else:
		# No post data availabe, let's just show the page to the user.
		return render(request, ('user/login.html'))