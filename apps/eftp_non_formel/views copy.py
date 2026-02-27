from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def structure_list(request):
    return render(request, 'eftp_non_formel/structure_list.html', {'structures': []})

@login_required
def structure_create(request):
    return render(request, 'eftp_non_formel/structure_form.html')

@login_required
def structure_detail(request, pk):
    return render(request, 'eftp_non_formel/structure_detail.html', {'structure': None})

@login_required
def structure_edit(request, pk):
    return render(request, 'eftp_non_formel/structure_form.html')

@login_required
def structure_delete(request, pk):
    return render(request, 'eftp_non_formel/structure_confirm_delete.html')

@login_required
def import_export(request):
    return render(request, 'eftp_non_formel/import_export.html')