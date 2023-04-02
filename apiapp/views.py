from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests

@csrf_exempt
def who_made_me(request):
    try:
        if request.method == 'GET':
            data_about_me = {
                "Creator": "Syed Muhammad Danish",
                "FunFact": "I think I am a great cook"
            }
            return JsonResponse(data_about_me, status=200)
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def number_to_word(request):
    try:
        data = json.loads(request.body)
        if request.method == 'POST':
            # Check if num key is present in the request body
            if not 'num' in data:
                return JsonResponse({'error': 'Input parameter missing'}, status=400)
            num = data['num']
            if num is not None:
                try:
                    # Try to convert the input to an integer if a number is given as a string
                    num = int(num)
                except ValueError:
                    return JsonResponse({'error': 'Input must be an integer'}, status=400)
                # Map the integer to its corresponding English word
                words = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
                if 0 <= num <= 9:
                    return JsonResponse({'word': words[num]}, status=200)
                else:
                    return JsonResponse({'error': 'Input must be an integer between 0 and 9'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON request body'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
def get_word(request, word):
    try:
        if request.method == 'GET':
            if word.isdigit():
                return JsonResponse({'error': 'Input must be a word, not a number'}, status=400)
            url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
            response = requests.get(url)
            isVerb = False     #Check if the word is verb
            isNoun = False     #Check if the word is noun
            data = response.json()
            if response.ok:
                for index, meaning in enumerate(data[0]['meanings']):
                    if meaning['partOfSpeech'] == 'verb':
                        isVerb = True
                        verb_index = data[0]['meanings'].index(meaning)    # get index of verb in a tuple
                        
                    if meaning['partOfSpeech'] == 'noun':
                        isNoun = True
                        noun_index = data[0]['meanings'].index(meaning)    # get index of noun in a tuple
                        
                if isVerb is True:
                    for index, definition in enumerate(data[0]['meanings'][verb_index]['definitions']):
                        if 'example' in definition:    #Check if example is available in verb
                            verb_example_index = data[0]['meanings'][verb_index]['definitions'].index(definition)
                            return JsonResponse({'Example sentence': data[0]['meanings'][verb_index]['definitions'][verb_example_index]['example']}, status=200)
                    return JsonResponse({'result': 'This can be used as a verb, but unfortunately, there is no example available'}, status=200)
                

                if isVerb is False and isNoun is True:
                    for index, definition in enumerate(data[0]['meanings'][noun_index]['definitions']):
                        if 'definition' in definition:      #Check if dictionary definition is available in noun
                            noun_definition_index = data[0]['meanings'][noun_index]['definitions'].index(definition)
                            return JsonResponse({'Dictionary definition': data[0]['meanings'][noun_index]['definitions'][noun_definition_index]['definition']}, status=200)
                    return JsonResponse({'result': 'Sorry, No definition is available for this noun'}, status=200)
                
                
                if isVerb is False and isNoun is False:
                    return JsonResponse({'result': 'Sorry, the word is neither a verb nor a noun'}, status=200)
            
            else:
                return JsonResponse({'error' : data["message"] }, status=400)
        
        else:
            return JsonResponse({'error': 'Method not allowed'}, status=405)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)