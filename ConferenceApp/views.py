from django.shortcuts import render
from django.http import HttpResponse
from .models import Conference
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .forms import ConferenceForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from rest_framework import viewsets
from .serializers import ConferenceSerializer

class ConferenceViewSet(viewsets.ModelViewSet):
    """API endpoint that allows conferences to be viewed or edited.
    - list() -> GET /conferences/
    - retrieve() -> GET /conference/{id}/
    - create() -> POST /conferences/
    - update() -> PUT /conferences/{id}/
    - partial_update() -> PATCH /conferences/{id}/
    - destroy() -> DELETE /conferences/{id}/
    """
    queryset = Conference.objects.all()
    serializer_class = ConferenceSerializer
    search_fields = ['name','theme','location']


# -------------------------

def simple_view(request):
    return HttpResponse("This is a simple view.")

def home_view(request):
    return render(request,'ConferenceApp/home.html')

def welcome(request,name):
    return render(request,
                  'ConferenceApp/welcome.html',
                  {'n': name}
            )

def listConferences(request):
    conferences = Conference.objects.all()
    return render(request, 'ConferenceApp/list.html',{'conferences':conferences})

class ConferenceCreateView(LoginRequiredMixin,CreateView):
    model = Conference
    fields = "__all__"
    success_url = reverse_lazy('conference_list_view')

class ConferenceUpdateView(UpdateView):
    model = Conference
    # fields = ['name','theme','location','start_date','end_date','description']
    success_url = reverse_lazy('conference_list_view') 
    form_class = ConferenceForm

class ConferenceDeleteView(DeleteView):
    model = Conference
    success_url = reverse_lazy('conference_list_view')
    def test_func(self):
        return self.request.user.role == 'committee' or self.request.user.is_superuser

class ConferenceListView(ListView):
    model = Conference
    template_name = 'ConferenceApp/list.html'
    context_object_name = 'conferences'

class ConferenceDetailView(DetailView):
    model = Conference

