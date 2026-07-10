from rest_framework.views import exception_handler

def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        errors = response.data

        if isinstance(errors, dict):
            formatted_errors = {}

            for field, messages in errors.items():
                if isinstance(messages, list):
                    formatted_errors[field] = str(messages[0])  # first error only
                else:
                    formatted_errors[field] = str(messages)

            response.data = {"error":formatted_errors}

        elif isinstance(errors, list):
            response.data = {
                "error": str(errors[0])
            }

    return response