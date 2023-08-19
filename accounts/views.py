import base64
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import UserProfile, user_current_location
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        profile_picture = request.FILES.get('profile_picture')

        user = User.objects.create_user(username=username, password=password)
        
        if profile_picture:
            user_profile = UserProfile.objects.create(user=user, profile_picture=profile_picture)
        else:
            user_profile = UserProfile.objects.create(user=user)

        messages.success(request, 'Registration successful. You can now log in.')
        return redirect('login')  # Redirect to your login page or wherever you want

    return render(request, 'accounts/register.html')

from django.contrib import messages
from django.shortcuts import render, redirect
import base64
import numpy as np
import cv2
import face_recognition
from django.contrib.auth import authenticate, login

from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import UserProfile, user_current_location
import base64
import numpy as np
import cv2
import face_recognition

def login_with_camera(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            location = request.POST.get('current_location')

            user = authenticate(request, username=username, password=password)

            if user:
                try:
                    profile = user.userprofile
                except UserProfile.DoesNotExist:
                    profile = None

                if profile and profile.profile_picture:
                    saved_profile_picture = profile.profile_picture.path

                    captured_image_base64 = request.POST.get('captured_image')
                    captured_image_data = base64.b64decode(captured_image_base64.split(',')[1])
                    captured_image = cv2.imdecode(np.fromstring(captured_image_data, dtype=np.uint8), cv2.IMREAD_COLOR)

                    saved_face = face_recognition.load_image_file(saved_profile_picture)
                    captured_face = captured_image

                    saved_face_encoding = face_recognition.face_encodings(saved_face)[0]
                    captured_face_encoding = face_recognition.face_encodings(captured_face)[0]

                    results = face_recognition.compare_faces([saved_face_encoding], captured_face_encoding)
                    if results[0]:
                        login(request, user)

                        user_profile, created = user_current_location.objects.get_or_create(user=profile)
                        user_profile.current_location = location
                        user_profile.save()

                        return redirect('dashboard')

                messages.error(request, 'Face verification failed. Please try again.')

        except IndexError:
            messages.error(request, 'Place your face correctly and try again.')

    return render(request, 'accounts/login.html')






from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    current_location = None

    if request.user.is_authenticated:
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            user_location = user_current_location.objects.get(user=user_profile)
            current_location = user_location.current_location
        except (UserProfile.DoesNotExist, user_current_location.DoesNotExist):
            pass

    context = {
        'current_location': current_location
    }
    return render(request, 'accounts/dashboard.html', context)



from django.shortcuts import render
from django.http import JsonResponse
from geopy.geocoders import Nominatim

def get_location_name(request):
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        location_name = get_actual_location_name(latitude, longitude)
        return JsonResponse({'location_name': location_name})
    
    return render(request, 'get_location.html')

def get_actual_location_name(latitude, longitude):
    geolocator = Nominatim(user_agent='my_geocoder')
    location = geolocator.reverse((latitude, longitude), exactly_one=True)
    if location:
        return location.raw['display_name']
    return None

