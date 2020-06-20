from django.shortcuts import render, get_object_or_404
from .models import CV
from .forms import CVForm

from django.shortcuts import redirect
# Create your views here.
def cv(request):
    cv = get_object_or_404(CV)
    return render(request, 'cv/cv.html', {'cv': cv})
def cv_edit(request):
    cv = get_object_or_404(CV)
    if request.method == "POST":
        form = CVForm(request.POST, instance=cv)
        if form.is_valid():
            cv = form.save(commit=False)
            cv.author = request.user
            cv.save()
            return redirect('cv')
    else:
        form = CVForm(instance=cv)
    return render(request, 'cv/cv_edit.html', {'form': form})
