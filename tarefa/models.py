from django.db import models
from user.models import CustomUser

# Create your models here.
class Tarefa(models.Model):
    nomeTarefa = models.CharField(max_length=30, blank=False)
    descricao = models.TextField(blank=True)
    dataTarefa = models.DateField(auto_now_add=False, null=False)
    status = models.BooleanField(default=False)
    idUser = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    
    