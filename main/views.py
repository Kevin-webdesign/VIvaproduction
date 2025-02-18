from django.shortcuts import render, redirect
from .forms import SurveyForm
from .models import SurveyResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.db.models import Count
import json
from collections import Counter

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

    
    # Count the occurrences of each purchaseLocation
    purchaseLocation_data = dict(Counter(queryset.values_list('purchaseLocation', flat=True)))
    purchaseLocation_labels = list(purchaseLocation_data.keys())
    purchaseLocation_counts = list(purchaseLocation_data.values())

      # Gender Distribution
    heard_about_data = dict(Counter(queryset.values_list('heard_about', flat=True)))
    heard_about_labels = list(heard_about_data.keys())
    heard_about_counts = list(heard_about_data.values())


    # Mattress Type Distribution
    mattype_data = dict(Counter(queryset.values_list('mattressType', flat=True)))
    mattype_labels = list(mattype_data.keys())
    mattype_counts = list(mattype_data.values())

    context = {
        'total_records': total_records,
        'gender_data': gender_data,
        'gender_labels': gender_labels,
        'gender_counts': gender_counts,
        'age_data': age_data,
        'age_labels': age_labels,
        'age_counts': age_counts,
        'region_data': region_data,
        'region_labels': region_labels,
        'region_counts': region_counts,
        'mattype_data': mattype_data,
        'mattype_labels': mattype_labels,
        'mattype_counts': mattype_counts,
        'heard_about_data': heard_about_data,
        'heard_about_labels': heard_about_labels,
        'heard_about_counts': heard_about_counts,
       'purchaseLocation_labels': purchaseLocation_labels,
        'purchaseLocation_counts': purchaseLocation_counts,
        'responses': queryset,
    }
    return render(request, 'admins/index.html', context)



def gender_statistics(request):
    # Sample gender data (replace with actual database query)
    queryset = SurveyResponse.objects.all()
    total_records = queryset.count()

    # Gender Distribution
    gender_data = dict(Counter(queryset.values_list('gender', flat=True)))
    region_data = dict(Counter(queryset.values_list('region', flat=True)))
    purchase_data = dict(Counter(queryset.values_list('purchaseLocation', flat=True)))
    mattype_data = dict(Counter(queryset.values_list('mattressType', flat=True)))

    # Calculate statistics
    total_records = sum(gender_data.values())
    max_gender = max(gender_data, key=gender_data.get)
    max_count = gender_data[max_gender]
    min_gender = min(gender_data, key=gender_data.get)
    min_count = gender_data[min_gender]
    gender_ratio = f"{gender_data.get('Male', 0)}:{gender_data.get('Female', 0)}"

    max_region = max(region_data, key=region_data.get)
    max_region_count = region_data[max_region]
    min_region = min(region_data, key=region_data.get)
    min_region_count = region_data[min_region]

    max_purchase_method = max(purchase_data, key=purchase_data.get)
    max_purchase_count = purchase_data[max_purchase_method]
    min_purchase_method = min(purchase_data, key=purchase_data.get)
    min_purchase_count = purchase_data[min_purchase_method]

    max_mattype = max(mattype_data, key=mattype_data.get)
    max_mattype_count = mattype_data[max_mattype]
    min_mattype = min(mattype_data, key=mattype_data.get)
    min_mattype_count = mattype_data[min_mattype]

    context = {
        "total_records": total_records,
        "gender_labels": json.dumps(list(gender_data.keys())),
        "gender_counts": json.dumps(list(gender_data.values())),
        "max_gender": max_gender,
        "max_count": max_count,
        "min_gender": min_gender,
        "min_count": min_count,
        "gender_ratio": gender_ratio,
        "region_labels": json.dumps(list(region_data.keys())),
        "region_counts": json.dumps(list(region_data.values())),
        "max_region": max_region,
        "max_region_count": max_region_count,
        "min_region": min_region,
        "min_region_count": min_region_count,
        "purchaseLocation_labels": json.dumps(list(purchase_data.keys())),
        "purchaseLocation_counts": json.dumps(list(purchase_data.values())),
        "max_purchase_method": max_purchase_method,
        "max_purchase_count": max_purchase_count,
        "min_purchase_method": min_purchase_method,
        "min_purchase_count": min_purchase_count,
        "mattype_labels": json.dumps(list(mattype_data.keys())),
        "mattype_counts": json.dumps(list(mattype_data.values())),
        "max_mattype": max_mattype,
        "max_mattype_count": max_mattype_count,
        "min_mattype": min_mattype,
        "min_mattype_count": min_mattype_count,
    }
    return render(request, "admins/statistic.html", context)

    
    return render(request, "admins/statistic.html", context)

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

    

    # Mattress Type Distribution
    mattype_data = dict(Counter(queryset.values_list('mattressType', flat=True)))
    mattype_labels = list(mattype_data.keys())
    mattype_counts = list(mattype_data.values())

    context = {
        'total_records': total_records,
        'gender_data': gender_data,
        'gender_labels': gender_labels,
        'gender_counts': gender_counts,
        'age_data': age_data,
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
                'message': "Either Username or password is wrong. If You don't have account register you self"
            })
    return render(request, 'main/login.html' )





