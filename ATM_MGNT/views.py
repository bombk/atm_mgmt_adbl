from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from .models import ATM , DownReason , ATMDown , Brand , ATMContact , ATMDowntime


@login_required
def home_view(request):
    group = request.user.groups.first()
    return render(request, 'home.html', {'group': group})

@login_required
def atm_list(request):
    atm = ATM.objects.all()
    return render(request, 'atmlist.html', {'atm': atm})

@login_required
def atm_down(request):
    downreason=DownReason.objects.all()
    brands=Brand.objects.all()
    return render(request, 'atmdown/atmdown_form.html', {'downreason':downreason,'brands':brands})
@login_required
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
        atm_down = ATMDown(terminal_branch=atm_branch, terminal_code=terminal_code, atm_brand=atm_brand, down_date=down_date, down_reason_id=down_reason, remarks=remarks)
        atm_down.save()
        return redirect('atmdown')
@login_required
def file_transfer_down(request):
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
            ).values('id', 'terminal_branch', 'terminal_code','atm_brand__name')

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
                if user.is_superuser:
                    return redirect('/admin/')
                else:
                    return redirect('home')
                # Redirect to a success page
            else:
                # Return an invalid response
                return JsonResponse({'error': 'Invalid credentials'}, status=400)
        else:
            # Return an invalid response
            return JsonResponse({'error': 'Invalid credentials'}, status=400)                
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

@login_required
def contact_list(request):
    contacts = ATMContact.objects.all()
    return render(request, 'contact/contact_list.html', {'contacts': contacts})

@login_required
def add_atmdown(request):
    if request.method == 'POST':
        # return  JsonResponse(request.POST)
        terminal_code = request.POST.get('terminal_code')
        
        try:
            atm = ATM.objects.get(terminal_code=terminal_code)
            if atm.atm_online is True:
                 # Save the updated ATM instance
                terminal_branch = request.POST.get('atm_branch')
                terminal_code = request.POST.get('terminal_code')
                atm_brand = request.POST.get('atm_brand')
                start_date = request.POST.get('down_date')
                end_date = request.POST.get('end_date')
                remarks = request.POST.get('remarks')
                atm_down = ATMDowntime(terminal_code=terminal_code, terminal_branch=terminal_branch,atm_brand=atm_brand, start_date=start_date, end_date=end_date, remarks=remarks)
                atm_down.save()

                atm.atm_online = False  # Set atm_online to False
                atm.save()
            else:
                return JsonResponse({'error': 'ATM is already down'}, status=400)
        except ATM.DoesNotExist:
            # Handle the case where the ATM with the given terminal_code does not exist
            print(f"ATM with terminal_code {terminal_code} does not exist.")
        return redirect('add_atmdown')
    return render(request, 'atmdown/atm_down_form.html')


@login_required
def atm_down_list(request):
    atmdown = ATMDowntime.objects.filter(end_date__isnull=True)
    return render(request, 'atmdown/atm_down_list.html', {'atmdown': atmdown})

@login_required
def update_atmdown(request, id):
    atmdown = ATMDowntime.objects.get(id=id)
    atmdown.end_date = request.POST.get('end_date')
    atmdown.save()
    terminal_code=atmdown.terminal_code
    atm=ATM.objects.get(terminal_code=terminal_code)
    atm.atm_online = True
    atm.save()
    return redirect('atm_down_list')

@login_required
def past_atm_down_list(request):
    atmdown = ATMDowntime.objects.filter(end_date__isnull=False)
    return render(request, 'atmdown/past_atm_down.html', {'atmdown': atmdown})
@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout
