from django.shortcuts import render
from .forms import cheque_form
import boto3
from .models import upload_cheque
# Create your views here.
def index(request):
    if request.method == 'POST':
        form = cheque_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return render(request, 'index.html', {'form':form})
    form = cheque_form()
    model = upload_cheque.objects.all()

    
    return render(request, 'index.html', {'form':form, 'model':model})