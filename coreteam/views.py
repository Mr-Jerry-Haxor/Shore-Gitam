from django.shortcuts import render, HttpResponse , redirect 
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib import messages



@login_required(login_url="/auth/login/google-oauth2/")
def coretasks(request , domain_name):
    if request.user.is_staff:
        if request.user.president:
            if domain_name == "president":
                president_tasks = Task.objects.filter(domain="president").order_by('-due_date')
                dashcontext = {
                    'tasks'  : president_tasks,
                    'domain' : "president"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == "vice_president":
                vice_president_tasks = Task.objects.filter(domain="vice-president").order_by('-due_date')
                dashcontext = {
                    'tasks' : vice_president_tasks,
                    'domain' : "vice_president"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'technology':
                technology_tasks = Task.objects.filter(domain="technology").order_by('-due_date')
                dashcontext = {
                    'tasks'  : technology_tasks,
                    'domain' : "technology"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == "events-cultural":
                events_cultural_tasks = Task.objects.filter(domain="events-cultural").order_by('-due_date')
                dashcontext = {
                    'tasks'  : events_cultural_tasks,
                    'domain' : "events-cultural"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'events-sports':
                events_sports_tasks = Task.objects.filter(domain="events-sports").order_by('-due_date')
                dashcontext = {
                    'tasks'  : events_sports_tasks,
                    'domain' : "events-sports"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'legal':
                legal_tasks = Task.objects.filter(domain="legal").order_by('-due_date')
                dashcontext = {
                    'tasks'  : legal_tasks,
                    'domain' : "legal"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'operations':
                operations_tasks = Task.objects.filter(domain="operations").order_by('-due_date')
                dashcontext = {
                    'tasks'  : operations_tasks,
                    'domain' : "operations"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'marketing':
                marketing_tasks = Task.objects.filter(domain="marketing").order_by('-due_date')
                dashcontext = {
                    'tasks'  : marketing_tasks,
                    'domain' : "marketing"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'sponsorship':
                sponsorship_tasks = Task.objects.filter(domain="sponsorship").order_by('-due_date')
                dashcontext = {
                    'tasks'  : sponsorship_tasks,
                    'domain' : "sponsorship"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == "design":
                design_tasks = Task.objects.filter(domain="design").order_by('-due_date')
                dashcontext = {
                    'tasks'  : design_tasks,
                    'domain' : "design"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'finance':
                finance_tasks = Task.objects.filter(domain="finance").order_by('-due_date')
                dashcontext = {
                    'tasks'  : finance_tasks,
                    'domain' : "finance"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'media':
                media_tasks = Task.objects.filter(domain="media").order_by('-due_date')
                dashcontext = {
                    'tasks'  : media_tasks,
                    'domain' : "media"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'security':
                security_tasks = Task.objects.filter(domain="security").order_by('-due_date')
                dashcontext = {
                    'tasks'  : security_tasks,
                    'domain' : "security"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'hospitality':
                hospitality_tasks = Task.objects.filter(domain="hospitality").order_by('-due_date')
                dashcontext = {
                    'tasks'  : hospitality_tasks,
                    'domain' : "hospitality"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('coretasks')
        elif request.user.vice_president:
            if domain_name == "vice_president":
                vice_president_tasks = Task.objects.filter(domain="vice-president").order_by('-due_date')
                dashcontext = {
                    'tasks' : vice_president_tasks,
                    'domain' : "vice_president"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'technology':
                technology_tasks = Task.objects.filter(domain="technology").order_by('-due_date')
                dashcontext = {
                    'tasks'  : technology_tasks,
                    'domain' : "technology"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == "events-cultural":
                events_cultural_tasks = Task.objects.filter(domain="events-cultural").order_by('-due_date')
                dashcontext = {
                    'tasks'  : events_cultural_tasks,
                    'domain' : "events-cultural"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'events-sports':
                events_sports_tasks = Task.objects.filter(domain="events-sports").order_by('-due_date')
                dashcontext = {
                    'tasks'  : events_sports_tasks,
                    'domain' : "events-sports"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'legal':
                legal_tasks = Task.objects.filter(domain="legal").order_by('-due_date')
                dashcontext = {
                    'tasks'  : legal_tasks,
                    'domain' : "legal"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'operations':
                operations_tasks = Task.objects.filter(domain="operations").order_by('-due_date')
                dashcontext = {
                    'tasks'  : operations_tasks,
                    'domain' : "operations"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'marketing':
                marketing_tasks = Task.objects.filter(domain="marketing").order_by('-due_date')
                dashcontext = {
                    'tasks'  : marketing_tasks,
                    'domain' : "marketing"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'sponsorship':
                sponsorship_tasks = Task.objects.filter(domain="sponsorship").order_by('-due_date')
                dashcontext = {
                    'tasks'  : sponsorship_tasks,
                    'domain' : "sponsorship"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == "design":
                design_tasks = Task.objects.filter(domain="design").order_by('-due_date')
                dashcontext = {
                    'tasks'  : design_tasks,
                    'domain' : "design"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'finance':
                finance_tasks = Task.objects.filter(domain="finance").order_by('-due_date')
                dashcontext = {
                    'tasks'  : finance_tasks,
                    'domain' : "finance"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'media':
                media_tasks = Task.objects.filter(domain="media").order_by('-due_date')
                dashcontext = {
                    'tasks'  : media_tasks,
                    'domain' : "media"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'security':
                security_tasks = Task.objects.filter(domain="security").order_by('-due_date')
                dashcontext = {
                    'tasks'  : security_tasks,
                    'domain' : "security"
                }
                return render(request , 'dashboard.html' , dashcontext)
            elif domain_name == 'hospitality':
                hospitality_tasks = Task.objects.filter(domain="hospitality").order_by('-due_date')
                dashcontext = {
                    'tasks'  : hospitality_tasks,
                    'domain' : "hospitality"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('coretasks')
        elif request.user.technology:
            if domain_name == 'technology':
                technology_tasks = Task.objects.filter(domain="technology").order_by('-due_date')
                dashcontext = {
                    'tasks'  : technology_tasks,
                    'domain' : "technology"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.events_cultural:
            if domain_name == 'events_cultural':
                events_cultural_tasks = Task.objects.filter(domain="events-cultural").order_by('-due_date')
                dashcontext = {
                    'tasks'  : events_cultural_tasks,
                    'domain' : "events_cultural"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.events_sports:
            if domain_name == 'events_sports':
                events_sports_tasks = Task.objects.filter(domain="events-sports").order_by('-due_date')
                dashcontext = {
                    'tasks'  : events_sports_tasks,
                    'domain' : "events_sports"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.legal:
            if domain_name == 'legal':
                legal_tasks = Task.objects.filter(domain="legal").order_by('-due_date')
                dashcontext = {
                    'tasks'  : legal_tasks,
                    'domain' : "legal"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.operations:
            if domain_name == 'operations':
                operations_tasks = Task.objects.filter(domain="operations").order_by('-due_date')
                dashcontext = {
                    'tasks'  : operations_tasks,
                    'domain' : "operations"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.marketing:
            if domain_name == 'marketing':
                marketing_tasks = Task.objects.filter(domain="marketing").order_by('-due_date')
                dashcontext = {
                    'tasks'  : marketing_tasks,
                    'domain' : "marketing"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.sponsorship:
            if domain_name == 'sponsorship':
                sponsorship_tasks = Task.objects.filter(domain="sponsorship").order_by('-due_date')
                dashcontext = {
                    'tasks'  : sponsorship_tasks,
                    'domain' : "sponsorship"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.design:
            if domain_name == 'design':
                design_tasks = Task.objects.filter(domain="design").order_by('-due_date')
                dashcontext = {
                    'tasks'  : design_tasks,
                    'domain' : "design"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.finance:
            if domain_name == 'finance':
                finance_tasks = Task.objects.filter(domain="finance").order_by('-due_date')
                dashcontext = {
                    'tasks'  : finance_tasks,
                    'domain' : "finance"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.media:
            if domain_name == 'media':
                media_tasks = Task.objects.filter(domain="media").order_by('-due_date')
                dashcontext = {
                    'tasks'  : media_tasks,
                    'domain' : "media"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.security:
            if domain_name == 'security':
                security_tasks = Task.objects.filter(domain="security").order_by('-due_date')
                dashcontext = {
                    'tasks'  :  security_tasks,
                    'domain' : "security"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        elif request.user.hospitality:
            if domain_name == 'hospitality':
                hospitality_tasks = Task.objects.filter(domain="hospitality").order_by('-due_date')
                dashcontext = {
                    'tasks'  : hospitality_tasks,
                    'domain' : "hospitality"
                }
                return render(request , 'dashboard.html' , dashcontext)
            else:
                return redirect('corehome')
        else:
            return redirect('index')
    else:
        return redirect('index')


@login_required(login_url="/auth/login/google-oauth2/")
def home(request):
    if request.user.is_staff:
        name = request.user.first_name
        return render(request, 'corehome.html' , {'name': name})
    else:
        return redirect('index')

@login_required(login_url="/auth/login/google-oauth2/")
def createtask(request , domain_name):
    if request.user.is_staff:
        if request.user.president and domain_name == "president" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('president', 'President'),
                    ('vice-president', 'Vice President'),
                    ('technology', 'Technology'),
                    ('events-cultural', 'Events - Cultural'),
                    ('events-sports', 'Events - Sports'),
                    ('legal', 'Legal'),
                    ('operations', 'Operations'),
                    ('marketing', 'Marketing'),
                    ('sponsorship', 'Sponsorship'),
                    ('design', 'Design'),
                    ('finance', 'Finance'),
                    ('media', 'Media'),
                    ('security', 'Security'),
                    ('hospitality', 'Hospitality'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "president"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='president')
        elif request.user.vice_president and domain_name == "vice_president" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('vice-president', 'Vice President'),
                    ('technology', 'Technology'),
                    ('events-cultural', 'Events - Cultural'),
                    ('events-sports', 'Events - Sports'),
                    ('legal', 'Legal'),
                    ('operations', 'Operations'),
                    ('marketing', 'Marketing'),
                    ('sponsorship', 'Sponsorship'),
                    ('design', 'Design'),
                    ('finance', 'Finance'),
                    ('media', 'Media'),
                    ('security', 'Security'),
                    ('hospitality', 'Hospitality'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "vice_president"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='vice_president')
        elif request.user.technology and domain_name == "technology" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('technology', 'Technology'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "technology"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
            
                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks', domain_name='technology')
        elif request.user.events_cultural and domain_name == "events_cultural" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('events-cultural', 'Events - Cultural'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "events-cultural"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='events_cultural')
        elif request.user.events_sports and domain_name == "events_sports" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('events-sports', 'Events - Sports'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "events-sports"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='events_sports')
        elif request.user.legal and domain_name == "legal" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('legal', 'Legal'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "legal"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='legal')
        elif request.user.operations and domain_name == "operations" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('operations', 'Operations'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "operations"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='operations')
        elif request.user.marketing and domain_name == "marketing" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('marketing', 'Marketing'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "marketing"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='marketing')
        elif request.user.sponsorship and domain_name == "sponsorship" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('sponsorship', 'Sponsorship'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "sponsorship"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='sponsorship')
        elif request.user.design and domain_name == "design" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('design', 'Design'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "design"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='design')
        elif request.user.finance and domain_name == "finance" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('finance', 'Finance'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "finance"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='finance')
        elif request.user.media and domain_name == "media" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('media', 'Media'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "media"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='media')
        elif request.user.security and domain_name == "security" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('security', 'Security'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "security"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='security')
        elif request.user.hospitality and domain_name == "hospitality" :
            if request.method == "GET":
                assigned_by = f"{request.user.first_name} {request.user.last_name}"
                DOMAIN_CHOICES = [
                    ('hospitality', 'Hospitality'),
                ]
                context = {
                    'DOMAIN_CHOICES' : DOMAIN_CHOICES,
                    'assigned_by': assigned_by,
                    'domain' : "hospitality"
                }
                return render(request , "createtask.html" ,context)
            else:
                task_title = request.POST.get('task_title')
                domain = request.POST.get('domain')
                description = request.POST.get('description')
                priority = request.POST.get('priority')
                attached_file = request.FILES.get('attached_file')
                due_date = request.POST.get('due_date')
                status = request.POST.get('status')
                assigned_to = request.POST.get('assigned_to')
                assigned_by = request.POST.get('assigned_by')
                advisory = 'advisory' in request.POST  # Checking if the checkbox is checked
                

                task = Task.objects.create(
                    task_title = task_title,
                    domain = domain,
                    description = description,
                    priority = priority,
                    attached_file = attached_file,
                    due_date = due_date,
                    status = status,
                    assigned_to = assigned_to,
                    assigned_by = assigned_by,
                    advisory = advisory
                )      
                messages.success(request, 'Task Created Successfully')        
                return redirect('coretasks' , domain_name='hospitality')
        else:
            return redirect('index')
    else:
        return redirect('index')



@login_required(login_url="/auth/login/google-oauth2/")  
def edit_task(request, domain_name , taskid):
    if request.user.is_staff:
        if request.user.president or request.user.vice_president:
            if domain_name == Task.objects.filter(id=taskid).values()[0]['domain']:
                if request.method == 'GET':
                    taskdetails = Task.objects.filter(id=taskid).values()[0]
                    return render(request, 'edittask.html', {'task' :taskdetails })
                elif request.method == 'POST':
                    now_attached_file = request.FILES.get('attached_file')
                    
                    task = Task.objects.get(id=taskid)
                    
                    if now_attached_file:
                        task.attached_file.delete()  # Delete the old file
                        task.attached_file.save(now_attached_file.name, now_attached_file, save=True)
                    task.task_title = request.POST.get('task_title')
                    task.domain = request.POST.get('domain')
                    task.description = request.POST.get('description')
                    task.priority = request.POST.get('priority')
                    task.due_date = request.POST.get('due_date')
                    task.status = request.POST.get('status')
                    task.assigned_to = request.POST.get('assigned_to')
                    task.assigned_by = request.POST.get('assigned_by')
                    task.advisory = 'advisory' in request.POST

                    task.save()
                    return redirect('coretasks' , domain_name=domain_name)
            else:
                return redirect('corehome')
        else:
            return redirect('corehome')
    else:
        return redirect('index')
    
    
    
    
    
    
    