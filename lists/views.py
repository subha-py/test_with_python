from django.shortcuts import render,redirect
from django.http import HttpResponse
from lists.models import Item,List
# Create your views here.
def home_page(request):
    return render(request,'home.html')

def view_list(request,list_id):
    list_=List.objects.get(id=list_id)
    items=Item.objects.filter(list=list_)
    context={
        'list':list_
    }
    return render(request,'list.html',context)

def new_list(request):
    list_=List.objects.create()
    item=Item.objects.create(text=request.POST.get('item_text',''),list=list_)
    return redirect('/lists/%d/'%(list_.id))

def add_item(request,list_id):
    list_=List.objects.get(id=list_id)
    item=Item.objects.create(text=request.POST.get('item_text',''),list=list_)
    return redirect('/lists/%d/'%(list_.id))