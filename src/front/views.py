from django.shortcuts import render, redirect
from django.contrib import messages


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

def trainers(request):
    return render(request, 'front/trainers.html')



def valider_paiement(request):
    if request.method == 'POST':
        mode = request.POST.get('mode_paiement')

        if mode == 'orange':
            phone = request.POST.get('orange_phone')
            code = request.POST.get('orange_code')
            # Traitement Orange Money
        elif mode == 'mtn':
            phone = request.POST.get('mtn_phone')
            code = request.POST.get('mtn_code')
            # Traitement MTN Money
        elif mode == 'card':
            number = request.POST.get('card_number')
            name = request.POST.get('card_name')
            expiry = request.POST.get('card_expiry')
            cvv = request.POST.get('card_cvv')
            # Traitement Carte Bancaire

        # Logique commune après paiement
        return redirect('confirmation_paiement')
