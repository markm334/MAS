from django.shortcuts import render

# Create your views here.
def index(request):
	return render(request, 'index.html')


def about(request):
	return render(request, 'about.html')


def contact(request):
	return render(request, 'contact.html')


def blog(request):
	return render(request, 'blog.html')


def gallery(request):
	return render(request, 'gallery.html')


def events(request):
	return render(request, 'events.html')


def donation(request):
	return render(request, 'donation.html')


def volunteer(request):
	return render(request, 'volunteer.html')


def service(request):
    return render(request, 'service.html')


def causes(request):
    return render(request, 'causes.html')
