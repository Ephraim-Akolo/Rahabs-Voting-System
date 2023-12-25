import cv2, face_recognition
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.http.response import JsonResponse
from django.contrib import messages
from django.http import Http404
from .emailing import send_otp
from .cv import face_in_frame
from . import models, forms

# Create your views here.



def home(request):
    context = {}
    options = ['Date', "State", "Party"]
    selected = 1
    if request.method == "POST" and 'filter' in request.POST:
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
        form = forms.VotePostForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(models.User, vin=form.cleaned_data['voterID'])
            cand = get_object_or_404(models.Candidate, name__iexact=form.cleaned_data['candidateName'], party__name = form.cleaned_data['partyName'])
            voted = models.Election.objects.filter(user=user)
            if user.check_password(form.cleaned_data['password']) and not voted:
                accred = models.Accreditation.objects.create(user=user, candidate = cand)
                return render(request, 'website/webCam.html', context={'accred': accred})
        messages.add_message(request, messages.ERROR, "Had problems validating your submitted details!" if not voted else "You have already voted the Candidate of your choice!")
        # messages.warning(request, "Verify all details are correct.")
        return redirect('vote')
    context = {}
    candidates = models.Candidate.objects.all()
    context['candidates'] = candidates
    return render(request, "website/vote.html", context=context)


def facial_auth(request):
    if request.method != 'POST':
        return redirect('vote')
    assert request.FILES
    form = forms.UpdateImageForm(request.POST, request.FILES)
    if not form.is_valid():
        print("image not valid", form.error_class, form.errors)
        return redirect('vote')
    #TODO: FACE ID
    form.save()
    instance: models.Accreditation = form.instance
    print(instance.image.path, instance.user.image)
    # image1, image2 = cv2.imread(instance.user.image.path), cv2.imread(instance.image.path)
    image1 = face_recognition.load_image_file(instance.user.image.path)
    image2 = face_recognition.load_image_file(instance.image.path)
    image1_encodings = face_recognition.face_encodings(image1)
    image2_encodings = face_recognition.face_encodings(image2)
    if not len(image1_encodings):
        messages.error(request, f"Could not fetch image from {instance.user.image.path}!")
        return JsonResponse({'success': False}) 
    if not len(image2_encodings):
        messages.error(request, f"Could not your face in the image! {instance.image.path}!")
        return JsonResponse({'success': False}) 
    results = face_recognition.compare_faces([image1_encodings[0]], image2_encodings[0], tolerance=.4)
    print(results)
    if not results[0]:
        messages.error(request, f"Authorization Failed. Facial features mismatch!")
        return JsonResponse({'success': False})

    _otp, _otp_obj = models.OTP.generate_otp(instance)
    sent, r = send_otp(instance.user.email, _otp)
    if not sent:
        _otp_obj.delete()
        messages.error(request, f"could not send mail: {r}")
        return JsonResponse({'success': True, 'url': request.build_absolute_uri(reverse('vote')),})
    messages.info(request, 'Image has been accepted and authorized!')
    data = {'success': True, 'url': request.build_absolute_uri(reverse('verify')),}
    return JsonResponse(data)
    

def otp_verify(request):
    if request.method != 'POST':
        return render(request, 'website/otp.html')
    form = forms.OTPForm(request.POST)
    if not form.is_valid():
        return redirect('vote')
    otp = f"{form.cleaned_data['first']}{form.cleaned_data['second']}{form.cleaned_data['third']}{form.cleaned_data['fourth']}{form.cleaned_data['fifth']}"
    accred = get_object_or_404(models.Accreditation, otp__otp=otp)
    context = {}
    if accred.otp.is_valid():
        _voted = models.Election.objects.create(user=accred.user, candidate=accred.candidate)
        context['display_message'] = f'{_voted.user.username} Vote Casted for {_voted.candidate.name} Successfully!'
        context['color'] = 'green'
    else:
        context['color'] = 'red'
        context['display_message'] = ' OTP Verification Failed!'
    return render(request, 'website/success_page.html', context=context)


def recover_password(request):
    if request.method == "POST":
        form = forms.EmailForm(request.POST)
        if form.is_valid():
            user = get_object_or_404(models.User, email=form.cleaned_data['email'])
            _otp, _otp_obj = models.OTP.generate_otp(user)
            sent, r = send_otp(user.email, _otp)
            if sent: 
                messages.info(request, "An OTP has been sent to your mail!")
                return render(request, 'website/recover_password.html', context={"recover_pasword": True})
            messages.error(request, f"could not send mail: {r}")
            print(r)
            _otp_obj.delete()
            return redirect('recover')
        form = forms.RecoverPasswordForm(request.POST)
        if form.is_valid():
            otp = get_object_or_404(models.OTP, otp=form.cleaned_data['otp'])
            if otp.is_valid():
                user = otp.user
                user.set_password(form.cleaned_data['password'])
                otp.delete()
                user.save()
                messages.info(request, "password changed Successfully!")
                return redirect('home')
            else:
                otp.delete()
                messages.error(request, "OTP not valid or expired!")
        else:
            messages.error(request, "form validation failed!")
            messages.info(request, "Verify passwords fields!")
    return render(request, "website/recover.html")

