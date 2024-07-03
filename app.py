import os

import streamlit as st
from openai import OpenAI
import time

from open_ai_vector_store_loader import get_vector_store_id_by_name

if 'client' not in st.session_state:
    st.session_state.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

if 'vector_store_id' not in st.session_state:
    st.session_state.vector_store_id = get_vector_store_id_by_name("ArcelorMittal")

if "assistant" not in st.session_state:
    st.session_state.assistant = st.session_state.client.beta.assistants.create(
        instructions="You are Olga you are a very kind and friendly AI assistant. You are an employee at the "
                     "company Arcelormittal and your are a recruiter for the company. Your goal is to promote a "
                     "good image for the company and answer any questions that the user may have about the company."
                     "As a second role your job is also to ask about peoples skills, experience or interest, when you" 
                     "gathered some information propose some open vacancies that you can find in uploaded documents."
                     "You are currently standing at a job fair in belgium.",
        name="Documents Assistant",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": [st.session_state.vector_store_id]}},
        model="gpt-3.5-turbo",
    )


# ===============================

def run_assistant(
        message_body):  # Create a message, run the assistant on it, monitor it for completion, and display the output
    # Create a message in an existing thread
    message = st.session_state.client.beta.threads.messages.create(
        thread_id=st.session_state.thread.id,
        role="user",
        content=message_body,
    )

    # Run the existing assistant on the existing thread
    run = st.session_state.client.beta.threads.runs.create(
        thread_id=st.session_state.thread.id,
        assistant_id=st.session_state.assistant.id,
    )

    # Monitor the assistant and report status
    while run.status != "completed":
        run = st.session_state.client.beta.threads.runs.retrieve(
            thread_id=st.session_state.thread.id,
            run_id=run.id
        )
        time.sleep(.5)

    # Extract the messages from the thread
    messages = st.session_state.client.beta.threads.messages.list(
        thread_id=st.session_state.thread.id
    )

    # Display the output
    # for message in reversed(messages.data):
    #     print(message.role + ": " + message.content[0].text.value)
    return messages


# ************************
if 'thread' not in st.session_state:
    st.session_state.thread = st.session_state.client.beta.threads.create()

st.title("ArcelorMittal")

print('init')
# check for messages in session and create if not exists
if "messages" not in st.session_state.keys():
    st.session_state.messages = None
    print('init')

# Display all messages


user_prompt = st.chat_input()

if user_prompt is not None:
    # st.session_state.messages.append({"role": "user", "content": user_prompt})
    if st.session_state.messages:
        for message in reversed(st.session_state.messages.data):
            with st.chat_message(message.role):
                st.write(message.content[0].text.value)
    with st.chat_message("user"):
        st.write(user_prompt)
    st.session_state.messages = run_assistant(user_prompt)
    if st.session_state.messages:
        with st.chat_message(st.session_state.messages.data[0].role):
            st.write(st.session_state.messages.data[0].content[0].text.value)

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write("🌟 I'm Olga, your helpful AI assistant from Arcelormittal, here to guide you through the world of "
                 "of ArcelorMittal and guide you trough opportunities at our company! 🚀")
    print("finished request")

    # breakpoint()

# print('sessstae')
# print(st.session_state.messages)
# if st.session_state.messages:
#     for i, message in enumerate(reversed(st.session_state.messages.data)):
#         if i == len(st.session_state.messages.data) - 2:
#             continue
#         with st.chat_message(message.role):
#             st.write(message.content[0].text.value)
# else:
#     print('else')
#     with st.chat_message('user'):
#         st.write('some')

# print("thread_id:", thread.id, "assistant_id:", assistant.id)
#
# while True:
#     user_input = input("Enter a question, or type 'exit' to end: ").strip().lower()
#     if user_input == 'exit':
#         break
#     else:
#         run_assistant(user_input)
