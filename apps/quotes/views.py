from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt


def index(request):
    print('\n= = = index = = =')
    return render(request, 'quotes/index.html')

def registration(request):
    print('\n regitration========')
    if request.method == 'POST':
        errors = User.objects.registration_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_pw)
            request.session['id'] = User.objects.get(email=request.POST['email']).id
            request.session['first_name'] = User.objects.get(email=request.POST['email']).first_name
            request.session['last_name'] = User.objects.get(email=request.POST['email']).last_name
            messages.success(request, "WELCOME FROM REGISTRATION")
            return redirect('/quotes_html')

def login(request):
    print('\n LOGIN============')
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            request.session['id'] = User.objects.get(email=request.POST['email']).id
            messages.success(request, "WELCOME FROM LOGIN")
            return redirect('/quotes_html')


# =========================== QUOTES ============================
def quotes_html(request):
    print('\n quotes_html =========')
    if 'id' in request.session:
        userDB = User.objects.get(id=request.session['id'])
        quotesDB = Quote.objects.all()
        usersall = User.objects.all()
        context = {
            'user': userDB,
            'quotes': quotesDB
        }
        return render(request, 'quotes/quotes_html.html', context)
    else:
        return redirect('/')

def quotes_add_method(request):
    print('\n quotes add method =========')
    if 'id' in request.session:
        if request.method == 'POST': 
            print('\n update_method ==========')
            errors = Quote.objects.quote_validator(request.POST)
            if len(errors):
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/quotes_html')
            else:
                quote = Quote.objects.create(author=request.POST['author'], quote=request.POST['quote'], uploader=User.objects.get(id=request.session['id']))
                quote.save()
                return redirect('/quotes_html')   
    else: 
        return redirect('/')


# ========================= user ======================
def user(request, id):
    if 'id' in request.session:
        print('\n user html =========')
        user = User.objects.get(id=id)
        quotes = User.objects.get(id=id).uploaded_quotes.all()
        context = {
            'user': user,
            'quotes': quotes,
        }
        return render(request, 'quotes/user.html', context)
    else: 
        return redirect('/')




# ========================== DELETE ======================

def delete(request, id):
    if 'id' in request.session:
        print('\inside delete method -----------')
        # if request.method == 'POST':
        Quote.objects.get(id=id).delete()
        print('\n======== quote deleted')
        return redirect('/quotes_html')
    else:
        return redirect('/')


# =========================== UPDATE / EDIT ========================
def edit(request, id):
    if 'id' in request.session:
        print('\n edit ==========')
        user = User.objects.get(id=request.session['id'])
        context = { 'user': user}
        return render(request, 'quotes/edit.html', context)
    else:
        return redirect('/')

def edit_method(request):
    if 'id' in request.session:
        if request.method == 'POST': 
            print('\n update_method ==========')
            errors = User.objects.update_validator(request.POST)
            if len(errors):
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect('/edit/'+str(request.session['id']))
            else:
                user = User.objects.get(id=request.session['id'])
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()
                return redirect('/quotes_html')   
    else: 
        return redirect('/')

# =========================== LOGOUT ===========================
def logout(request):
    print('\n= = = LOGOUT = = =')
    request.session.clear()
    return redirect('/')




# ===========================likes method ====================
def likes(request, id):
    print('\n LIKES LIKES LIKES LIKES ----- method--------')
    u = User.objects.get(id=request.session['id'])
    u.liked_quotes.add(Quote.objects.get(id=id))
    u.save()
    print('\n liked quote saved =-=-=-=-=-==-=-\n')
    return redirect('/quotes_html')