#the last table

def purchase(request):
    # Query all survey responses
    queryset = SurveyResponse.objects.all()
    total_records = queryset.count()

    # Count the occurrences of each purchaseLocation
    purchaseLocation_data = dict(Counter(queryset.values_list('purchaseLocation', flat=True)))
    purchaseLocation_labels = list(purchaseLocation_data.keys())
    purchaseLocation_counts = list(purchaseLocation_data.values())

    # Prepare context for the template
    context = {
        'total_records': total_records,
        'purchaseLocation_labels': purchaseLocation_labels,
        'purchaseLocation_counts': purchaseLocation_counts,
    }

    # Render the template with the context
    return render(request, 'admins/purchase.html', context)


def age(request):
    # Fetch data from the SurveyResponse model
    queryset = SurveyResponse.objects.all()
    total_records = queryset.count()
    # Age Distribution
    age_data = dict(Counter(queryset.values_list('age', flat=True)))
    age_labels = list(age_data.keys())
    age_counts = list(age_data.values())

    context = {
        'total_records': total_records,
        'age_data': age_data,
        'age_labels': age_labels,
        'age_counts': age_counts,
    }
    return render(request, 'admins/age.html', context)



def mattype(request):
    # Fetch data from the SurveyResponse model
    queryset = SurveyResponse.objects.all()
    total_records = queryset.count()

    # Mattress Type Distribution
    mattype_data = dict(Counter(queryset.values_list('mattressType', flat=True)))
    mattype_labels = list(mattype_data.keys())
    mattype_counts = list(mattype_data.values())

    context = {
        'total_records': total_records,
        'mattype_data': mattype_data,
        'mattype_labels': mattype_labels,
        'mattype_counts': mattype_counts,
    }
    return render(request, 'admins/mattype.html', context)


def source(request):
    # Fetch data from the SurveyResponse model
    queryset = SurveyResponse.objects.all()
    total_records = queryset.count()

    # Gender Distribution
    heard_about_data = dict(Counter(queryset.values_list('heard_about', flat=True)))
    heard_about_labels = list(heard_about_data.keys())
    heard_about_counts = list(heard_about_data.values())


    context = {
        'total_records': total_records,
        'heard_about_data': heard_about_data,
        'heard_about_labels': heard_about_labels,
        'heard_about_counts': heard_about_counts,
    }
    return render(request, 'admins/source.html', context)

def gender(request):
    # Fetch data from the SurveyResponse model
    queryset = SurveyResponse.objects.all()
    total_records = queryset.count()

    # Gender Distribution
    gender_data = dict(Counter(queryset.values_list('gender', flat=True)))
    gender_labels = list(gender_data.keys())
    gender_counts = list(gender_data.values())


    context = {
        'total_records': total_records,
        'gender_data': gender_data,
        'gender_labels': gender_labels,
        'gender_counts': gender_counts,
    }
    return render(request, 'admins/analysis2.html', context)

def region(request):
    # Fetch data from the SurveyResponse model
    queryset = SurveyResponse.objects.all()
    total_records = queryset.count()
    # Region Distribution
    region_data = dict(Counter(queryset.values_list('region', flat=True)))
    region_labels = list(region_data.keys())
    region_counts = list(region_data.values())

  

    context = {
        'total_records': total_records,
        'region_data': region_data,
        'region_labels': region_labels,
        'region_counts': region_counts,
      
    }
    return render(request, 'admins/region.html', context)