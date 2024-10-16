def sign_up(request):
    if request.method == 'POST':
        # Get the form data from the POST request
        name = request.POST.get('name')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        role = request.POST.get('role')
        phone = request.POST.get('phone')  # Get the phone number

        # Basic validation
        if password1 != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('login')  # Redirect to the sign-up page

        # Check if email already exists for Tenant
        if Tenant.objects.filter(tenant_email=email).exists():
            messages.error(request, 'Email already exists as a Tenant.')
            return redirect('login')

        # Check if email already exists for Property Owner
        if PropertyOwner.objects.filter(owner_email=email).exists():
            messages.error(request, 'Email already exists as a Property Owner.')
            return redirect('login')

        # Check if email already exists for Property Manager
        if PropertyManager.objects.filter(manager_email=email).exists():
            messages.error(request, 'Email already exists as a Property Manager.')
            return redirect('login')  # Redirect to the sign-up page

        # Create user based on role
        if role == 'tenant':
            Tenant.objects.create(tenant_name=name, tenant_email=email, tenant_password=password1, contact_number=phone)
        elif role == 'owner':
            PropertyOwner.objects.create(owner_name=name, owner_email=email, owner_password=password1, contact_number=phone)
        elif role == 'manager':
            PropertyManager.objects.create(manager_name=name, manager_email=email, manager_password=password1, contact_number=phone)

        messages.success(request, 'User created successfully! You can now log in.')
        return redirect('login')  # Redirect to login after successful registration

    return render(request, 'login.html')  # Render the signup/login template

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        
        tenant = Tenant.objects.filter(tenant_email=email, tenant_password=password).first()
        if tenant:
            request.session['user_id'] = tenant.id
            request.session['role'] = 'tenant'
            request.session['username'] = tenant.tenant_name  
            return redirect('tenant_homepage')

        owner = PropertyOwner.objects.filter(owner_email=email, owner_password=password).first()
        if owner:
            request.session['user_id'] = owner.id
            request.session['role'] = 'owner'
            request.session['username'] = owner.owner_name  # Store owner's name
            return redirect('owner_homepage')

        # Check login for Property Manager
        manager = PropertyManager.objects.filter(manager_email=email, manager_password=password).first()
        if manager:
            request.session['user_id'] = manager.id
            request.session['role'] = 'manager'
            request.session['username'] = manager.manager_name  # Store manager's name
            return redirect('manager_homepage')

        messages.error(request, 'Invalid email or password.')
        return redirect('login')

    return render(request, 'login.html')  # Render the signup/login template