from django.views.generic import CreateView, UpdateView, DeleteView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin


class OwnerListView(ListView):
    pass
    #just do what listView do



class OwnerDetailView(DetailView):

    pass
    #subclass of DetailView
    






class OwnerCreateView(LoginRequiredMixin ,CreateView):

    def form_valid(self,form):

        object = form.save(commit=False)
        object.owner = self.request.user
        object.save()

        return super(CreateView,self).form_valid(form)




class OwnerUpdateView(LoginRequiredMixin,UpdateView):

    def get_queryset(self):

        query = super(UpdateView,self).get_queryset()
        return query.filter(owner=self.request.user)


class OwnerDeleteView(LoginRequiredMixin,DeleteView):
    pass


