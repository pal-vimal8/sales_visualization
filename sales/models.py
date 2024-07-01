from django.db import models

# # Create your models here.
class Salesperson(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class SalesRecord(models.Model):
    salesperson = models.ForeignKey(Salesperson, on_delete=models.CASCADE)
    sales_month = models.DateField()
    sales_amount = models.FloatField()

    def __str__(self):
        return f"{self.salesperson.name} - {self.sales_month} - {self.sales_amount}"
#

# from django.db import models

# class Salesperson(models.Model):
#     name = models.CharField(max_length=100)
#     sales_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     sales_month = models.DateField()

#     def __str__(self):
#         return self.name
