import os
import re
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.prompts import ChatPromptTemplate

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def select_categories_for_user(user_id):
    from .models import UserInterestResponse
    from userprofile.models import Category

    user_answers = UserInterestResponse.objects.filter(user_id=user_id)
    if not user_answers.exists():
        return {"error": "No responses found for this user."}

    question_responses = [
        f"Question: {answer.question.text}, Response: {'Yes' if answer.response else 'No'}"
        for answer in user_answers
    ]
    input_text = "\n".join(question_responses)

    available_categories = Category.objects.values_list("name", flat=True)
    category_list = ", ".join(available_categories)

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "You are an AI that selects categories based on user responses."),
        ("user", "User answered the following questions:\n\n{input_text}\n\n"
                 "Select exactly 7 categories from this list: {category_list}. "
                 "Choose only from the provided list.")
    ])

    chat = init_chat_model("gpt-4o" , model_provider="openai")

    formatted_prompt = prompt_template.format(input_text=input_text, category_list=category_list)
    response = chat.invoke(formatted_prompt)

    selected_categories = [re.sub(r"^\d+\.\s*", "", c.strip()) for c in response.content.split("\n") if c.strip()]

    valid_categories = Category.objects.filter(name__in=selected_categories)[:7]



    return [category.name for category in valid_categories]

