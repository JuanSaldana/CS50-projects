from typing import Type
from django.shortcuts import render
from random import choice

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry_name):
    return render(request, "encyclopedia/entry.html", {
        "entry_name": entry_name,
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


def create_entry(request, entry_name="", entry="", error=""):
    return render(request, "encyclopedia/create_entry.html", {"entry_name": entry_name, "entry": entry, "error": error, "state": "NEW"})


def save_entry(request, state="NEW"):
    title = request.GET.get("title")
    content = request.GET.get("content")
    if util.get_entry(title, default=False) and state == "NEW":
        return render(request, "encyclopedia/entry.html", {"entry": util.render_entry("error/COPY")})
    else:
        util.save_entry(title, content)
        return entry(request, title)


def edit_entry(request, entry_name):
    entry = util.get_entry(entry_name, default=False)
    if entry:
        return render(request, "encyclopedia/create_entry.html", {"entry": entry, "entry_name": entry_name, "state": "OLD"})


def random_page(request):
    entries = util.list_entries()
    return entry(request, choice(entries))
