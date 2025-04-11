from django.shortcuts import render, redirect

# Create your views here.
from .forms import CustomUserCreationForm
from django.contrib.auth import login
from django.template.loader import get_template
#from .models import Products
#from django.conf import settings





def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
        
    else :
         form = CustomUserCreationForm()
    return render (request, 'Accounts/register.html', {'form': form} )


