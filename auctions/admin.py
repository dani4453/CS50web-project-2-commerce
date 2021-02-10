from django.contrib import admin

from .models import User, Category, Listing, Bid, Comment
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category")

class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "description", "bidprice", "image", "category", "status", "user")

class BidAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "bidder", "bidprice")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "datetime", "comment")

admin.site.register(Listing, ListingAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(User)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)