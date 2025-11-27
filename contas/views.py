from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


from .models import Conta, Tag


@login_required
def dashboard(request):
    """
    Dashboard usando o usuário logado (request.user)
    """
    user = request.user

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'create':
            conta = Conta.objects.create(
                user=user,
                nome=request.POST.get('nome', ''),
                valor_total=Decimal(request.POST.get('valor_total') or '0'),
                descricao=request.POST.get('descricao') or ''
            )
            tipo_id = request.POST.get('tipo_id')
            if tipo_id:
                conta.tags.set([tipo_id])

        elif action == 'update':
            conta = get_object_or_404(Conta, id=request.POST.get('id'), user=user)
            conta.nome = request.POST.get('nome', '')
            conta.valor_total = Decimal(request.POST.get('valor_total') or '0')
            conta.descricao = request.POST.get('descricao') or ''
            conta.save()

            tipo_id = request.POST.get('tipo_id')
            if tipo_id:
                conta.tags.set([tipo_id])
            else:
                conta.tags.clear()

        elif action == 'delete':
            conta = get_object_or_404(Conta, id=request.POST.get('id'), user=user)
            conta.delete()

        return redirect('dashboard')

    # ----- listagem agrupada por tipo -----
    tags = Tag.objects.all().order_by('nome')
    groups = []

    # contas com tipo
    for tag in tags:
        contas = list(Conta.objects.filter(user=user, tags=tag).order_by('nome'))
        for c in contas:
            c.tipo_id = tag.id
        if contas:
            groups.append({
                'tipo_id': tag.id,
                'tipo_nome': tag.nome,
                'contas': contas,
            })

    # contas sem tipo
    sem_tipo = list(
        Conta.objects.filter(user=user, tags__isnull=True)
        .distinct()
        .order_by('nome')
    )
    for c in sem_tipo:
        c.tipo_id = ''
    if sem_tipo:
        groups.append({
            'tipo_id': 0,
            'tipo_nome': 'Sem tipo',
            'contas': sem_tipo,
        })

    context = {
        'groups': groups,
        'tags': tags,
        'no_user': False,
    }
    return render(request, 'contas/dashboard.html', context)

def logout_view(request):
    """
    Faz o logout e manda para a tela de login.
    """
    logout(request)
    return redirect('login')

