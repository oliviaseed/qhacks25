import openai

def test_openai_api(api_key, organization, model="gpt-3.5-turbo"):
    """
    Test script for the OpenAI API with organization support.

    Parameters:
        api_key (str): Your OpenAI API key.
        organization (str): Your OpenAI organization ID.
        model (str): The model to test. Default is "gpt-3.5-turbo".

    Returns:
        None
    """
    try:
        # Set up the OpenAI API key and organization
        openai.api_key = api_key
        openai.organization = organization

        # Define a simple test prompt
        messages = [{"role": "user", "content": "Write a short poem about the sunrise."}]

        print(f"Sending request to OpenAI API with model: {model}\n")

        # Send a request to the OpenAI API
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            max_tokens=50,
            temperature=0.7
        )

        # Extract and print the generated response
        text = response.choices[0].message["content"].strip()
        print(f"Response:\n{text}\n")

    except openai.error.AuthenticationError:
        print("Authentication failed. Please check your API key and organization ID.")

    except openai.error.OpenAIError as e:
        print(f"An error occurred with the OpenAI API: {e}")

if __name__ == "__main__":
    # Replace 'your-api-key' and 'your-organization-id' with your actual OpenAI API key and organization ID
    # api_key = "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"
    # organization = "org-wpYzzvYaFPDDhehFs2lYy4d1"

    # Run the test script
    test_openai_api(api_key, organization)
