from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import CreateView, ListView
from django.views.generic.detail import DetailView

from .models import Auction, User


class ActiveAuctionsListView(ListView):
    model = Auction
    fields = ['title', 'description', 'active', 'image_url']
    template_name = "auctions/index.html"

    def get_queryset(self):
        return Auction.objects.filter(active=True)


def index(request):
    return render(request, "auctions/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

class AuctionCreateView(CreateView):
    model = Auction
    fields = ['title', 'description', 'image_url', 'starting_bid', 'category']
    template_name = 'auctions/create.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.current_bid = self.request.POST['starting_bid']
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('index')


class AuctionDetailView(DetailView):
    model = Auction
    fields = "_all_"
    template_name = 'auctions/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['in_watchlist'] = self.request.user.watchlist.filter(pk=self.object.pk).exists()
        context['comments'] = self.object.comments.all()
        print(context['comments'])
        return context

class WishlistListView(ListView):
    model= Auction
    fields = ['title', 'description', 'active', 'image_url']
    template_name = "auctions/index.html"

    def get_queryset(self):
        return Auction.objects.filter(watchlist=self.request.user)

def Categories(request):
    categories = Auction.objects.all().values_list("category", flat=True).distinct()
    print(categories)
    
    return render(request, "auctions/categories.html", context={"categories": categories})
class CategoryListView(ListView):
    model = Auction
    fields = ['title', 'description', 'active', 'image_url']
    template_name = "auctions/category.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.kwargs['category']
        return context

    def get_queryset(self):
        return Auction.objects.filter(category=self.kwargs['category'])

def bid(request, pk):
    auction = Auction.objects.get(pk=pk)
    bid = float(request.POST['bid'])
    if auction.created_by == request.user:
        return HttpResponse('You cannot bid on your own auction.')
    if auction.active:
        if bid >= auction.current_bid:
            auction.current_bid = bid
            auction.last_winner = request.user
            auction.save()
            return HttpResponseRedirect(reverse('auctions', args=(auction.pk,)))
        else:
            return HttpResponseRedirect(reverse('auctions', args=(auction.pk,)))

def toggle_watchlist(request, pk):
    auction = Auction.objects.get(pk=pk)
    in_watchlist = request.user.watchlist.filter(pk=auction.pk).exists()
    if auction.created_by == request.user:
        return HttpResponse('You cannot watch your own auction.')
    if in_watchlist:
        auction.watchlist.remove(request.user)
    else:
        auction.watchlist.add(request.user)
    auction.save()  # save to update the many-to-many field
    return HttpResponseRedirect(reverse('auctions', args=(auction.pk,)))

def active(request, pk):
    auction = Auction.objects.get(pk=pk)
    active = bool(int(request.POST['active']))
    print(active)
    auction.active = active
    auction.save()
    return HttpResponseRedirect(reverse('auctions', args=(auction.pk,)))

def comment(request, pk):
    auction = Auction.objects.get(pk=pk)
    comment = request.POST['comment']
    auction.comments.create(comment=comment, created_by=request.user)
    auction.save()
    return HttpResponseRedirect(reverse('auctions', args=(auction.pk,)))

