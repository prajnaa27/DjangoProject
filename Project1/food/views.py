from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Item
from django.template import loader
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

#Claude
def home(request):
    item_list = Item.objects.all()
    cart = request.session.get('cart', {})
    
    # Process items to include current quantities
    for item in item_list:
        item.current_quantity = cart.get(item.item_name, {}).get('quantity', 0)
    
    context = {
        'items': item_list,
    }
    return render(request, 'food/home.html', context)
# def home(request):
#     item_list=Item.objects.all()
#     template=loader.get_template('food/home.html')
#     cart = request.session.get('cart', {})
#     cart_quantities = {k: v['quantity'] for k, v in cart.items()} if cart else {}
#     context={
#         'items':item_list,
#         'cart_quantities': cart_quantities,
#     }

    

#     # Pass cart items to template
#     return render(request, 'food/home.html', context)
#     # return render(request,'food/home.html',context)

def add_to_cart(request, item_name):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        item_price = float(request.POST.get('price', 0))

        if item_name in cart:
            cart[item_name]['quantity'] += 1  # Increment quantity
        else:
            cart[item_name] = {'quantity': 1, 'price': item_price}  # Add first time

        request.session['cart'] = cart
        return JsonResponse({
            'status': 'success', 
            'cart': cart, 
            'quantity': cart[item_name]['quantity']
        })


    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)

def decrement_cart(request, item_name):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if item_name in cart:
            cart[item_name]['quantity'] -= 1
            if cart[item_name]['quantity'] <= 0:
                del cart[item_name]
                request.session['cart'] = cart
                return JsonResponse({'status': 'success', 'quantity': 0, 'deleted': True})
            else:
                request.session['cart'] = cart
                return JsonResponse({'status': 'success', 'quantity': cart[item_name]['quantity'], 'deleted': False})
        return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)




def clear_cart(request):
    if request.method == 'POST':
        request.session['cart'] = {}
        request.session.modified = True  # Ensure session is saved
        return JsonResponse({'status': 'success', 'message': 'Cart cleared'})
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)

def remove_from_cart(request, item_name):
    """Completely remove an item from cart regardless of quantity"""
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        if item_name in cart:
            del cart[item_name]
            request.session['cart'] = cart
            return JsonResponse({'status': 'success', 'message': 'Item removed from cart'})
        return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid method'}, status=400)

# def cart(request):
#     cart = request.session.get('cart',{})
#     # total_price = sum(item['quantity'] * item['price'] for item in cart.values())
#     total_price = sum(
#     int(item['quantity']) * float(item['price']) 
#     for item in cart.values()
# )
#     cart_items = []
#     total_price = 0
#     items = cart.get('items', cart)

#     for item_name, details in items.items():
#         quantity = int(details.get('quantity', 0))
#         price = float(details.get('price', 0))
#         subtotal = quantity * price
#         details['subtotal'] = subtotal
#         cart_items.append((item_name, details))
#         total_price += subtotal

#     context={
#         'cart':cart,
#         'total_price':total_price
#     }
    
#     return render(request,'food/cart.html',context)

def cart(request):
    cart = request.session.get('cart', {})
    total_price = 0
    
    # Calculate subtotals and total price
    for item_name, details in cart.items():
        quantity = int(details.get('quantity', 0))
        price = float(details.get('price', 0))
        subtotal = quantity * price
        details['subtotal'] = subtotal
        total_price += subtotal

    context = {
        'cart': cart,
        'total_price': total_price
    }
    
    return render(request, 'food/cart.html', context)


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