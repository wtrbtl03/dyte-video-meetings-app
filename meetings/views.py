from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
import json
import requests


API_BASE_URL = "https://api.dyte.io/v2"

def shorten_meeting_link(meeting_link):
    try:
        response = requests.get(
            f"https://getPico.Link/get/{meeting_link}"
        )
        data = response.json()
        meeting_short_link = data['shortened_url']
    except:
        meeting_short_link = meeting_link
    return meeting_short_link

def create_meeting(request):
    print(request)
    if request.method == 'POST':
        title = request.POST.get('title')
        if_record_on_start = request.POST.get('record_on_start') == 'on'
        # if_record_on_start = False
        try:
            response = requests.post(
                'https://api.dyte.io/v2/meetings',
                json={
                    "title": title,
                    "record_on_start": if_record_on_start
                },
                headers={
                    "Authorization": f"Basic {settings.DYTE_CONN_BASE64}",
                    "Content-Type": "application/json",
                }
            )
            response.raise_for_status()  # Raises an HTTPError for bad responses
            
            data = response.json()
            
            if 'data' in data and 'id' in data['data']:
                meeting_id = data['data']['id']
                # return redirect('meeting_room', meeting_id=meeting_id)

                meeting_url = request.build_absolute_uri(f'/meeting/{meeting_id}/')
                meeting_short_link = shorten_meeting_link(meeting_url)            
                return render(request, 'meetings/create_meeting.html', {'meeting_url': meeting_short_link})
            else:
                print("Unexpected API response:", data)  # For debugging
                messages.error(request, "Unexpected response from Dyte API. Please try again.")
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")  # For debugging
            messages.error(request, "Failed to create meeting. Please check your API credentials and try again.")
        except ValueError as e:
            print(f"JSON decoding failed: {e}")  # For debugging
            messages.error(request, "Error parsing response from Dyte API.")
    
    return render(request, 'meetings/create_meeting.html')

def meeting_room(request, meeting_id):
    # Ensure session key is available
    session_key = request.session.session_key
    if not session_key:
        # Create a session key if it does not exist
        request.session.create()
        session_key = request.session.session_key

    try:
        response = requests.post(
            f'https://api.dyte.io/v2/meetings/{meeting_id}/participants',
            json={
                'preset_name': 'client_preset',
                'custom_participant_id': 'session_key'
            },
            headers={
                "Authorization": f"Basic {settings.DYTE_CONN_BASE64}",
                'Content-Type': 'application/json',
            }
        )
        response.raise_for_status()  # Raises an HTTPError for bad responses
        
        data = response.json()

        if 'data' in data and 'token' in data['data']:
            auth_token = data['data']['token']
            return render(request, 'meetings/meeting_room.html', {'meeting_id': meeting_id, 'auth_token': auth_token})
        else:
            print("Unexpected API response:", data) 
            messages.error(request, "Unexpected response from Dyte API. Please try again.")
            return redirect('create_meeting')
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")  
        messages.error(request, "Failed to add participant to meeting. Please try again.")
        return redirect('create_meeting')
    except ValueError as e:
        print(f"JSON decoding failed: {e}") 
        messages.error(request, "Error parsing response from Dyte API.")
        return redirect('create_meeting')

def test(request, preset_name):
    print(preset_name)
    response = requests.get(
        f'https://api.dyte.io/v2/presets/{preset_name}',
        headers={
            "Authorization": f"Basic {settings.DYTE_CONN_BASE64}",
            "Content-Type": "application/json",
        }
    )
    data = response.json()

    return JsonResponse(data)
