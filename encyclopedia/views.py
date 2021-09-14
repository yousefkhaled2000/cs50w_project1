from django.shortcuts import render
from markdown import markdown
from django.http import HttpResponseRedirect
from django.urls import reverse
from random import randint, seed
from datetime import datetime
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, TITLE):
    entry = util.get_entry(TITLE)
    if not entry:
        return render(request, "encyclopedia/not_found.html")
    else:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown(entry),
            "title": TITLE
        })

def search(request):
    entries = util.list_entries()
    query = str(request.GET['q'])
    for entry in entries:
        if query.lower() == entry.lower():
            return HttpResponseRedirect(reverse("entry", args=[query]))
    else:
        results = []
        for entry in entries:
            if query.lower() in entry.lower():
                results.append(entry)
        return render(request, "encyclopedia/search.html", {
            "results": results
        })

def new(request):
    if request.method == "GET":
        return render(request, "encyclopedia/new.html", {
            "error": False
        })
    else:
        entries = util.list_entries()
        title = str(request.POST["title"])
        content = str(request.POST["content"])
        for entry in entries:
            if title.lower() == entry.lower():
                return render(request, "encyclopedia/new.html", {
                    "error": True
                })
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))

def edit(request, title):
    content = util.get_entry(title)
    if request.method == "GET":
        return render(request, "encyclopedia/edit.html", {
            "content": content,
            "title": title
        })
    else:
        ncontent = str(request.POST["ncontent"])
        util.save_entry(title, ncontent)
        return HttpResponseRedirect(reverse("entry", args=[title]))

def random(request):
    seed(datetime.now())
    entries = util.list_entries()
    random = randint(0, len(entries) - 1)
    return HttpResponseRedirect(reverse("entry", args=[entries[random]]))