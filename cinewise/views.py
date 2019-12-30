from django.shortcuts import render, redirect
from dal import autocomplete
from .models import Node
from .forms import UserInputForm
from bs4 import BeautifulSoup
from utils.Graph import gen_recommendations
from utils.Movies import movies_to_nodes, Movie, load_nodes


# Create your views here.
def home(request):
    if request.method == "POST":
        # print("Post request!")
        # print(request.POST.get)
        form = UserInputForm(request.POST)
        print(form.errors)
        print(form.is_valid())
        form_soup = BeautifulSoup(form.__str__(), 'lxml')
        selected_soup = form_soup.find_all('option', selected=True)
        print(selected_soup)
        for soup in selected_soup:
            print(soup.text)
        nodes = [soup.text for soup in selected_soup]
        print("Redirecting!")
        union_colors_results, energy_spread_results = gen_recommendations(nodes)
        # print(union_colors_results)
        # print(energy_spread_results)
        return render(request, "cinewise/results.html",
                      {"union_colors_results": union_colors_results, "energy_spread_results": energy_spread_results})
    else:
        form = UserInputForm()
        print(form)
        return render(request, 'cinewise/index.html', {'form': form})


def refreshnodes(request):
    nodes = load_nodes()
    Node.objects.all().delete()
    for node in nodes:
        node_model = Node(name=node)
        node_model.save()


class NodeAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # if not self.request.user.is_authenticated:
        #     return Node.objects.none()
        qs = Node.objects.all()
        if self.q:
            qs = qs.filter(name__contains=self.q)
        return qs
