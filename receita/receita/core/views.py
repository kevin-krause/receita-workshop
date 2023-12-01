from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from requests import HTTPError
from receita.core.receitaws import ReceitaWS
from django.contrib import messages
from receita.core.forms import CNPJForm, CommentForm
from receita.core.models import Comment, Empresa
from receita.core.utils import parse_date, parse_endereco
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    empresas = Empresa.objects.all().order_by('nome')
    if request.htmx:
        template_name = 'partials/index.html'
    else:
        template_name = 'index.html'
    return render(request, template_name, context={'empresas': empresas})


@login_required
def empresa_detail(request, pk):
    cnpj_data = get_object_or_404(Empresa, pk=pk)
    
    if request.method == "POST":
        comment_view(request, cnpj_data.cnpj)
    
    comment_form = CommentForm(
        initial={
            "user": request.user,
            "empresa": cnpj_data
        }
    )
    context = {
        "cnpj_data": cnpj_data,
        "comment_form": comment_form,
        "comments": Comment.objects.filter(empresa=cnpj_data).order_by('-created_at')
    }
    return render(request, 'empresa_detail.html', context)


@login_required
def busca_receita(request):
    receita_ws = ReceitaWS()
    context = {}
    cnpj = request.GET.get('cnpj')
    form = CNPJForm()

    if request.method == "POST":
        comment_view(request, cnpj)

    if cnpj:
        form = CNPJForm(request.GET)
        if form.is_valid():
            cnpj = form.cleaned_data['cnpj']
            cnpj_data = Empresa.objects.filter(cnpj=cnpj).first()

            if not cnpj_data:
                try:
                    cnpj_data = receita_ws.get_from_cnpj(cnpj=cnpj)
                    cnpj_data, _ = Empresa.objects.update_or_create(
                    cnpj=cnpj,
                    defaults={
                        'abertura': parse_date(cnpj_data['abertura'], '%d/%m/%Y'),
                        'situacao': cnpj_data['situacao'],
                        'tipo': cnpj_data['tipo'],
                        'nome': cnpj_data['nome'],
                        'fantasia': cnpj_data['fantasia'],
                        'endereco': parse_endereco(cnpj_data),
                        'email': cnpj_data['email'],
                    }
                )
                except HTTPError as e:
                    messages.error(request, e)

            comment_form = CommentForm(
                initial={
                    "user": request.user,
                    "empresa": cnpj_data
                }
            )
            context.update({
                        "cnpj_data": cnpj_data,
                        "comment_form": comment_form,
                        "comments": Comment.objects.filter(empresa=cnpj_data).order_by('-created_at')
                    })
    context.update({
        'form': form,
    })
    if request.htmx:
        template_name = 'partials/busca_receita.html'
    else:
        template_name = 'busca_receita.html'
    return render(request, template_name, context=context)


def comment_view(request, cnpj):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        empresa = get_object_or_404(Empresa, cnpj=cnpj)
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.empresa = empresa
        comment.save()
        messages.success(request, "Comentário enviado com sucesso!")
    else:
        messages.error(request, "Não foi possível comentar")
    return HttpResponseRedirect(reverse_lazy('core:busca_receita'))