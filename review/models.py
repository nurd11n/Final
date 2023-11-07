# from django.db import models
# from django.contrib.auth import get_user_model
# from car.models import ...
#
#
# User = get_user_model()
#
#
# class Comment(models.Model):
#     body = models.TextField()
#     author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
#     flight = models.ForeignKey(Flight, related_name='comments', on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#
#
# class Like(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
#     flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='likes')
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f'{self.author.name} liked {self.ticket.title}'
#
#
# class Rating(models.Model):
#     rating = models.PositiveSmallIntegerField()
#     flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='ratings')
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
#
#     def __str__(self):
#         return f'{self.rating} - {self.ticket}'
#
#
# class Favourites(models.Model):
#     author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favourites')
#     flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='favourites')
#
#     def __str__(self):
#         return f'{self.author} {self.ticket}'
#

