import requests
from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationSummaryMemory, ConversationBufferMemory, FileChatMessageHistory
from langchain.chains import LLMChain, SequentialChain


from constants.constants import AUTHORISATION, ACCESS, GPT_URL, USERNAME, PASSWORD

# This is the external LLM
class LLM():

    def __new__(c, key=None):
        if not hasattr(c, "instance"):
            c.instance = super(LLM, c).__new__(c)
            return c.instance
        

    def __init__(self, key=None):
        self.chat = ChatOpenAI(
            openai_api_key = key,
            verbose = True
        )

        self.memory = ConversationSummaryMemory(
            # chat_memory = FileChatMessageHistory("messages.json"),
            llm = self.chat,
            memory_key="messages", 
            return_messages=True
        )

        self.prompt = ChatPromptTemplate(
            input_variables = ["content", "messages"],
            messages = [
                MessagesPlaceholder(variable_name="messages"),
                HumanMessagePromptTemplate.from_template("{content}")
            ]
        )

        self.chain = LLMChain(
            llm = self.chat,
            prompt = self.prompt,
            memory = self.memory,
            verbose = True
        )
        
        print("\nLLM Initilialised\n")


    def post(self, content):
        try:
            result = self.chain({
                "content": content
            })
            return result
        except Exception as error:
            print(error)



# This is the internal LLM – Secure GPT
class SGPT():

    token = None
    baseURL = GPT_URL
    header = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }


    def __new__(c):
        if not hasattr(c, "instance"):
            c.instance = super(SGPT, c).__new__(c)
            return c.instance
        

    def __init__(self, user: str, password: str):
        if(self.token is not None):
            self.header[AUTHORISATION] = f"Bearer {self.token}"

            response = requests.get(
                f"{self.baseURL}/auth/validate", 
                headers= self.header, 
                verify=False
            )

            if not response.status_code == 200:
                print("\nToken is invalid. Logging in now. . .\n")
                self.login(user, password)
                return
            
        else:
            self.login(user, password)


    def login(self, user: str, password: str):
        try:
            response = requests.post(
                f"{self.baseURL}/auth/login", 
                json = {
                    USERNAME: user,
                    PASSWORD: password,
                },
                verify=False
            )

            if not response.status_code == 200:
                raise Exception("Credentials missing or incorrect.")
            else:
                tokens = response.json()
                self.token = tokens[ACCESS]
                self.header[AUTHORISATION] = f"Bearer {tokens[ACCESS]}"

                file = open(".env", "w+")
                file.write(f"export USERNAME={self.credential[USERNAME]}\nexport PASSWORD={self.credential[PASSWORD]}\nexport TOKEN={tokens[ACCESS]}")
                file.close()

        except ConnectionError as error:
            raise Exception(f"Failed to to establish connection to {self.baseURL}.\n{error}.\n")
        