from django.shortcuts import render, redirect
import os
import json
from django.http import JsonResponse
from .forms import UserForm,EmergencyForm
from .models import UserDetails

JSON_FILE_PATH = 'data/UserData.json'
JSON_FILE_PATH2 = 'data/emergency.json'

def home(request):
    form = UserForm()
    return render(request, 'Main/home.html', {'UserForm': form})

def emerg(request):
    form2 = EmergencyForm()
    return render(request, 'Main/emergency.html', {'EmergencyForm': form2})


def view_donors(request):
    # Initialize donors and emergency data as empty lists
    donors = []
    emergency = []
    
    # Function to safely load JSON data from a file
    def load_json(file_path):
        if os.path.exists(file_path):  # Check if file exists
            try:
                with open(file_path, 'r') as file:
                    return json.load(file)
            except json.JSONDecodeError:
                # Log error or add debugging message if needed
                print(f"Error decoding JSON in file: {file_path}")
        return []  # Return an empty list if file doesn't exist or is invalid

    # Load data from both files
    donors = load_json(JSON_FILE_PATH)
    emergency = load_json(JSON_FILE_PATH2)

    # Pass the loaded data to the template
    context = {
        'donors': donors,
        'emergency': emergency
    }

    return render(request, 'Main/donors.html', context)
def save_user_details(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            # Extract cleaned data from the form
            cleaned_data = form.cleaned_data

            # Create a dictionary for the new entry
            new_entry = {
                "name": cleaned_data['name'],
                "mobile": cleaned_data['mobile'],
                "blood_group": cleaned_data['bg'],
                "gender": cleaned_data['gender'],
                "district": cleaned_data['dists'],
                "last_donated_date": str(cleaned_data['last_date'])  # Convert date to string for JSON serialization
            }

            try:
                # Read existing data from the JSON file
                try:
                    with open(JSON_FILE_PATH, 'r') as file:
                        data = json.load(file)
                except FileNotFoundError:
                    # If file doesn't exist, initialize an empty list
                    data = []

                # Append the new entry to the existing data
                data.append(new_entry)

                # Write the updated data back to the JSON file
                with open(JSON_FILE_PATH, 'w') as file:
                    json.dump(data, file, indent=4)

                return JsonResponse({
                    'status': 'success',
                    'message': 'User details saved successfully!'
                })

            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error saving data: {str(e)}'
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid form data!',
                'errors': form.errors
            })

    else:
        form = UserForm()
    return render(request, 'form.html', {'form': form})

def emergency_details(request):
    if request.method == 'POST':
        form = EmergencyForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data

            # Create a dictionary for the new emergency entry
            new_entry = {
                "pname": cleaned_data['pname'],
                "pmobile": cleaned_data['pmobile'],
                "bg_needed": cleaned_data['bg_needed'],
                "pgender": cleaned_data['pgender'],
                "units_needed": cleaned_data['units_needed'],
                "hospital_name": cleaned_data['hospital_name'],
                "pdists": cleaned_data['pdists'],
                "urgency_level": cleaned_data['urgency_level']
            }

            try:
                # Read existing data from the emergency JSON file
                try:
                    with open(JSON_FILE_PATH2, 'r') as file:
                        data = json.load(file)
                except FileNotFoundError:
                    # If file doesn't exist, initialize an empty list
                    data = []

                # Append the new entry to the existing emergency data
                data.append(new_entry)

                # Write the updated data back to the emergency JSON file
                with open(JSON_FILE_PATH2, 'w') as file:
                    json.dump(data, file, indent=4)

                return JsonResponse({
                    'status': 'success',
                    'message': 'Emergency details saved successfully!'
                })

            except Exception as e:
                return JsonResponse({
                    'status': 'error',
                    'message': f'Error saving emergency data: {str(e)}'
                })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Invalid form data!',
                'errors': form.errors
            })

    else:
        form = EmergencyForm()
    return render(request, 'form.html', {'form': form})
