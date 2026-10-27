from django.shortcuts import render

from storage import load_sources


def sources_list(request):
    sources = load_sources()
    context = {"sources": list(sources.values())}
    return render(request, "sources/source_list.html", context)


def source_detail(request, source_id):
    sources = load_sources()
    source = sources.get(source_id)
    context = {"source": source}
    status = 404 if source is None else 200
    return render(request, "sources/source_detail.html", context, status=status)