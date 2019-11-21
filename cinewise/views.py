from django.shortcuts import render
from dal import autocomplete
from .models import Node
from .forms import UserInputForm


# Create your views here.
def home(request):
    form = UserInputForm()
    return render(request, 'cinewise/index.html', {'form': form})
    # return HttpResponse("Home page comes here!")


class NodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            return Node.objects.none()
        qs = Node.objects.all()
        if self.q:
            qs = qs.filter(name__istartswith=self.q)
        return qs
