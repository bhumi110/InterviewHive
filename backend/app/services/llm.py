import os
import time

from groq import Groq
from dotenv import load_dotenv


load_dotenv()


client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def generate_response(
    messages,
    model="openai/gpt-oss-120b",
    temperature=0.3,
    max_tokens=1000,
    max_retries=3
):
    """
    Central LLM service.

    All agents will eventually use this function
    instead of calling Groq directly.
    """

    for attempt in range(max_retries):

        try:

            response = client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content

        except Exception as e:

            error_message = str(e).lower()

            if (
                "rate limit" in error_message
                or "429" in error_message
            ):

                wait_time = 5 * (attempt + 1)

                print(
                    f"Rate limit reached. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                raise e

    raise RuntimeError(
        "Groq API rate limit persisted after retries."
    )