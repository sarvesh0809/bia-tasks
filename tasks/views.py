from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Item
from .serializers import ItemSerializer,UserCredentialsSerializer,VideoGenerationSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from io import BytesIO
import base64
import cv2,imageio  
from pytube import YouTube

def task(request):
    return render(request,'task.html')

#  Task 1:

def task1(request):
    return HttpResponse("<h1 style='text-align: center;margin-top:5em;'>Hello, Django!</h1>")


# Task 2 & 3 combined:

class Task3(generics.ListCreateAPIView):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


#  Task 4:
    
users={
'boston':'boston123',
'user1':'1234',
'user2':'5678',
}
class Task4(APIView):
    serializer_class = UserCredentialsSerializer
    def get_serializer(self, *args, **kwargs):
        return self.serializer_class()
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        if username in users and users[username] == password:
            refresh = RefreshToken()
            refresh.access_token.payload['sub'] = username
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            return Response({
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, status=status.HTTP_200_OK)    
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    


# Task 5:
    
class Task5(APIView):
    serializer_class = VideoGenerationSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        youtube_url = serializer.validated_data['url']
        title = serializer.validated_data['title']
        youtube_video = YouTube(youtube_url)
        video_stream = youtube_video.streams.filter(file_extension="mp4").first()
        video_path = video_stream.download()


        cap = cv2.VideoCapture(video_path)

        width = int(cap.get(3))
        height = int(cap.get(4))

        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        text_color = (255, 255, 255)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            text_size = cv2.getTextSize(title, font, font_scale, font_thickness)[0]
            text_x = (width - text_size[0]) // 2
            text_y = (height + text_size[1]) // 2
            cv2.putText(frame, title, (text_x, text_y), font, font_scale, text_color, font_thickness)

            frames.append(frame)

        cap.release()

        video_buffer = BytesIO()
        imageio.mimsave(video_buffer, frames, format='mp4', fps=30)

        video_base64 = base64.b64encode(video_buffer.getvalue()).decode('utf-8')
        response = HttpResponse(content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="video.mp4"'
        response.write(base64.b64decode(video_base64))

        return response