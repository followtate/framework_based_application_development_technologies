from django.shortcuts import render

from storage import load_data


def lists(request):
    _, _, _, reading_lists = load_data()
    context = {"lists": list(reading_lists.values())}
    return render(request, "reading_lists/list_list.html", context)


def list_detail(request, list_id):
    _, _, _, reading_lists = load_data()
    reading_list = reading_lists.get(list_id)
    context = {"reading_list": reading_list}
    status = 404 if reading_list is None else 200
    return render(request, "reading_lists/list_detail.html", context, status=status)