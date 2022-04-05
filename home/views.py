from multiprocessing import context
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.urls import is_valid_path
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from account.models import Customer
from home.models import Category, Product
from home.forms import PostProductForm, EditProductForm
from django.contrib import messages
from django.http import HttpResponseRedirect

# category
context={}
cats_menu=Category.objects.all()
context['cats_menu']=cats_menu

# Create your views here.
def homeView(request):
    return render(request,'home/index.html', context)



def search(request):
    return render(request,'home/index.html')

# category

def add_category(request):
    return render(request,'home/index.html')

def category_details(request,cats):
    return render(request,'home/index.html')

def all_category_details(request):
    cats_menu=Category.objects.all()
    context={'cats_menu':cats_menu}
    return HttpResponseRedirect(request.path_info,context)

def update_category(request,cats):
    return render(request,'home/index.html')

def delete_category(request,cats):
    return render(request,'home/index.html')





# Product
def add_product(request):
    if request.method=='POST':
        form=PostProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "your Product has successfully added")
            return redirect('all_product_details')
        else:
            messages.success(request, "Form is Not Valid")
    else:
        form=PostProductForm()
    context['form']= form
    return render(request,'product/add_product.html', context)


def product_info(request,pk):
    product=Product.objects.get(id=pk)
    context={'product':product}
    return render(request,'product/index.html', context)

# def product_details(request,pk):
#     product_id=request.POST.get('product_id')
#     product_details=Product.objects.all
#     return render(request,'product/product_details.html',product_id)

class ProductDetailsView(DetailView):
    model=Product
    template_name='product/product_details.html'

def all_product_details(request):
    context["all_products"] = Product.objects.all()
    return render(request,'product/view_all_product.html', context)


def customer_product_list(request,pk):
    pk=Customer.objects.get(user=request.user)
    # print(pk)
    all_posted_product=Product.objects.filter(author=pk).order_by('created_at')
    context['all_posted_product']=all_posted_product
    return render(request,'product/customer_product_list.html',context)


class delete_product(DeleteView):
    model=Product
    template_name='product/delete_product.html'
    
    def get_success_url(self):
        pk=Customer.objects.get(user=self.request.user)
        # print(pk)
        return reverse( 'customer_product_list', kwargs={'pk': pk.id})

class update_product(UpdateView):
    model=Product
    form_class=EditProductForm
    template_name='product/update_product.html'
    
    def get_success_url(self):
        pk=Customer.objects.get(user=self.request.user)
        # print(pk)
        return reverse( 'customer_product_list', kwargs={'pk': pk.id})




def rating_product(request,pk):
    return render(request,'home/index.html')

# Comments
def add_comment(request):
    return render(request,'home/index.html')

def comment_details(request,pk):
    return render(request,'home/index.html')

def all_comment_details(request):
    return render(request,'home/index.html')

def update_comment(request,pk):
    return render(request,'home/index.html')

def delete_comment(request,pk):
    return render(request,'home/index.html')

# Auction
def add_auction(request,pk):
    product=Product.objects.get(id=pk)
    return render(request,'product/view_all_auction_product.html',context)

def update_auction(request, pk):
    pass

def delete_auction(request, pk):
    pass

def bid_auction(request, pk):
    pass

# Customer product related functionality
def bid_details(request):
    return render(request,'product/bid_details.html',context)


def company_rating(request, pk):
    pass