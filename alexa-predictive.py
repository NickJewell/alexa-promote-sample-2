


"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit, 
connecting to the Alteryx Promote API and using slots to parameterise a predictive scoring
"""

from __future__ import print_function


# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alteryx Promote Alexa Predictive sample. " \
                    "Provide me some flower measurements and I'll classify for you " 
					
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Provide me some flower measurements and I'll classify for you" 

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



def iris_predict(intent, session):
    """ Sets the color in the session and prepares the speech to reply to the
    user. Note that this has to split the integer and decimal parts of the model into two separate slots as AMAZON NUMBER format only handles integers!
    """

    card_title = intent['name']
    session_attributes = {}
    should_end_session = False

	
    SL_1 = intent['slots']['SLPre']['value']
    SL_2 = intent['slots']['SLPost']['value']
    
    SepalLength = int(SL_1) + float(SL_2)*0.1
	
    SW_1 = intent['slots']['SWPre']['value']
    SW_2 = intent['slots']['SWPost']['value']
    
    SepalWidth = int(SW_1) + float(SW_2)*0.1
	
    PW_1 = intent['slots']['PWPre']['value']
    PW_2 = intent['slots']['PWPost']['value']
    
    PetalWidth = int(PW_1) + float(PW_2)*0.1
	
    PL_1 = intent['slots']['PLPre']['value']
    PL_2 = intent['slots']['PLPost']['value']
    
    PetalLength = int(PL_1) + float(PL_2)*0.1	
	
    import requests
    from requests.auth import HTTPBasicAuth

    data = '{"SL":' + str(SepalLength) + ',"SW": ' + str(SepalWidth) + ',"PL": ' + str(PetalLength) + ',"PW": ' + str(PetalWidth) + '}'
	
    #Post request body with basic auth
    r = requests.post('PROMOTE_MODEL_ENDPOINT', data=data, auth=('PROMOTE_USER_NAME', 'PROMOTE_API_KEY'))

    import json
    json_response = json.loads(r.text)
	
    setosa_score = json_response['result']['prediction.Score_Iris.setosa'][0]
    versicolor_score = json_response['result']['prediction.Score_Iris.versicolor'][0]
    virginica_score = json_response['result']['prediction.Score_Iris.virginica'][0]
    speech_output = 'Predicted Likelihood is as follows. Setosa: ' + str(round(setosa_score,2)) + '. Versicolor: ' + str(round(versicolor_score,2)) + '. Virginica: ' + str(round(virginica_score,2)) 
    reprompt_text = 'try again'	
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "Predict":
        return iris_predict(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "YOURAMAZONSKILLIDGOESHERE"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
