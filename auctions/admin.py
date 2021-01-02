from django.contrib import admin
from .models import AuctionList, Bid, Comment, Catagory, WatchList, User

# Register your models here.
admin.site.register(AuctionList)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchList)
admin.site.register(Catagory)
admin.site.register(User)
