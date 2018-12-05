from django.shortcuts import render
from django.db.models import F,ExpressionWrapper,DecimalField
from django.http import HttpResponseRedirect
from django.views import View
from django.forms import ModelForm
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
# from django.views.generic.edit import DeleteView
# from django.views.generic.edit import UpdateView


from .models import Tesouro
# Create your views here.
class ListarTesouros(LoginRequiredMixin, ListView):
    model = Tesouro
    template_name = "lista_tesouros.html"

    def get_queryset(self, **kwargs):
        lst_tesouros = Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
                                 output_field=DecimalField(max_digits=10,\
                                                         decimal_places=2,\
                                                          blank=True)\
                                                         )\
                                 )
        return lst_tesouros

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_geral'] = 0
        for obj in context['object_list']:
            context['total_geral'] += obj.valor_total
        return context


    # def get(self,request):
    #     lst_tesouros = Tesouro.objects.annotate(valor_total=ExpressionWrapper(F('quantidade')*F('preco'),\
    #                         output_field=DecimalField(max_digits=10,\
    #                                                 decimal_places=2,\
    #                                                  blank=True)\
    #                                                 )\
    #                         )
    #     valor_total = 0
    #     for tesouro in lst_tesouros:
    #         valor_total += tesouro.valor_total
    #     return render(request,"lista_tesouros.html",{"lista_tesouros":lst_tesouros,
    #                                                  "total_geral":valor_total})




# class TesouroForm(ModelForm):
#     class Meta:
#         model = Tesouro
#         fields = ['nome', 'quantidade', 'preco', 'img_tesouro']
#         labels = {
#             "img_tesouro": "Imagem"
#         }
#
# class SalvarTesouro(View):
#     def get_tesouro(self,id):
#         if id:
#             return Tesouro.objects.get(id=id)
#         return None
#
#     def get(self,request,id=None):
#         return render(request,"salvar_tesouro.html",{"tesouroForm":TesouroForm(instance=self.get_tesouro(id))})
#
#     def post(self,request,id=None):
#         form = TesouroForm(request.POST,request.FILES, instance=self.get_tesouro(id))
#
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('lista_tesouros') )
#         else:
#             return render(request,"salvar_tesouro.html",{"tesouroForm":form})
#
# class RemoverTesouro(View):
#     def get(self,request,id):
#         Tesouro.objects.get(id=id).delete()
#         return HttpResponseRedirect(reverse('lista_tesouros') )

class RemoverTesouro(LoginRequiredMixin, DeleteView):
    model = Tesouro
    success_url = reverse_lazy("lista_tesouros")


class InserirTesouro(LoginRequiredMixin, CreateView):
    model = Tesouro
    fields = "__all__"
    template_name = "salvar_tesouro.html"
    success_url = reverse_lazy("lista_tesouros")

class AtualizarTesouro(LoginRequiredMixin, UpdateView):
    model = Tesouro
    fields = "__all__"
    template_name = "salvar_tesouro.html"
    success_url = reverse_lazy("lista_tesouros")
