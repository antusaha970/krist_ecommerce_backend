from django.db import models


class ClientMessage(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=300)
    message = models.TextField()
    received_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.email
