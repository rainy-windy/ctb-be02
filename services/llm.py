from langchain.chat_models import ChatOpenAI
from langchain.prompts import MessagesPlaceholder, HumanMessagePromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationSummaryMemory, ConversationBufferMemory, FileChatMessageHistory
from langchain.chains import LLMChain, SequentialChain


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


