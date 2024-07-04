import os

import streamlit as st
from openai import OpenAI
import time
from config import Config

from assitant import Assistant

if 'client' not in st.session_state:
    st.session_state.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

if "assistant" not in st.session_state:
    assistant = Assistant()
    st.session_state.assistant = assistant.get_assistant()


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

# add history to chat
if st.session_state.messages:
    for message in reversed(st.session_state.messages.data):
        with st.chat_message(message.role):
            st.write(message.content[0].text.value)

if user_prompt is not None:
    # st.session_state.messages.append({"role": "user", "content": user_prompt})
    # # add history to chat
    # if st.session_state.messages:
    #     for message in reversed(st.session_state.messages.data):
    #         with st.chat_message(message.role):
    #             st.write(message.content[0].text.value)
    # add user prompt to chat
    with st.chat_message("user"):
        st.write(user_prompt)
    st.session_state.messages = run_assistant(user_prompt)
    # add response to chat
    if st.session_state.messages:
        with st.chat_message(st.session_state.messages.data[0].role):
            st.write(st.session_state.messages.data[0].content[0].text.value)

if not st.session_state.messages:
    with st.chat_message("assistant"):
        st.write("🌟 I'm Olga, your helpful AI assistant from Arcelormittal. Do you have questions about the company or jobs? Shoot! 🚀")
    print("finished request")

# options = ["What do we make?", "What are our value?", "What we do for Climate Change?"]
# columns = list(zip(options, st.columns(3)))
# for option, col in columns:
#     with col:
#         if st.button(option, use_container_width=True):
#             print(option)
if st.button("Go to Job Training!", type="primary"):
    response = st.session_state.client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": Config.CLASSIFY_PROMPT
                    }
                ]
            },
        ],
        temperature=0,
        max_tokens=25,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        response_format={"type": "json_object"},
    )
    response_message = response.choices[0].message.content
    print(response_message)

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
