
README

This is a simple repository that contains all the code components needed by the Alexa skill in order to call a parameterised score from an Alteryx Promote-hosted model. 

HOW TO DEPLOY

Download this repository (including the multiple subfolders) and the alexa-promote.py file. Feel free to edit the contents of alexa-promote.py to meet your needs, and to include the relevant Alexa Skill ID, Promote Server URL, username and API key details. 

Zip these files locally so that you can import them into your AWS Lambda function as a single package (or host them in a dedicated S3 bucket). 

Create your AWS Lambda function by signing up at: https://console.aws.amazon.com/lambda/home?region=us-east-1#/functions

Create your Alexa Skill by signing up at: 
https://developer.amazon.com/alexa-skills-kit

Test your skill using: 
http://echosim.io/

CONFIGURATION NOTES:
--------------------

LAMBDA FUNCTION Configuration: 

 - Be sure to use a blank python function template
 - Use Python 2.7
 - Set your handler to alexa-predictive.lambda_handler (referencing the python code in the repo)
 - You'll need to create a basic lambda execution role. Instructions here: http://docs.aws.amazon.com/lambda/latest/dg/with-s3-example-create-iam-role.html
 - In Advanced Settings, use a timeout of 30s (as I've found the default 3s to be a little unforgiving!)
 - Once created, take a note of the ARN (Amazon Resource ID) as you'll need to link this into your Alexa Skill.

ALEXA SKILL Configuration: 

 - Add a new skill via the developer console at: https://developer.amazon.com/edw/home.html#/skills
 - Once created, make sure you note the skill ID (you then need to add this to your lambda function) 
 - Give the skill a name. For example 'Alteryx-Promote-Demo-2'
 - Give the skill an invocation, for example 'classification demo'. This means you'll call the skill by saying 'Alexa, open classification demo'
 - Define an Interaction Model. For this example, we've added some extra slots to capture the model parameters we want to use for scoring. An interesting issue with the built-in Alexa SLOT_TYPES means that it can't read decimals using AMAZON.NUMBER, so we have a more complex interaction model that handles pre-decimal and post-decimal numbers for this example. 
 
> {
  "intents": [
    {
      "slots": [
        {
          "name": "SLPre",
          "type": "AMAZON.NUMBER"
        },
        {
          "name": "SLPost",
          "type": "AMAZON.NUMBER"
        },
        {
          "name": "SWPre",
          "type": "AMAZON.NUMBER"
        },
        {
          "name": "SWPost",
          "type": "AMAZON.NUMBER"
        },
        {
          "name": "PLPre",
          "type": "AMAZON.NUMBER"
        },
        {
          "name": "PLPost",
          "type": "AMAZON.NUMBER"
        },
        {
          "name": "PWPre",
          "type": "AMAZON.NUMBER"
        },
        {
          "name": "PWPost",
          "type": "AMAZON.NUMBER"
        }
      ],
      "intent": "Predict"
    },
    {
      "intent": "AMAZON.HelpIntent"
    }
  ]
}

 - Set up Sample Utterances so that the skill knows how to run. In our Python code we're expecting an Intent called Predict, so add a sample such as:
> Predict Classify Sepal Length {SLPre} point {SLPost} and Sepal Width {SWPre} point {SWPost} and Petal Length {PLPre} point {PLPost} and Petal Width {PWPre} point {PWPost}

 - So when the user says 'Alexa, ask classification demo to classify sepal length four point two and sepal width one point six and petal length one point four and petal width two point six', the correct python function will trigger. 
 - Go to the configuration tab, and make sure that the ARN for the Lambda code is entered here. 
 - Now go to the test tab, and start trying the skill out! If you get errors, go back to your AWS console and examine the Cloudwatch logs: you'll get all the python log details there. Also, check your Promote server's logs in case the model itself is having issues. 

