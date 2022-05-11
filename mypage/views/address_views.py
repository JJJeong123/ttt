import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime

from config.models import Address, Member

class AddressView(LoginRequiredMixin, View):
    '''
    배송지 관리
    '''
    def get(self, request: HttpRequest):
        context={}
        context['addresses']=list(Address.objects.filter(deleteflag='0', member__user=request.user).order_by('-created_at')\
                                  .values('ad_name', 'code', 'ad_detail', 'id'))
        
        return render(request, 'address.html', context)

    def post(self, request:HttpRequest):
        context={}
        request.POST=json.loads(request.body)

        code=request.POST.get('code')
        ad_detail=request.POST.get('ad_detail')

        Address.objects.create(
            deleteflag='0',
            code=code,
            ad_detail=ad_detail,
            member=Member.objects.get(user=request.user),
        )

        context['success']=True

        return JsonResponse(context, content_type='application/json')

    def put(self, request:HttpRequest):
        context={}
        request.PUT=json.loads(request.body)

        id=request.PUT.get('id')
        ad_name=request.PUT.get('ad_name')

        Address.objects.filter(id=id).update(
            ad_name=ad_name
        )
      
        context['success']=True

        return JsonResponse(context, content_type='application/json')
    
    def delete(self, request:HttpRequest):
        context={}
        request.DELETE=json.loads(request.body)

        id=request.DELETE.get('id')

        Address.objects.filter(id=id).update(
            deleteflag='1',
            deleted_at=datetime.now(),
        )
      
        context['success']=True

        return JsonResponse(context, content_type='application/json')


class AddressModalView(LoginRequiredMixin, View):
    '''
    배송지 관리

    배송지 수정 모달에 들어갈 정보를 받아옵니다
    '''
    def get(self, request: HttpRequest):
        context={}
        id=request.GET.get('id')

        context['address']=list(Address.objects.filter(id=id).values('id', 'ad_detail', 'ad_name'))[0]
        context['success']=True

        return JsonResponse(context, content_type='application/json')
