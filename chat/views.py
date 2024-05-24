import datetime, requests, logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from constants.constants import ACTION,ANSWER,ARGUMENTS,ASSISTANT,AUTHOR,CONTENT,DATA,EMBEDDING,ENDPT,ERROR,FMR,FUN_CALL,FUNCTION, INDEX,METH,MSG,NAME,ROLE,SUBJECTS,SYSTEM,TIMESTAMP,USER
from constants.messages import CHAT_HISTORY, QUERY_ERROR,QUERY_SUCCESS

from main import llm
from .serializers import GetSerialiser, PostSerialiser

class Chat(APIView):

    user = None
    apiURL = "/api/v1/chat/"

    def post(self, request, cid):
        serial = PostSerialiser(data=request.data)

        try:
            if not serial.is_valid():
                return Response(
                    {
                        MSG: serial.errors,
                        METH: "POST",
                        ENDPT: self.apiURL,
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            content = serial.validated_data.get(CONTENT)
            session = serial.validated_data.get("session")

            query = {
                ROLE: USER,
                CONTENT: content
            }

            response = llm.post(content)

            if(response.status_code == 200):
                print(response.json())


        except Exception as err:
            logging.error("%s: Error: %s", "500", err)
            return Response(
                {
                    MSG: QUERY_ERROR,
                    METH: "POST",
                    ENDPT: self.apiURL + cid,
                },
                status = status.HTTP_400_BAD_REQUEST
            )            


    def get(self, request, cid):
        serial = GetSerialiser(data=request.query_params)

        try:
            if not serial.is_valid():
                return Response(
                    {
                        MSG: serial.errors,
                        METH: "GET",
                        ENDPT: self.apiURL + cid,
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )
            
            sid = serial.validated_data.get("sid")
            pag = serial.validated_data.get("pag") or 1
            
            response = requests.get(
                f"https://ykw6lp7zg1.execute-api.ap-southeast-1.amazonaws.com/dev/chat/{cid}?sid={sid}&rec={pag}",
                # headers=self.header,
            )

            if response.status_code == 200:
                payload = response.json()
                messages = []

                for session in payload["Items"]:
                    messages.extend(session["payload"])
                
                return Response({
                    "session": 1, 
                    MSG: messages,
                    METH: "GET",
                    ENDPT: self.apiURL,
                })

            return Response({
                    "session": -1,
                    MSG: [],
                    METH: "GET",
                    ENDPT: self.apiURL,
                })
        except Exception as err:
            logging.error("%s: Error: %s", "500", err)
            return Response(
                {
                    MSG: QUERY_ERROR,
                    METH: "GET",
                    ENDPT: self.apiURL + cid,
                },
                status = status.HTTP_400_BAD_REQUEST
            )
            
    