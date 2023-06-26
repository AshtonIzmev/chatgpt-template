import yaml

with open('prompts/prompt_feedback.yml', 'r') as f:
    yml_feedback = yaml.safe_load(f)

########
# FEEDBACK
########
def get_feedback_conversation_prompt(context):
    return [
        {"role": "system", "content": yml_feedback['prompts']['base']['system'].replace("$CONTEXTE", context)},
        {"role": "assistant", "content": yml_feedback['prompts']['base']['assistant']},
        ]

def get_feedback_summarizer_prompt(conversation):
    return [{"role": "assistant", "content": yml_feedback['prompts']['monitoring']['summarizer'].replace("$CONVERSATION", conversation)}]