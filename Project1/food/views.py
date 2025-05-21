from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string

from .models import Item
from django.template import loader
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

def home(request):
    item_list=Item.objects.all()
    template=loader.get_template('food/home.html')
    context={
        'items':item_list
    }
    return render(request,'food/home.html',context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            contact_data = form.save()  # Save to DB

            # Send Email
            subject = f"New Contact from {contact_data.name}"

            text_body = f"Message:\n{contact_data.message}\n\nFrom: {contact_data.name} <{contact_data.email}>"

            html_body = render_to_string('food/email.html', {
                'name': contact_data.name,
                'email': contact_data.email,
                'message': contact_data.message,
            })

            send_mail(
                subject,
                text_body,
                contact_data.email,
                ['prajnas702@gmail.com'],
                fail_silently=False,
                html_message=html_body
            )


            messages.success(request, "Your message has been sent successfully!")
            return redirect('contact')
        else:
            messages.error(request, "Please provide valid details.")
    else:
        form = ContactForm()
    return render(request, 'food/contact.html', {'form': form})