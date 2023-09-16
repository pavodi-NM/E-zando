from django.shortcuts import render

# Create your views here.

def HomeElectronicStore(request):
    return render(request, 'home-electronics-store.html')

def HomeFashionstore1(request):
    return render(request, 'home-fashion-store-v1.html')

def HomeFashionstore2(request):
    return render(request, 'home-fashion-store-v2.html')

def HomeGroceryStore(request):
    return render(request, 'home-grocery-store.html')

def HomeFurniturestore(request):
    return render(request,'home-furniture-store.html')

def HomeParcelStore(request):
    return render(request, 'home-parcel-store.html')

def HomeMarketStore(request):
    return render(request, 'home-marketplace.html')
