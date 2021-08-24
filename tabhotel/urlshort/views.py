from django.http.response import Http404, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
# Create your views here.
from .models import ShortURL
from .forms import CreateNewShortURL
from datetime import datetime
import random, string
from statistic.models import ClickAnalytic

def home(request):
    return render(request, 'home.html')

def createShortURL(request):
    if request.method == 'POST':
        form = CreateNewShortURL(request.POST)
        if form.is_valid():
            original_website = form.cleaned_data['original_url']
            random_chars_list = list(string.ascii_letters)
            random_chars=''
            for i in range(6):
                random_chars += random.choice(random_chars_list)
            while len(ShortURL.objects.filter(short_url=random_chars)) != 0:
                for i in range(6):
                    random_chars += random.choice(random_chars_list)
            d = datetime.now()
            s = ShortURL(original_url=original_website, short_url=random_chars, time_date_created=d)
            s.save()
            return render(request, 'urlcreated.html', {'chars':random_chars})
    else:
        form=CreateNewShortURL()
        context={'form': form}
        return render(request, 'create.html', context)
def redirect(request, url):
    current_obj = ShortURL.objects.filter(short_url=url)
    if len(current_obj) == 0:
        return render(request, 'pagenotfound.html')
    context = {'obj':current_obj[0]}
    return render(request, 'redirect.html', context)   
class ShortRedirectView(View):
	def get(self, request, shortcode=None, *args, **kwargs):

         qs= ShortURL.objects.filter(short_url=shortcode)
         if qs.count()!=1 and not qs.exists():
             raise Http404
         obj = qs.first()
         print(ClickAnalytic.objects.click_analyse(obj))
         return HttpResponseRedirect(obj.short_url)
       
		#object = get_object_or_404(ShortURL, shortcode=shortcode)
        
		#obj_url = object.url
		#ClickAnalytic.objects.click_analyse(object)
		#return HttpResponseRedirect(obj_url)