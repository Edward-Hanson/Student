from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import json

from accounts.models import CustomUser, Student_Interest
from .models import Room


def get_interest(request):
    user=request.user
    selected_interests= request.POST.get('selected_interests')
    my_list = json.loads(selected_interests)
    for item in my_list:
        interest = Student_Interest.objects.create(interest=item,student=user)
    return redirect('pairs')

def pairs(request):
    user= request.user
    user_interest = user.interests.all()
    Rooms = Room.objects.all()
    
    if not user.room:
        for room in Rooms:
            if room.students.count()>=4:
                continue
            
            else:
                if room.room_interest=="":
                    room.students.add(user)
                    interests = ''
                    for item in user_interests:
                        interests = interests + "|" +item
                    room.room_interest = interests
                    room.save()
                    return render(request,'pairs.html',{'room':room,'user':user})
                else:
                    user_interests= list(user.interests.values_list('interest',flat=True))
                    room_interests = room.room_interest.split("|")
                    room_interests_refined = [item for item in room_interests if item.strip()!=""]
                    common_interest= list(set(user_interests).intersection(set(room_interests_refined)))
                    if len(common_interest)>1:
                        room.students.add(user)
                        if room.students.count()==2:
                            interest=''
                            for item in common_interest:
                                interest = interest + "|" + item
                            room.room_interest = interest
                            room.save()
                    continue
                        
                        #send mail
                        recipient_email = user.student_mail

                        email = EmailMessage(
                        subject='KINDRED HOSTELS',
                        body=f'You have successfully booked a room, Check your portal for more information',
                        from_email="ehanson787@gmail.com",
                        to=[recipient_email],
                                         )
                        email.attach_file()
                        email.send()
                        return render(request,'pairs.html',{'room_interest':room_interests,'room':room,'user':user})
        else:
            return redirect('interests')
            messages.info(request,"You already have a room, you can not book more room")
    return redirect('interests')

