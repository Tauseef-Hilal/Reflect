import logging
import openai

from .env import OPENAI_API_KEY

# Configuration
openai.api_key = OPENAI_API_KEY


def openai_request(prompt: str) -> str:

    try:
        res = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            temperature=0.2
        )
        print(type(res))
        print(res)
    except openai.error.ServiceUnavailableError:
        return "We are at capacity right now! Please try again later"
    except Exception as e:
        logging.error(e)
        return "OOPS: Some error occured"

    return res.json()["choices"][0]["text"].strip()
