import time
from openai import OpenAI

# Enter your Assistant ID here.
ASSISTANT_ID = "asst_OdboRIxKhLQrirwYRHZFhyZd"

# Make sure your API key is set as an environment variable.
client = OpenAI(api_key="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")


def mini_btc_assistant(question):
    # Create a thread with a message.
    if len(question) > 40:
        return "This question is too long please make it a bit shorter"
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                # Update this with the query you want to use.
                "content": "limit your response to 45 words : " + str(question),
            }
        ]
    )

    # Submit the thread to the assistant (as a new run).
    run = client.beta.threads.runs.create(thread_id=thread.id, assistant_id=ASSISTANT_ID)
    print(f" Run Created: {run.id}")

    # Wait for run to complete.
    while run.status != "completed":
        run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
        print(f" Run Status: {run.status}")
        time.sleep(1)
    else:
        print(f" Run Completed!")

    # Get the latest message from the thread.
    message_response = client.beta.threads.messages.list(thread_id=thread.id)
    messages = message_response.data

    # Print the latest message.
    latest_message = messages[0]
    return "Ai Response : " + latest_message.content[0].text.value.replace("【7†source】", "")


print(mini_btc_assistant("what price can mini bitcoin reach?"))
