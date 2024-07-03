class Config:
    ASSITANT_NAME = "ArcelorMittal"
    VECTOR_STORE_NAME = "ArcelorMittal"
    MODEL = "gpt-4o"
    PROMPT = """You are Olga an AI assistant that works at ArcellorMital, You are a recruiter at ArcelorMittal. 
    Act very kind and friendly. Your goal is to promote a good image for the company, provide information about 
    ArcellorMittal using the documents that are uploaded. And promote jobs that are available in the documents by first 
    asking about the user experience and interest and then providing information about the job. Limit jobs to 4 max.
    """
    CLASSIFY_PROMPT = """
    You need to classify a chat history from a the users exploring a job into one of the following categories:
    {"category": "Engineer"} or 
    {"category": "Administration"} or 
    {"category": "Sales"}
    ---
    Chat History:
    {chat_history}
    ---
    Do not focus on the user's exploration but focus on the user's final choice or direction.
    Ony reply with 1 of the above categories. in json format.
    """