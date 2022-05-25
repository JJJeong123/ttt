import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.db.models import IntegerField
from django.db.models.functions import Cast
from datetime import datetime, timedelta

from config.models import Product, Order, OrderProduct, Address, Member, Cart,  CartProduct, Coupon


class CheckoutView(LoginRequiredMixin, View):
    '''
    결제창
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}

        context['memname'] = list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0]
        context['cart'] = CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()

        return render(request, 'checkout.html', context)
    
    def post(self, request: HttpRequest):
        context={}
        context['success']=False
        request.POST=json.loads(request.body)

        type=request.POST.get('type')
        address_id=request.POST.get('address')
        products=request.POST.get('products')
        name=request.POST.get('name')
        call=request.POST.get('call')
        coupons=request.POST.get('coupons')
        discount_amount=request.POST.get('discount_amount')

        try:
            address=Address.objects.get(id=address_id)
        except Address.DoesNotExist:
            address = None

        total_price=getPrice(products)
        order_no=getOrderNo()

        # for delivery and short-delivery
        if(address is not None):
            Order.objects.create(
                deleteflag='0',
                address=address.ad_detail,
                code=address.code,
                name=address.name,
                call=address.call,
                status='0',
                date=datetime.now().strftime("%Y-%m-%d"),
                type=type,
                total_price=total_price-discount_amount,
                order_no=order_no,
                member=Member.objects.get(user=request.user),
            )
            order={
                'no': order_no,
                'type': type,
                'call': call,
                'name': name,
                'address': address.ad_detail,
            }

        # for drivethru and pickup
        else:
            Order.objects.create(
                deleteflag='0',
                name=name,
                call=call,
                status='0',
                date=datetime.now().strftime("%Y-%m-%d"),
                type=type,
                total_price=total_price,
                order_no=order_no,
                member=Member.objects.get(user=request.user),
              )
            order={
                'no': order_no,
                'type': type,
                'call': call,
                'name': name,
                'address': "",
            }

        for product in products:
            OrderProduct.objects.create(
                deleteflag='0',
                amount=product.get('amount'),
                order=Order.objects.get(order_no=order_no),
                product=Product.objects.get(id=product.get('id')),
                status='0',
                review_flag='0',
            )
        discount(coupons, request.user)
        deleteFromCart(request.user.id, products)
        
        context['success']=True
        context['order']=order

        return JsonResponse(context, content_type='application/json')

class CheckoutConfirmView(LoginRequiredMixin, View):
    '''
    주문완료 후 확인창
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}

        return render(request, 'checkout_confirm.html', context)
    
class AddressView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}

        try:
            context['addresses']=list(Address.objects.filter(deleteflag='0', member__user=request.user).order_by('-created_at')\
                          .values('ad_name', 'code', 'ad_detail', 'id', 'name', 'call'))

            context['success']=True
        
        except Exception as e:
            context['success']=False

        return JsonResponse(context, content_type='application/json')

class CouponView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        try:
            context['coupons']=list(Coupon.objects.filter(deleteflag='0', member__user=request.user).order_by('-created_at')\
                          .values('rate', 'product__id', 'product__name', 'id'))

            context['success']=True
        
        except Exception as e:
            context['success']=False

        return JsonResponse(context, content_type='application/json')

class OrderHistoryView(LoginRequiredMixin, View):
    '''
    주문내역
    '''
    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        orders=[]
        products=[]
        num=[] # 주문 당 상품 개수
        amount=[] # 주문의 첫 번째 상품 개수
        first_item=[] # 주문의 첫 번째 상품 정보

        # user's orders
        orders=list(Order.objects.filter(deleteflag='0', member__user_id=request.user.id).order_by('-created_at').values('id', 'order_no', 'status', 'created_at', 'total_price'))

        # products of each 
        for order in orders:
            product=list(OrderProduct.objects.filter(deleteflag='0', order=order['id']).values('product__id', 'product__price', 'amount', 'product__name'))
            products.append(product)
            first_item.append(Product.objects.get(id=product[0]['product__id']))
            num.append(product[0]['amount'])

        for product in products:
            amount.append(len(product)-1)

        context={
            'first_item': first_item,
            'amount': amount,
            'orders': orders,
            'num': num,
            'memname': list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0],
            'cart': CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()
        }
        return render(request, 'order_history.html', context)

    def delete(self, request:HttpRequest):
        context={}
        request.DELETE = json.loads(request.body)

        order_id=request.DELETE.get('order_id')

        try:
            Order.objects.filter(id=order_id).update(
                status='10',
                updated_at=datetime.now(),
            )
            ids=list(OrderProduct.objects.filter(order__id=order_id).values_list('id', flat=True))
            
            for id in ids:
                OrderProduct.objects.filter(id=id).update(
                    status='10',
                    updated_at=datetime.now(),
                )

            context['success']=True
        
        except Exception as e:
            context['success']=False


        return JsonResponse(context, content_type='application/json')

class OrderDetailView(LoginRequiredMixin, View):
    '''
    주문내역 상세
    '''

    def get(self, request: HttpRequest, *args, **kwargs):
        context={}
        main_imgs=[]

        id = kwargs.get('id')

        order=Order.objects.get(id=id)
        products=list(OrderProduct.objects.filter(order=id).values('product__id', 'product__name', 'amount').annotate(total=Cast(F('amount') * F('product__price'), IntegerField())))

        for p in products:
            main_imgs.append(Product.objects.get(id=p['product__id']))

        context={
            'order': order,
            'products': products,
            'items': main_imgs,
            'memname':list(Member.objects.filter(user_id=request.user.id).values_list('mem_name', flat=True))[0],
            'cart': CartProduct.objects.filter(cart__member__user=request.user, deleteflag='0').count()
        }

        return render(request, 'order_detail.html',  context)

# Get total price of order
def getPrice(products):
    total_price=0

    for product in products:
        total_price+=int(product.get('price'))
    
    return total_price

# create order_no
def getOrderNo():
    tommorow_date = (datetime.now() + timedelta(days=1)).strftime("%Y%m-%d")
    current_date=datetime.now().strftime("%Y-%m-%d")

    order_cnt=Order.objects.filter(deleteflag='0', date__range=[current_date, tommorow_date]).count()

    return str(datetime.now().strftime("%Y%m%d")+format(order_cnt, '06d'))

def deleteFromCart(user_id, products):
    cart=list(Cart.objects.filter(member__user_id=user_id).values_list('id', flat=True))[0]
    
    for product in products:
        cartproduct=Product.objects.get(id=product.get('id'))

        CartProduct.objects.filter(deleteflag='0', cart=cart, product=cartproduct).update(
            deleteflag='1',
            amount=0,
            deleted_at=datetime.now(),
        )

def discount(coupons, user):
    for coupon in coupons:
        Coupon.objects.filter(deleteflag='0', member__user=user, id=coupon).update(
            deleteflag='1',
            deleted_at=datetime.now(),
        )