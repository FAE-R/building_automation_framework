from django.shortcuts import render
from .models import Feedback

def home(request):
    feedbacks = Feedback.objects.all()
    return render(request, 'home.html', {'feedbacks': feedbacks})