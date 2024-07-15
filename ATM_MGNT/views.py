from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import ATM , DownReason , ATMDown , Brand


@login_required
def home_view(request):
    return render(request, 'home.html')

def atm_list(request):
    atm = ATM.objects.all()
    return render(request, 'atmlist.html', {'atm': atm})

def atm_down(request):
    downreason=DownReason.objects.all()
    brands=Brand.objects.all()
    return render(request, 'atmdown/atmdown_form.html', {'downreason':downreason,'brands':brands})

def atm_down_save(request):
    if request.method == 'POST':
        atm_branch = request.POST.get('atm_branch')
        terminal_code = request.POST.get('terminal_code')
        atm_brand = request.POST.get('atm_brand')
        down_date = request.POST.get('down_date')
        down_reason = request.POST.get('down_reason')
        remarks = request.POST.get('remarks')
         # Retrieve the Brand and DownReason instances
        # atm_brand = get_object_or_404(Brand, pk=atm_brand_id)
        # down_reason = get_object_or_404(DownReason, pk=down_reason_id)
        atm_down = ATMDown(terminal_branch=atm_branch, terminal_code=terminal_code, atm_brand_id=atm_brand, down_date=down_date, down_reason_id=down_reason, remarks=remarks)
        atm_down.save()
        return redirect('atmdown')

def atm_down_list(request):
    atmdown = ATMDown.objects.all()
    return render(request, 'atmdown/atmdown_list.html', {'atmdown': atmdown})


@csrf_exempt
def get_atm(request):
    if request.method == 'GET':
        # Print request.POST to debug what data is being received
        print(request.GET.get('atm_branch', ''))
        
        atm_branch = request.GET.get('atm_branch', '')
        if atm_branch.strip():
            # Filter using case-insensitive search on terminal_branch or terminal_code
            get_data = ATM.objects.filter(
                Q(terminal_branch__icontains=atm_branch) |
                Q(terminal_code__icontains=atm_branch)
            ).values('id', 'terminal_branch', 'terminal_code')

            return JsonResponse({'data': list(get_data)})
        else:
            return JsonResponse({'error': 'Empty search string provided'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with your desired redirect URL
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
