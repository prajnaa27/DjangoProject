from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.http import JsonResponse
from .models import Item,Payment
import razorpay
from django.template import loader
from .forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages

# Create your views here.
def hello(request):
    return HttpResponse("Hello world")

def home(request):
    return render(request, 'food/home.html')

def menu(request):
    item_list = Item.objects.all()
    cart = request.session.get('cart', {})
    
    # Process items to include current quantities
    for item in item_list:
        item.current_quantity = cart.get(item.item_name, {}).get('quantity', 0)
    
    context = {
        'items': item_list,
    }
    return render(request, 'food/menu.html', context)



def add_to_cart(request, item_name):
    if request.method == 'POST':
        try:
            cart = request.session.get('cart', {})
            
            price_raw = request.POST.get('price')
            if not price_raw:
                return JsonResponse({'status': 'error', 'message': 'Missing price'}, status=400)

            item_price = float(price_raw)

            # Decode URL-encoded name like 'Neer%20Dosa' → 'Neer Dosa'
            # item_name = unquote(item_name)

            if item_name in cart:
                cart[item_name]['quantity'] += 1
            else:
                cart[item_name] = {'quantity': 1, 'price': item_price}

            request.session['cart'] = cart

            return JsonResponse({
                'status': 'success',
                'cart': cart,
                'quantity': cart[item_name]['quantity']
            })

        except ValueError as ve:
            return JsonResponse({'status': 'error', 'message': f'Invalid price: {ve}'}, status=400)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

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

def initiate_payment(request):
    if request.method == 'POST':
        # 1. Extract form data
        name = request.POST.get('customer_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        amount = int(request.POST.get('amount')) 

        # 2. Create Razorpay client
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        # 3. Create Razorpay order
        razorpay_order = client.order.create({
            'amount': amount,
            'currency': 'INR',
            'receipt': f'receipt_{phone}',
            'payment_capture': 1
        })

        # 4. Save Payment record in DB
        payment = Payment.objects.create(
            order_id=razorpay_order['id'],
            amount=amount,
            status='created',
            customer_name=name,
            email=email,
            phone=phone,
            address=address
        )

        # 5. Pass data to Razorpay modal template
        return render(request, 'razorpay_payment.html', {
            'order_id': razorpay_order['id'],
            'razorpay_key_id': settings.RAZORPAY_KEY_ID,
            'amount': amount,
            'payment': payment
        })


def upi_checkout(request):
    if request.method == 'POST':
        name = request.POST.get('customer_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        amount = float(request.POST.get('amount'))

        # Create order manually
        payment = Payment.objects.create(
            order_id=f"manual_{phone}_{Payment.objects.count()+1}",
            payment_id="",
            amount=amount,
            status="created",
            customer_name=name,
            email=email,
            phone=phone,
            address=address
        )


        
        return render(request, 'food/show_qr.html', {
            'payment': payment,
            'amount_display': f"{amount}"
        })
    
def mark_paid(request, payment_id):
    payment = get_object_or_404(Payment, id=payment_id)
    if request.method == 'POST':
        payment.status = 'paid'
        payment.payment_id = 'manual-upi-success'
        payment.save()

        if 'cart' in request.session:
            del request.session['cart']
            
        return render(request, 'food/thank_you.html', {'payment': payment})
       
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

