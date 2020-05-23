from django.shortcuts import render, get_object_or_404
from .models import CV
# Create your views here.
def cv(request):
    c = get_object_or_404(CV)
    return render(request, 'cv/cv.html', {'cv': c})
