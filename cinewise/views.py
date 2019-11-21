from django.shortcuts import render, redirect
from dal import autocomplete
from .models import Node
from .forms import UserInputForm
from bs4 import BeautifulSoup
from django.utils.html import format_html


# Create your views here.
def home(request):
    if request.method == "POST":
        print("Post request!")
        # print(request.POST)
        form = UserInputForm(request.POST)
        print(form)
        form_soup = BeautifulSoup(form.__str__(), 'lxml')
        selected_soup = form_soup.find_all('option', selected=True)
        print(selected_soup)
        for soup in selected_soup:
            print(soup.text)
        # id_nodes = request.POST.get('id_nodes')
        # form.fields['id_nodes'].choices = [(id_nodes, id_nodes)]
        print(form.is_valid())
        # print(form.cleaned_data.get('nodes'))
        # print(form)
        # if form.is_valid():
        #     nodes = form.cleaned_data["nodes"]
        #     print("Form is valid")
        #     print(nodes)
        #     print(type(nodes))
        # else:
        #     print("Form is invalid")
        print("Redirecting!")
        return redirect("result")
    else:
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

    # def get_result_label(self, item):
    #     return format_html('{}', item.name)


def result(request):
    return render(request, "cinewise/results.html")
