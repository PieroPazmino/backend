from django.db import models
# Create your models here.
class MainModel(models.Model):

# Create your models here.
    class Meta:
            permissions = [
                ("index_viewer", "Can show to index view (function-based)"),
            ]