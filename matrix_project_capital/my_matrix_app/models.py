from django.db import models


class Matrix(models.Model):
    start_matrix = models.TextField(max_length=255, blank=True)
    matrix_data = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return f"Matrix {self.pk}"
