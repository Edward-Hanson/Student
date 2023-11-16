from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import json
from django.contrib.auth.decorators import login_required

from accounts.models import CustomUser, Student_Interest
from .models import Room

@login_required
def get_interest(request):
    user=request.user
    if not user.room:
        selected_interests= request.POST.get('selected_interests')
        my_list = json.loads(selected_interests)
        for item in my_list:
            interest = Student_Interest.objects.create(interest=item,student=user)
        return redirect('pairs')
    return redirect("view_room")

def send_mail(user):
    recipient_email = user.student_mail

    email = EmailMessage(
    subject='KINDRED HOSTELS',
    body=f'You have successfully booked a room, Check your portal for more information',
    from_email="ehanson787@gmail.com",
    to=[recipient_email],
             )
    email.send()
                      
@login_required
def pairs(request):
    user= request.user
    user_interests = user.interests.all()
    Rooms = Room.objects.all()
    
    if not user.room:
        for room in Rooms:
            if room.students.count()>=4:
                continue
            else:
                if room.room_interest=="":
                    room.students.add(user)
                    interests = ''
                    user_interests= list(user.interests.values_list('interest',flat=True))
                    for item in user_interests:
                        interests = interests + "|" +item
                    room.room_interest = interests
                    room.save()
                    send_mail(user)
                    return render(request,'pairs.html',{'room':room,'user':user})
                else:
                    user_interests= list(user.interests.values_list('interest',flat=True))
                    room_interests = room.room_interest.split("|")
                    room_interests_refined = [item for item in room_interests if item.strip()!=""]
                    common_interest= list(set(user_interests).intersection(set(room_interests_refined)))
                    if len(common_interest)>1:
                        room.students.add(user)
                        interest=''
                        for item in common_interest:
                            interest = interest + "|" + item
                        room.room_interest = interest
                        room.save()
                        send_mail(user)
                        return render(request,'pairs.html',{'room':room,'user':user})
    
                    continue
    return redirect('view_room')

@login_required
def view_room(request):
    user=request.user
    room =  user.room
    interests = room.room_interest.split("|")
    room_interests= [item for item in interests if item.strip()!=""]
    return render(request,'view.html',{'room':room,'room_interests':room_interests})
    
