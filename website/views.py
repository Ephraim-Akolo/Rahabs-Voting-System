from django.shortcuts import render
from django.http import Http404
from . import models

# Create your views here.



def home(request):
    context = {}
    options = ['Date', "State", "Party"]
    selected = 1
    if request.method == "POST" and 'filter' in request.POST:
        # print("KKKKKKKKK", request.POST)
        if request.POST.get('filter').lower()=='date':
            election = models.Election.objects.all().order_by('-date')
        elif request.POST.get('filter').lower()=='state':
            election = models.Election.objects.all().order_by('user__lga__state__name')
            selected = 2
        elif request.POST.get('filter').lower()=='party':
            election = models.Election.objects.all().order_by('candidate__party__name')
            selected = 3
    else:
        election = models.Election.objects.all().order_by('-date')

    context['election'] = election
    context['options'] = options
    context['selected'] = selected
    return render(request, 'website/home.html', context=context)


def vote(request):
    if request.method == 'POST':
        print(request.POST)
        return render(request, 'website/webCam.html')
    context = {}
    candidates = models.Candidate.objects.all()
    context['candidates'] = candidates
    return render(request, "website/vote.html", context=context)


def facial_auth(request):
    if request.method == 'POST':
        # print(request.POST)
        return render(request, 'website/otp.html')
    
def otp_verify(request):
    print("dkjjjjjjjjjjjjjjjj")
    if request.method == 'POST':
        print("otp_verify", request.POST)
        return render(request, 'website/success_page.html')

