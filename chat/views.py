import datetime, json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from constants.constants import ACTION,ANSWER,ARGUMENTS,ASSISTANT,AUTHOR,CONTENT,DATA,EMBEDDING,ENDPT,ERROR,FMR,FUN_CALL,FUNCTION, INDEX,METH,MSG,NAME,ROLE,SUBJECTS,SYSTEM,TIMESTAMP,USER
from constants.messages import CHAT_HISTORY, QUERY_ERROR,QUERY_SUCCESS


class Chat(APIView):

    user = None
    apiURL = "/api/v1/chat"


    def get(self, request, format=None):
        now = datetime.datetime.now()
        last = now - datetime.timedelta(hours = 13)
        try:

            return Response(
                {
                    MSG: [],
                    METH: "GET",
                    ENDPT: self.apiURL,
                })
        except Exception as error:
            return Response(
                {
                    MSG: QUERY_ERROR,
                    METH: "GET",
                    ENDPT: self.apiURL,
                },
                status = status.HTTP_400_BAD_REQUEST
            )
            
    