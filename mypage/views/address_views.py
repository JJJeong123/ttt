import json
from django.http import HttpRequest, JsonResponse 
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.mixins import LoginRequiredMixin

from config.models import Address, Member

class AddressView(LoginRequiredMixin, View):
    '''
    배송지 관리
    '''
    def get(self, request: HttpRequest):
        context={}
        context['addresses']=list(Address.objects.filter(deleteflag='0', member__user=request.user).order_by('-created_at')\
                                  .values('ad_name', 'code', 'ad_detail'))
        
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
