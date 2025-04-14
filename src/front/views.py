from django.shortcuts import render


def index(request):
    return render(request, 'front/index.html')

def about(request):
    return render(request, 'front/about.html')

def contact(request):
    return render(request, 'front/contact.html')

def course_details(request):
    return render(request, 'front/course_details.html')

def courses(request):
    return render(request, 'front/courses.html')

def events(request):
    return render(request, 'front/events.html')

def pricing(request):
    return render(request, 'front/pricing.html')

def starter_page(request):
    return render(request, 'front/starter_page.html')

def trainers(request):
    return render(request, 'front/trainers.html')
