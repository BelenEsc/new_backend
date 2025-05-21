from django.shortcuts import render

def home(request):
    return render(request, 'request_form.html', {})
