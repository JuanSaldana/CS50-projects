from typing import Type
from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry_name):
    return render(request, "encyclopedia/entry.html", {
        "entry": util.render_entry(entry_name),
    })


def search_results(request):
    query = request.GET.get("q")
    results = util.search_entry(query)
    if isinstance(results, list):
        return render(request, "encyclopedia/search_results.html", {
            "results": results
        })
    elif isinstance(results, str):
        return entry(request, results)
    else:
        return entry(request, query)
