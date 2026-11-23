from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .models import ContactMessage, ProfileInfo, Project, Service


def services_view(request):
    profile = ProfileInfo.objects.first()
    services = Service.objects.filter(is_active=True)
    context = {
        'profile': profile,
        'services': services,
    }
    return render(request, 'portfolio/services.html', context)


def projects_view(request):
    profile = ProfileInfo.objects.first()
    selected_category = request.GET.get('category', 'all')

    projects = Project.objects.prefetch_related('images')
    if selected_category and selected_category != 'all':
        projects = projects.filter(category=selected_category)

    context = {
        'profile': profile,
        'projects': projects,
        'categories': Project.CATEGORY_CHOICES,
        'selected_category': selected_category,
    }
    return render(request, 'portfolio/projects.html', context)


def project_detail_view(request, slug):
    profile = ProfileInfo.objects.first()
    project = get_object_or_404(Project.objects.prefetch_related('images'), slug=slug)
    context = {
        'profile': profile,
        'project': project,
    }
    return render(request, 'portfolio/project_detail.html', context)


def about_contact_view(request):
    profile = ProfileInfo.objects.first()

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()

        if name and email and subject and message_text:
            ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text,
            )
            messages.success(request, 'تم إرسال رسالتك بنجاح! سأتواصل معك في أقرب وقت.')
            return redirect('portfolio:about_contact')
        else:
            messages.error(request, 'يرجى تعبئة جميع الحقول المطلوبة قبل الإرسال.')

    context = {
        'profile': profile,
    }
    return render(request, 'portfolio/about_contact.html', context)