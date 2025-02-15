from django.shortcuts import render, redirect
from .forms import SurveyForm
from .models import SurveyResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db.models import Count
import json
from collections import Counter
from django.shortcuts import render
from .models import SurveyResponse

def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def survey(request):
    if request.method == 'POST':
        form = SurveyForm(request.POST)
        if form.is_valid():
            # Save the form data
            survey_response = form.save(commit=False)

            # Process the "heard_about" field (checkboxes)
            heard_about = request.POST.getlist('source')  # Get all selected checkboxes
            survey_response.heard_about = ', '.join(heard_about)  # Convert to comma-separated string

            # Save the response to the database
            survey_response.save()
    else:
        form = SurveyForm()
    return render(request, 'main/survey.html', {'form': form})


def adminIndex(request):
    responses = SurveyResponse.objects.all()
    return render(request, 'admins/index.html', {'responses': responses})

def surveyDetails(request):
    responses = SurveyResponse.objects.all()
    return render(request,'admins/surveys.html',{'responses': responses})

def user_logout(request):
    logout(request)
    return redirect('index')


def survey_charts(request):
    # Gender distribution
    gender_data = SurveyResponse.objects.values('gender').annotate(count=Count('gender'))
    gender_labels = [entry['gender'] for entry in gender_data]
    gender_counts = [entry['count'] for entry in gender_data]

    # Comfort rating distribution
    comfort_data = SurveyResponse.objects.values('comfortRating').annotate(count=Count('comfortRating'))
    comfort_labels = [entry['comfortRating'] for entry in comfort_data]
    comfort_counts = [entry['count'] for entry in comfort_data]

    # Convert data to JSON
    chart_data = {
        "gender_labels": gender_labels,
        "gender_counts": gender_counts,
        "comfort_labels": comfort_labels,
        "comfort_counts": comfort_counts,
    }

    return render(request, "charts.html", {"chart_data": json.dumps(chart_data)})

def analysis(request):
    # Fetch data from the SurveyResponse model
    queryset = SurveyResponse.objects.all()
    total_records = queryset.count()

    # Gender Distribution
    gender_data = dict(Counter(queryset.values_list('gender', flat=True)))
    gender_labels = list(gender_data.keys())
    gender_counts = list(gender_data.values())

    # Age Distribution
    age_data = dict(Counter(queryset.values_list('age', flat=True)))
    age_labels = list(age_data.keys())
    age_counts = list(age_data.values())

    # Region Distribution
    region_data = dict(Counter(queryset.values_list('region', flat=True)))
    region_labels = list(region_data.keys())
    region_counts = list(region_data.values())

    mattype_data = dict(Counter(queryset.values_list('mattressType', flat=True)))
    mattype_labels = list(mattype_data.keys())
    mattype_counts = list(mattype_data.values())

    context = {
        'total_records': total_records,
        'gender_data': gender_data,  # Make sure this is an iterable object
        'gender_labels': gender_labels,
        'gender_counts': gender_counts,
        'age_data': age_data,  # Same for this
        'age_labels': age_labels,
        'age_counts': age_counts,
        'region_data': region_data,
        'region_labels': region_labels,
        'region_counts': region_counts,
        'mattype_data': mattype_data,
        'mattype_labels': mattype_labels,
        'mattype_counts': mattype_counts,
    }
    return render(request, 'admins/analysis.html', context)
from django.shortcuts import render
from .models import SurveyResponse
from collections import Counter

#Create registration

def registration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm')

        #checking password 
        if password != confirm_password:
            return render(request, 'main/register.html', {
                'message': "Password doesn't match!!"
            })
        
        #checking username 
        if User.objects.filter(username=username).exists():
            return render(request, 'main/register.html', {
                'message': "User Name already exist..!!"
            })
        
        #Save User

        user = User.objects.create(
            username = username,
            first_name = first_name,
            last_name = last_name,
            email = email,
            password = password
        )

        user.save()
        return redirect('login')
    return render(request, 'main/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'main/login.html', {
                'message': "You don't have an account, Please register yourself"
            })
    return render(request, 'main/login.html' )
