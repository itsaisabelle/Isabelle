from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name
    
class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    reported = models.BooleanField(default=False)
    commentCounter = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id) + ' - ' + self.movie.name
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        counter = Review.objects.filter(user=self.user).count()
        Review.objects.filter(user=self.user).update(commentCounter=counter)

class Most(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    reviewCounter = models.PositiveIntegerField(default=0)
    amountPurchased = models.PositiveIntegerField(default=0)

    @receiver(post_save, sender='cart.Item')
    def mostP(sender, instance, **kwargs):
        from cart.models import Item
        record, created = Most.objects.get_or_create(movie=instance.movie)
        totalQ = Item.objects.filter(movie=instance.movie).aggregate(total=Sum('quantity'))
        total = totalQ['total'] or 0
        record.amountPurchased = total
        record.save()

    @receiver(post_save, sender='movies.Review')
    def mostR(sender, instance, **kwargs):
        record, created = Most.objects.get_or_create(movie=instance.movie)
        totalQ = Review.objects.filter(movie=instance.movie).count()
        record.reviewCounter = totalQ
        record.save()

class Report(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)
    review = models.ForeignKey(Review,
        on_delete=models.CASCADE)
    user = models.ForeignKey(User,
        on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.id) + ' - ' + self.review.user.username