from django.shortcuts import render
import markdown
from . import util
import random


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def mdToHtml(title):
    content = util.get_entry(title)
    marker = markdown.Markdown()
    if content == None:
        return None
    else:
        return marker.convert(content)

def entry(request,title):
    content = mdToHtml(title)
    if content == None:
        return render(request, "encyclopedia/error.html", { "message" : "This Page doesn't exist"})
    else:
        return render(request, "encyclopedia/entry.html", {
            "title" : title,
            "content" : content
        })

def search(request):
    if request.method == "POST":
        entry_search = request.POST['q']
        content = mdToHtml(entry_search)
        if content != None:
            return entry(request,entry_search)
        else :
            recom = []
            allentries = util.list_entries()
            for i in allentries:
                if entry_search.lower() in i.lower():
                    recom.append(i)
            
            return render(request, "encyclopedia/search.html",{"recom" : recom, "length" : len(recom)})


def newPage(request):
    if request.method == "GET":
        return render(request,"encyclopedia/newPage.html")
    else:
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {"message" : "This Page already exists!"})
        else:
            util.save_entry(title,content)
            return entry(request,title)
        

def edit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = util.get_entry(title)
        bytes(content, 'utf8')
        return render(request, "encyclopedia/edit.html", {
            "title" : title,
            "content" : content
        })
    
def saveEdit(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = bytes(request.POST["content"], 'utf8')
        util.save_entry(title,content)
        return entry(request,title)
    
def rand(request):
    picked = random.choice(util.list_entries())
    return entry(request,picked)
    

