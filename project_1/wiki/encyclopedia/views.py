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
