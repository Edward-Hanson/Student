from django.shortcuts import render
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponse
import json
import ast

from accounts.models import CustomUser, Student_Interest
from .models import Room



def pair_students(request):
    user=request.user
    selected_interests= request.POST.get('selected_interests')
    my_list = json.loads(selected_interests)
    for item in my_list:
        interest = Student_Interest.objects.create(interest=item,student=user)
    Rooms = Room.objects.all()
    print("Rooms:",user.room)
    if user.room==None:
        print("Hiiiiii")
        if user.interests.count()>=3:
            print("count validation of interest")
            for room in Rooms:
                print("room interest: ", type(room.room_interest))
                if room.room_interest=="":
                    print("line29")
                    room.students.add(user)
                    user_interests= list(user.interests.values_list('interest',flat=True))
                    interests = ''
                    for item in user_interests:
                        interests = interests + "|" +item
                    room.room_interest = interests
                    room.save()
                    return render(request,'pairs.html',{'room':room,'user':user})
                elif room.students.count()==4:
                    continue
                else:
                    print("line41")
                    user_interests= list(user.interests.values_list('interest',flat=True))
                    room_interests = room.room_interest.split("|")
                    room_interests_refined = [item for item in room_interests if item.strip()!=""]
                    common_interest= list(set(user_interests).intersection(set(room_interests_refined)))
                    print("common interest: ",common_interest)
                    if len(common_interest)>1:
                        print("line 46")
                        interest= ''
                        if room.students.count()==1: 
                            print("line 48")
                            for item in common_interest:
                                interest = interest + "|" + item
                            room.room_interest = interest
                            room.save()
                        room.students.add(user)
                        
                        #send mail
                        user = request.user
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

