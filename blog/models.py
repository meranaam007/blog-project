from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from account.models import Profile
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name

# class PublishedPostManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(status = "P")

# class CatProgManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(category__name = "Programming")

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status = "P")

    def programming(self):
        return self.filter(category__name = "Programming")


# class PostManager(models.Manager):
#     def get_queryset(self):
#         return PostQuerySet(self.model)

#     def published(self):
#         return self.get_queryset().published()

#     def programming(self):
#         return self.get_queryset().programming()


class Post(models.Model):
    statuses = [("D","Draft"),("P","Published")]

    title = models.CharField(max_length = 250)
    content = models.TextField()
    status = models.CharField(max_length=1,choices=statuses,default="D")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name="categories")
    image = models.ImageField(upload_to="blog/",blank = True)
    slug = models.SlugField(unique= True,blank = True)
    author = models.ForeignKey(Profile,on_delete=models.CASCADE)

    objects = models.Manager()
    posts = PostQuerySet.as_manager()
    # published = PublishedPostManager()
    # prg = CatProgManager()

    def __str__(self):
        return self.title

    def save(self,*args,**kwargs):
        
        self.slug = slugify(self.title)
        
        super().save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("post-detail",args=[self.slug])


