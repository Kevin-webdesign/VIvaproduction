from django import forms
from .models import SurveyResponse

class SurveyForm(forms.ModelForm):
    class Meta:
        model = SurveyResponse
        fields = '__all__'

    # Custom field for checkboxes (heard_about)
    heard_about = forms.MultipleChoiceField(
        choices=[
            ('Social Media', 'Social Media'),
            ('TV/Radio', 'TV/Radio'),
            ('Friend/Family', 'Friend/Family'),
            ('Store Display', 'Store Display'),
            ('Other', 'Other'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )

    # Custom fields for radio buttons and dropdowns
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    AGE_CHOICES = [
        ('18-25', '18-25'),
        ('26-35', '26-35'),
        ('36-45', '36-45'),
        ('46-55', '46-55'),
        ('56+', '56+'),
    ]
    age = forms.ChoiceField(
        choices=AGE_CHOICES,
        widget=forms.Select,
        required=False,
    )

    USAGE_DURATION_CHOICES = [
        ('Less than 3 months', 'Less than 3 months'),
        ('3-6 months', '3-6 months'),
        ('6-12 months', '6-12 months'),
        ('More than 1 year', 'More than 1 year'),
    ]
    usage_duration = forms.ChoiceField(
        choices=USAGE_DURATION_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    MATTRESS_TYPE_CHOICES = [
        ('Foam Mattress', 'Foam Mattress'),
        ('Spring Mattress', 'Spring Mattress'),
        ('Orthopedic Mattress', 'Orthopedic Mattress'),
        ('Other', 'Other'),
    ]
    mattress_type = forms.ChoiceField(
        choices=MATTRESS_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    COMFORT_RATING_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Average', 'Average'),
        ('Poor', 'Poor'),
    ]
    comfort_rating = forms.ChoiceField(
        choices=COMFORT_RATING_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    QUALITY_RATING_CHOICES = [
        ('Very Satisfied', 'Very Satisfied'),
        ('Satisfied', 'Satisfied'),
        ('Neutral', 'Neutral'),
        ('Dissatisfied', 'Dissatisfied'),
        ('Very Dissatisfied', 'Very Dissatisfied'),
    ]
    quality_rating = forms.ChoiceField(
        choices=QUALITY_RATING_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    SUPPORT_RATING_CHOICES = [
        ('Yes, very good', 'Yes, very good'),
        ('Somewhat good', 'Somewhat good'),
        ('Neutral', 'Neutral'),
        ('Not really', 'Not really'),
        ('No, not at all', 'No, not at all'),
    ]
    support_rating = forms.ChoiceField(
        choices=SUPPORT_RATING_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    PURCHASE_LOCATION_CHOICES = [
        ('Official Store', 'Official Store'),
        ('Local Retailer', 'Local Retailer'),
        ('Online', 'Online'),
        ('Other', 'Other'),
    ]
    purchase_location = forms.ChoiceField(
        choices=PURCHASE_LOCATION_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    SHOPPING_EXPERIENCE_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Average', 'Average'),
        ('Poor', 'Poor'),
    ]
    shopping_experience = forms.ChoiceField(
        choices=SHOPPING_EXPERIENCE_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    PRICE_SATISFACTION_CHOICES = [
        ('Yes, fair price', 'Yes, fair price'),
        ('Somewhat fair', 'Somewhat fair'),
        ('Too expensive', 'Too expensive'),
        ('Too cheap (low quality concern)', 'Too cheap (low quality concern)'),
    ]
    price_satisfaction = forms.ChoiceField(
        choices=PRICE_SATISFACTION_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    PRODUCT_DETAILS_CHOICES = [
        ('Yes, very helpful', 'Yes, very helpful'),
        ('Somewhat helpful', 'Somewhat helpful'),
        ('Neutral', 'Neutral'),
        ('Not really', 'Not really'),
        ('No, not at all', 'No, not at all'),
    ]
    product_details = forms.ChoiceField(
        choices=PRODUCT_DETAILS_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    RECOMMENDATION_CHOICES = [
        ('Yes', 'Yes'),
        ('Maybe', 'Maybe'),
        ('No', 'No'),
    ]
    recommendation = forms.ChoiceField(
        choices=RECOMMENDATION_CHOICES,
        widget=forms.RadioSelect,
        required=False,
    )

    def save(self, commit=True):
        instance = super().save(commit=False)
        # Convert list of heard_about choices to a comma-separated string
        instance.heard_about = ', '.join(self.cleaned_data.get('heard_about', []))
        if commit:
            instance.save()
        return instance
    
    