from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

from django.db.models import Q

from .models import Contact
from .forms import AddContactForm, UpdateContactForm



def home(request):
    request.session['last_page'] = 'home'
    user = str(request.user)
    contact_list = None
    query = request.GET.get('query')
    if query:
        contact_list = Contact.objects.filter(
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        contact_list = Contact.objects.all()

    if user == 'AnonymousUser':
        return render(request, 'home.html', {'contacts': contact_list, 'user': None})
    
    return render(request, 'home.html', {'contacts': contact_list, 'user': user})


def contact_detail(request, pk):
    try:
        contact = Contact.objects.get(pk=pk)
        print(contact)
        return render(request, 'contact_detail.html', {'contact': contact})
        
    except Contact.DoesNotExist:
        return render(request, 'not_found.html')
    

def search(request):
    pass
   
def authorize_admin(request):
    user = str(request.user)
    # print(user)
    last_page = request.session.get('last_page', None)
    if user != 'admin':
        login_form = AuthenticationForm()

        if request.method == 'POST':
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)

                print(last_page)
                if last_page == 'home':
                    return redirect(home)
                elif last_page == 'add':
                    return redirect(add_contact)
                elif last_page == 'update':
                    return redirect(update_contact_list)
                elif last_page == 'delete':
                    return redirect(delete_contact_list)
            
        return render(request, 'login.html', {'login_form': login_form})
    
    # If you accidently pressed login & already logged in, then it just redirects you to the last page.
    if last_page == 'home':
        return redirect(home)
    elif last_page == 'add':
        return redirect(add_contact)
    elif last_page == 'update':
        return redirect(update_contact_list)
    elif last_page == 'delete':
        return redirect(delete_contact_list)
    

def unauthorize_admin(request):
    user = str(request.user)
    print(user)
    if user == 'AnonymousUser':
        return render(request, 'logout.html', {'user': None})

    logout(request)
    return render(request, 'logout.html', {'user': user})

def add_contact(request):
    user = str(request.user)
    if user != 'admin':
        request.session['last_page'] = 'add'
        return redirect(authorize_admin)
    
    if request.method == 'POST':
        new_contact = AddContactForm(request.POST)
        
        if new_contact.is_valid():
            new_contact.save()
            return redirect(home)
        else:
            return render(request, 'contact_form.html', {'contact_form': new_contact})

    return render(request, 'contact_form.html', {'contact_form': AddContactForm()})


def update_contact_list(request):
    user = str(request.user)
    if user != 'admin':
        request.session['last_page'] = 'update'
        return redirect(authorize_admin)

    contact_list = Contact.objects.all()
    return render(request, 'update_contact.html',  {'contacts': contact_list})


def update_an_contact(request,pk):
    user = str(request.user)
    if user != 'admin':
        # return redirect()
        return render(request, 'not_admin.html', {'user': user})
    
    try:
        # print(pk)
        contact = Contact.objects.get(pk=pk)
        update_contact_form = UpdateContactForm(instance=contact)

        if request.method == 'POST':
            updated_contact = UpdateContactForm(request.POST, instance=contact)
            if 'salary' in updated_contact.changed_data or 'designation' in updated_contact.changed_data:
                return render(request, 'contact_form.html', {'contact_form': updated_contact, 'form': 'update', 'error': 1})
            
            if updated_contact.is_valid():
                updated_contact.save()
                return redirect(home)
            else:
                return render(request, 'contact_form.html', {'contact_form': updated_contact, 'form': 'update'})
        
        return render(request, 'contact_form.html', {'contact_form': update_contact_form , 'form': 'update'})

    except Contact.DoesNotExist:
        return render(request, 'not_found.html')


def delete_contact_list(request):
    user = str(request.user)
    if user != 'admin':
        request.session['last_page'] = 'delete'
        return redirect(authorize_admin)

    contact_list = Contact.objects.all()
    return render(request, 'delete_contact.html',  {'contacts': contact_list})


def delete_an_contact(request, pk):
    user = str(request.user)
    if user != 'admin':
        return render(request, 'not_admin.html', {'user': user})
    
    try:
        # print(pk)
        contact = Contact.objects.get(pk=pk)
        contact.delete()
        return redirect(home)

    except Contact.DoesNotExist:
        return render(request, 'not_found.html')