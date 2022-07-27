import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PatchNotesList(APIView):

    def get(self, request):
        # List versions
        versions = os.listdir("patchnotes/patchnotes")
        versionJSONList = []

        for version in versions:
            with open("patchnotes/patchnotes/"+version) as file:
                jsonData = json.load(file)
                versionJSONList.append(jsonData)

        return Response(versionJSONList, status=status.HTTP_200_OK)

class PatchNotesGet(APIView):

    def get(self,request, version):
        try:
            with open(f"patchnotes/patchnotes/{version}.json") as file:
                jsonData = json.load(file)
        except FileNotFoundError:
            return Response({"Error":"File not found for version specified"}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(jsonData, status=status.HTTP_200_OK)