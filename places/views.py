from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import Place, Review, Feedback, Scorecard


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

class ReviewView(generic.DetailView):
    model = Place
    template_name = 'places/review.html'


@login_required
def postreview(request, place_id):
    place = get_object_or_404(Place, pk=place_id)
    review = Review(visit_date=timezone.now(), place=place, reviewer=request.user)

    feedback = Feedback(review=review)
    for field in feedback.get_field_names():
        if request.POST.get(field) == 'good':
            setattr(feedback, field, True)
        elif request.POST.get(field) == 'poor':
            setattr(feedback, field, False)

    if feedback.get_counts()[0] + feedback.get_counts()[1] < 3:
        return render(request, 'places/review.html', {
            'place':place,
            'error_message': 'Minimum 3 feedback points required'
        })
    else:
        review.save()
        feedback.save()
        return HttpResponseRedirect(reverse('places:detail', args=(place.id,)))
