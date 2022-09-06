import os
from datetime import datetime
import steps_pool

try:
    env = os.getenv("ENV", "dev")

except Exception as e:
    print("error encountered in initialize lambda configuration %s" % e)


def lambda_handler(event):
    print(f"{datetime.now()} - lambda_handler - started")
    
    try:
        print(f"event for handling: {event}\n------------------")
        step = event['First']
        steps = event['Steps']
        while (True):
            action = step['Action']
            if (action != 'start'):
                stepMethod = getattr(steps_pool, action+"_action")
                args = step['Arguments']
                result = stepMethod(args)
            next = step['NextStepId']
            if (next == "-1"):
                return result
            step = steps[next]

    except Exception as e:
        print(f'failed to run lambda_handler, please see exception {e}')

    print(f"{datetime.now()} - lambda_handler - ended")


if __name__ == "__main__":
    lambda_handler(
        {
            "Id": "POC",
            "SupportedActions": [
                "start",
                "print",
                "set_variable",
                "file_exists",
                "read_file_into_variable",
                "end"
            ],
            "First": 
                {
                    "Action": "start",
                    "Arguments": {"none": "none"},
                    "NextStepId": "1"
                },
            "Steps": 
            {
                "1" : {
                    "Action": "print",
                    "Arguments": {"input": "123"},
                    "NextStepId": "2"
                },
                "2" : {
                    "Action": "end",
                    "Arguments": {"result": "success", "output": "123"},
                    "NextStepId": "-1"
                }
            }
        })

# Points to consider:

# Q - What's the api here? a single function? a class?
# A - a single function that handles the request, and another class that hold the steps

# Q - How do you hold the workflow in memory? parse it ahead of time? maybe read it as you go?
# A - parse it ahead of time, and hold it in memory

# Q - How do you debug the evaluation process?
# A - print the steps as you go

# Q - How do you make it easy to add actions?
# A - add them to the steps_pool.py file

# Q -How to you provide dependencies? (no need to integrate a real service locator or DI framework, just show how you'll use
# them)
# A - import the dependencies in the steps_pool.py file

# Q - Will be be able to easily change how actions are evaluated (e.g add logging)?
# A - yes, by adding the logging to the steps_pool.py file