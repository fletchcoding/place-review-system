from django.shortcuts import render
from django.views import generic

from .models import Place, Scorecard
from .forms import ReviewForm


class IndexView(generic.ListView):
    template_name = 'places/index.html'
    context_object_name = 'top_places_list'

    def get_queryset(self):
        """
        Returns a subset of places in the database
        """
        return Place.objects.all()

class DetailView(generic.DetailView):
    model = Place
    template_name = 'places/detail.html'
