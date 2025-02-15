# custom_filters.py
from django import template

register = template.Library()

@register.filter
def filter_gender(responses, gender):
    return len([response for response in responses if response.gender == gender])

@register.filter
def filter_age(responses, age_group):
    age_ranges = {
        'Under 18': (0, 17),
        '18-24': (18, 24),
        '25-34': (25, 34),
        '35-44': (35, 44),
        '45-54': (45, 54),
        '55+': (55, 150),
    }
    min_age, max_age = age_ranges.get(age_group, (0, 0))
    return len([response for response in responses if min_age <= response.age <= max_age])