from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.template import loader
import json

from .models import ImageName
from .forms import ImageUploadForm

class IndexView(generic.ListView):
    template_name = 'diabetics/index.html'
    context_object_name = 'latest_images_list'

    def get_queryset(self):
        '''Return the last three uploaded images.'''
        return ImageName.objects.order_by('imagename')[:3]    

class UploadsView(generic.edit.FormView):
    form_class = ImageUploadForm
    template_name = 'diabetics/uploads.html'  
    success_url = '../list_view' # Replace with your URL or reverse().

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist('image')
        if form.is_valid():
            for f in files:
                new = ImageName(image = f,
                                imagename = f)
                new.save()

            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    
    def get_queryset(self):
        '''Return the last three uploaded images.'''
        return ImageName.objects.order_by('imagename')[:3]

class DeleteView(generic.edit.DeleteView):
    model = ImageName
    success_url = '../../list_view'
    template_name = 'diabetics/delete.html'
  

def individual(request, imagename_id):
    '''Return the specified instance of ImageName.'''
    image = get_object_or_404(ImageName, pk=imagename_id)
    # Get next image or the first image if current image is the last one.
    try:
        next_image = ImageName.objects.get(pk=str(int(imagename_id) + 1))
    except ImageName.DoesNotExist:
        next_image = ImageName.objects.order_by('imagename')[0]
    # Get previous image or the last image if current image is the first one.
    try:
        pre_image = ImageName.objects.get(pk=str(int(imagename_id) - 1))
    except ImageName.DoesNotExist:
        pre_image = ImageName.objects.order_by('imagename').reverse()[0]
    context = {'image': image,
               'next_image': next_image,
               'pre_image': pre_image}
               
    return render(request, 'diabetics/individual.html', context)

class ListView(generic.ListView):
    template_name = 'diabetics/list_view.html'
    context_object_name = 'images_list'

    def get_queryset(self):
        return ImageName.objects.all()    

def summary(request):
    all_severe = ImageName.objects.all()
    result = {"No DR": 0,
              "Mild": 0,
              "Moderate": 0,
              "Severe": 0,
              "Proliferative DR": 0}
    for i in all_severe:
        result[i.result] += 1
        
    return render(request, 'diabetics/summary.html', {'result': json.dumps(result)})

