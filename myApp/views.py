import datetime
import json
from django.http.response import JsonResponse
from django.shortcuts import redirect, render

# My Imports
from .models import Product, Cart, Tag, Product_Cart
from django.core.mail import send_mail
from datetime import date


# Create your views here.
def home(request):

    # Check if browser exists
    if not request.session.exists(request.session.session_key):
        request.session.save()

    browser_key = request.session.session_key

    # Filter Cart form db
    if Cart.objects.filter(cart_id=browser_key):
        items = Product_Cart.objects.filter(cart=browser_key)
        total_item = 0
        for item in items:
            total_item += item.quantity

    else:
        # Browser is not exist yet
        total_item = ''

    try:
        proteinTag = Tag.objects.get(label='Protein')
        proteinList = Product.objects.filter(label=proteinTag)

        preWorkoutTag = Tag.objects.get(label='PreWorkout')
        preWorkoutList = Product.objects.filter(label=preWorkoutTag)

        equipmentTag = Tag.objects.get(label='Equipment')
        equipmentList = Product.objects.filter(label=equipmentTag)

    except:
        proteinList = None
        preWorkoutList = None
        equipmentList = None

    context = {
        'proteinList': list(proteinList),
        'preWorkoutList': list(preWorkoutList),
        'equipmentList': list(equipmentList),
        'total_item': total_item
    }

    return render(request, 'home.html', context)


def add_to_cart(request):

    # Checking for ajax request only
    if request.is_ajax():

        # geting products id
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)

        # Cheking if the browser already exist
        if not request.session.exists(request.session.session_key):
            request.session.save()

        browser_key = request.session.session_key

        # looking for the browser cart
        if not Cart.objects.filter(cart_id=browser_key):
            cart = Cart.objects.create(cart_id=browser_key)

        cart = Cart.objects.get(cart_id=browser_key)

        item_found = False

        # loop through products in cart
        for p in cart.products.all():
            # check product is exists in cart
            if p == product:
                # update quantity of that product
                item = Product_Cart.objects.get(product=product, cart=cart)
                item.quantity += 1
                item.date_added = date.today()
                item_found = True
                item.save()
                break

        # if item does not fond in cart
        if not item_found:
            # add new product browser cart
            cart.products.add(product, through_defaults={
                'quantity': '1', 'date_added': date.today})

        # adding checkout total
        cart.checkout_total += product.price

        # publishing to the site
        items = Product_Cart.objects.filter(cart=cart)
        total_item = 0
        for item in items:
            total_item += item.quantity

        cart.save()

        return JsonResponse({'total_item': total_item}, status=200)


def sendMeassage(request):

    if request.method == "POST" and request.is_ajax():
        # get contact information
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        description = request.POST.get('description')
        # get today's date
        date_submitted = datetime.datetime.now()

        try:
            send_mail("HIT_HARD NEW MESSAGE",
                      f"You have received new form from HIT-HARD.\n\nName: {name}\nPhone: {phone}\nEmail: {email}\nDescription:\n{description}\n\nDate submitted: {date_submitted}", "noreply.hithard@gmail.com", ['***************'])

            send_mail("HIT-HARD FORM SENT",
                      f"Dear {name},\n\nWe have received your form. After reviewing your form, We will contact you shortly to a phone: {phone} or an email: {email} .\n\nDo not reply to this message. \n\n\nThank you,\nHIT-HARD.\n\nDate submitted: {date_submitted}", "dpp4846@gmail.com", [email])
            return JsonResponse({'message': "✅ Thank you for submitting. You will receive an email from us. :)"}, status=200)

        except:

            return JsonResponse(
                {'message': "❌ An error occur while receiving your form. Please refresh the page and try again!, You may still receive email from us, in that case you do not have to take any further acction :)"}, status=200)

    return redirect('home')


def cart(request):

    if not request.session.exists(request.session.session_key):
        request.session.save()

    browser_key = request.session.session_key

    if Cart.objects.filter(cart_id=browser_key):

        cart = Product_Cart.objects.filter(cart=browser_key)
        total_item = 0
        checkout_total = (Cart.objects.get(cart_id=browser_key)).checkout_total

        for item in cart:
            total_item += item.quantity

    else:
        total_item = ''
        checkout_total = ''
        cart = None

    context = {
        'cart': cart,
        'total_item': total_item,
        'checkout_total': checkout_total

    }

    return render(request, 'cart.html', context)


def delete_item(request):

    if request.is_ajax():
        # remvoe product
        product_id = request.GET.get('product_id')
        product = Product.objects.get(id=product_id)
        cart = Cart.objects.get(cart_id=request.session.session_key)
        item = Product_Cart.objects.filter(cart=cart, product=product_id)
        i = 0
        while i < (item[0].quantity):
            cart.checkout_total -= product.price
            i += 1

        cart.save()
        item[0].delete()
    return JsonResponse({'done': 'done'}, status=200)


def order_submit(request):

    if request.is_ajax():

        # List of products that can be submitted ltr into email
        product_list = []
        list_str = ""
        total_amount = 0

        # get email
        user_email = request.POST.get('email')

        # get cart using session key
        cart = Cart.objects.get(cart_id=request.session.session_key)

        # get all products from cart
        products = Product_Cart.objects.filter(cart=cart)

        # Adding all product to email list
        for item in products:
            product_list.append(f"Product ID: {item.product.id}")
            product_list.append(f"name: {item.product.name}")
            product_list.append(f"description: {item.product.description}")
            product_list.append(f"quantity: {item.quantity}")
            product_list.append(f"Price: {item.product.price}\n")

        for p in product_list:
            list_str += f"\n{p}"

        total_amount = cart.checkout_total

        send_mail("Order successfully proccessed",
                  f"Dear {user_email},\n\nYour order has been successfully proccessed. Thank you for ordering with us!\n\nHere is your products list:\n\n{list_str}\n__________________________\nTotal amount: ${total_amount}\n__________________________\n\nNOTE: This website is for self educations only. \nHere you did anything will not be applied in real world or You have not actually purchased anything.\n\nThank you for trying out my website,\nDeep Parmar.", "dpp4846@gmail.com", [user_email])

        cart.delete()

        return JsonResponse({'done': 'done'}, status=200)
