from django.db import models


class SurveyResponse(models.Model):
    # Page 1: General Information
    fullName= models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)
    age = models.CharField(max_length=10, blank=True, null=True)
    region = models.CharField(max_length=100, blank=True, null=True)
    heard_about = models.CharField(max_length=200, blank=True, null=True) 

    # Page 2: Product Experience
    usageDuration = models.CharField(max_length=50, blank=True, null=True)
    mattressType = models.CharField(max_length=50, blank=True, null=True)
    comfortRating = models.CharField(max_length=50, blank=True, null=True)
    qualityRating = models.CharField(max_length=50, blank=True, null=True)
    supportRating = models.CharField(max_length=50, blank=True, null=True)

    # Page 3: Purchase Experience
    purchaseLocation = models.CharField(max_length=50, blank=True, null=True)
    shoppingExperience = models.CharField(max_length=50, blank=True, null=True)
    priceSatisfaction = models.CharField(max_length=50, blank=True, null=True)
    productDetails = models.CharField(max_length=50, blank=True, null=True)

    # Page 4: Improvement & Suggestions
    likes = models.TextField(blank=True, null=True)
    improvements = models.TextField(blank=True, null=True)
    recommendation = models.CharField(max_length=50, blank=True, null=True)
    comments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.fullName or "Anonymous Response"
