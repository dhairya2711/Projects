from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    pass


class Catagory(models.Model):
    catagory = models.CharField(max_length=100, null=False)

    def __str__(self):
        return f"{self.catagory}"


class AuctionList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="maker")
    title = models.CharField(max_length=100, null=False)
    discription = models.TextField(null=False)
    img_url = models.TextField()
    status = models.BooleanField(default=True)
    catagory = models.ForeignKey(Catagory, on_delete=models.CASCADE, related_name="auction", null=True)

    def __str__(self):
        return self.title


class Bid(models.Model):
    auction = models.ForeignKey(AuctionList, on_delete=models.CASCADE, related_name="bid_on")
    bid = models.FloatField(null=False)
    bidder_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")

    def __str__(self):
        return f"{self.auction}: {self.bid}"


class Comment(models.Model):
    item = models.ForeignKey(AuctionList, on_delete=models.CASCADE)
    comment_name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    comment = models.TextField(null=False)

    def __str__(self):
        return f"{self.comment_name}:\n{self.item}: {self.comment}"


class WatchList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ManyToManyField(AuctionList, blank=True, related_name="items")

    def __str__(self):
        return f"Name: {self.user} Item: {self.auction} "
