from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def etablissement_list(request):
    return render(request, 'eftp_formel/etablissement_list.html', {'etablissements': []})

@login_required
def etablissement_create(request):
    return render(request, 'eftp_formel/etablissement_form.html')

@login_required
def etablissement_detail(request, pk):
    return render(request, 'eftp_formel/etablissement_detail.html', {'etablissement': None})

@login_required
def etablissement_edit(request, pk):
    return render(request, 'eftp_formel/etablissement_form.html')

@login_required
def etablissement_delete(request, pk):
    return render(request, 'eftp_formel/etablissement_confirm_delete.html')

@login_required
def import_export(request):
    return render(request, 'eftp_formel/import_export.html')