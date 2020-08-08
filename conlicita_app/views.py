from django.shortcuts import render


def budgets(request):



    return render(request, 'budgets.html', {'Nome': 'Egor'})
