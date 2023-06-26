from gpt.gpt import get_chatgpt_response
from database.datafuncs import get_user_conversation_session_data, get_last_summary_context, get_user_conversation_history
from prompts.prompt import get_feedback_conversation_prompt, get_feedback_summarizer_prompt

def generate_prompt_base(user, session):
    conversation_prompt = [ {"role": c[4], "content": c[3]} for c in get_user_conversation_session_data('feedback', user, session) ]
    context = get_last_summary_context(user)
    if len(context) == 0:
        clean_context = "Pas de contexte"
    else:
        clean_context = context[0][0]
    return get_feedback_conversation_prompt(clean_context) + conversation_prompt

def generate_new_conversation_context(user):
    conversation_prompt = [ c[4].capitalize() + ": " + c[3] for c in get_user_conversation_history('feedback', user) ]
    prompt_summary = get_feedback_summarizer_prompt('\n'.join(conversation_prompt))
    return get_chatgpt_response(prompt_summary, user, top_p_val=0.5)

def get_chatgpt_feedback_response(user, session, jawab):
    prompt = generate_prompt_base(user, session)
    # Has been done like this because OpenAI APIs are often down and we do not want to log the user response (jawab) in the database before being sure we can have a response from OpenAI
    # Workaround instead of using table atomic writes
    prompt_with_temp_response = prompt + [{"role": "user", "content": jawab}]
    return get_chatgpt_response(prompt_with_temp_response, user, top_p_val=0.5)
