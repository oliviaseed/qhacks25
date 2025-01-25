import requests

import os
from groq import Groq

def call_groq_ai(api_url, payload, headers):
    """
    Function to call Groq AI API and return the response.

    Parameters:
        api_url (str): The endpoint URL for the Groq AI API.
        payload (dict): The data to send in the request body.
        headers (dict): The headers, including API keys or tokens if required.

    Returns:
        dict: Response from the API.
    """
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Example usage
if __name__ == "__main__":

    api_key = "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"
    client = Groq(api_key=api_key)

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": "Explain the importance of fast language models",
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    print(chat_completion.choices[0].message.content)
