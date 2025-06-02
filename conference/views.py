from django.shortcuts import render
import time
from agora_token_builder import RtcTokenBuilder
from django.utils import timezone
from rest_framework.response import Response
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework import status
from .models import AgoraChannel,CallRecord
from firebase_admin import messaging, exceptions
from django.http import JsonResponse
from agora_token_builder import RtcTokenBuilder
from user.models import CustomUser,Pharmacy,IPatient,DoctorProfile,Doctor
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Doctor_Call_serve, Doctor, CallRecord
import json
from django.contrib.auth.decorators import user_passes_test, login_required
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View

AGORA_APP_ID = settings.AGORA_APP_ID
AGORA_APP_CERTIFICATE = settings.AGORA_APP_CERTIFICATE
AGORA_TOKEN_EXPIRATION_IN_SECONDS = 3600*2

class CallView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        user_id = request.user
        ppno = request.data.get("ppno", None)
        group_name = request.data.get("group")

        if group_name == 'pharmacy':
            try:
                user = Pharmacy.objects.get(id=user_id.id)
            except Pharmacy.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
            
        elif group_name == 'ipatient':
            try:
                user = IPatient.objects.get(id=user_id.id)
            except IPatient.DoesNotExist:
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        current_timestamp = int(time.time())
        channel_name = f"{user.phone_number}_{current_timestamp}"
        expiration_time_in_seconds = AGORA_TOKEN_EXPIRATION_IN_SECONDS
        privilege_expired_ts = current_timestamp + expiration_time_in_seconds

        token = RtcTokenBuilder.buildTokenWithUid(
            AGORA_APP_ID, AGORA_APP_CERTIFICATE, channel_name, 0,
            1,
            privilege_expired_ts
        )
        agora_channel = AgoraChannel.objects.create(
            channel_name=channel_name,
            token_no=token
        )

        available_doctor = DoctorProfile.get_available_doctor()
        
        if available_doctor:
            available_doctor.update_status('service') 
            call_type = 'direct'
            if group_name == 'pharmacy':
                call_instance = CallRecord.objects.create(
                    pharmacy_id=user,
                    agora_channel=agora_channel,
                    call_type=call_type,
                    status='initiated',
                    ppno=ppno,
                )
            elif group_name == 'ipatient':
                call_instance = CallRecord.objects.create(
                    patient_id=user,
                    agora_channel=agora_channel,
                    call_type=call_type,
                    status='initiated'
                )

            channel_layer = get_channel_layer()
            print("Sending WebSocket message to group:", f'doctor_call_notifications_{available_doctor.doctor_field.id}')
            async_to_sync(channel_layer.group_send)(
                f'doctor_call_notifications_{available_doctor.doctor_field.id}', 
                {
                    'type': 'send_call_notification',
                    'data': {
                        'id':call_instance.id,
                        'user': user.phone_number,
                        'call_type': call_type,
                        'status': 'initiated',
                        'ppno': ppno,
                        'channel_name': channel_name,
                        'token': token,
                        'group': group_name
                    }
                }
            )

        # No doctor is available, schedule the call and notify all doctors
        else:
            call_type = 'scheduled'
            if group_name == 'pharmacy':
                call_instance = CallRecord.objects.create(
                    pharmacy_id=user,
                    agora_channel=agora_channel,
                    call_type=call_type,
                    status='scheduled',
                    ppno=ppno,
                )
            elif group_name == 'ipatient':
                call_instance = CallRecord.objects.create(
                    patient_id=user,
                    agora_channel=agora_channel,
                    call_type=call_type,
                    status='scheduled'
                )
            
            # Notify all doctors about the scheduled call
            channel_layer = get_channel_layer()
            print("Sending WebSocket message to group:", f'doctor_call_notifications_unavailable')
            async_to_sync(channel_layer.group_send)(
                'doctor_call_notifications_all',  # Broadcast to all doctors
                {
                    'type': 'send_call_notification',
                    'data': {
                        'id':call_instance.id,
                        'user': user.phone_number,
                        'call_type': call_type,
                        'status': 'scheduled',
                        'ppno': ppno,
                        'channel_name': channel_name,
                        'token': token,
                        'group': group_name
                    }
                }
            )
            
        return Response({
            "call_instance":call_instance.id,
            "channel_name": channel_name,
            "token": token,
            "call_type": call_type,
            "expiration": timezone.now() + timezone.timedelta(seconds=expiration_time_in_seconds)
        }, status=status.HTTP_200_OK)

def send_push_notification(token, priority="high"):
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title="Notification Title",
                body="Notification Body",
            ),
            token=token, 
            android=messaging.AndroidConfig(
                priority=priority 
            ),
            apns=messaging.APNSConfig(
                headers={
                    'apns-priority': '10' if priority == 'high' else '5' 
                }
            )
        )
        response = messaging.send(message)
        return {"success": True, "response": response}
    except exceptions.NotFoundError as not_found_error:
        # Handle specific FCM not found error
        print(f"FCM Not Found Error: {not_found_error}")
        return {"success": False, "error": str(not_found_error)}
    except exceptions.FirebaseError as firebase_error:
        # Handle general Firebase errors
        print(f"Firebase error: {firebase_error}")
        return {"success": False, "error": str(firebase_error)}
    except Exception as e:
        # Catch any other exceptions and log them
        print(f"General error: {str(e)}")
        return {"success": False, "error": str(e)}


@login_required(login_url='login_page')

@csrf_exempt
def call_back(request):
    doctor_id = request.user.id
    doctor = Doctor.objects.get(id=doctor_id)
    try:
        phone_number = request.POST.get('phone_number')
        call_record_id = request.POST.get('voiceCallId')
        call_record_instance= CallRecord.objects.get(id=call_record_id)

        if not phone_number:
            return JsonResponse({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        user = get_object_or_404(CustomUser, phone_number=phone_number)

        doctor_call_serve = Doctor_Call_serve(doctor=doctor, call_record=call_record_instance)
        doctor_call_serve.save()

        try:
            f_token = user.user_f_token.fcm_token
            print(f"User's FCM token: {f_token}")
        except CustomUser.user_f_token.RelatedObjectDoesNotExist:
            return JsonResponse({"error": "User device token not found."}, status=status.HTTP_404_NOT_FOUND)
        
        result = send_push_notification(f_token)
        if result["success"]:
            print("Push notification sent successfully.")
            return JsonResponse({"success": result["response"]}, status=status.HTTP_200_OK)
        else:
            print(f"Push notification failed: {result['error']}")
            # Return the error from FCM
            return JsonResponse({"error": result["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    except Exception as e:
        print(f"Unexpected error in call_back: {str(e)}")
        return JsonResponse({"error": "Internal server error", "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@csrf_exempt 
@login_required(login_url='login_page')
def add_doctor_call(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            call_record_id = data.get('call_record_id')
            doctor_id = request.user
            doctor = Doctor.objects.get(id=doctor_id.id)
            call_record_instance= CallRecord.objects.get(id=call_record_id)
            doctor_call_serve = Doctor_Call_serve(doctor=doctor, call_record=call_record_instance)
            doctor_call_serve.save()
            return JsonResponse({
                "doctor_call_serve_id": doctor_call_serve.id
            }, status=201)
        except Doctor.DoesNotExist:
            return JsonResponse({"error": "Doctor not found for this user"}, status=404)
        except CallRecord.DoesNotExist:
            return JsonResponse({"error": "CallRecord not found"}, status=404)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request method"}, status=400)


# class QueuePositionView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, user_type):
#         user_id = request.user.id  # Get the authenticated user's ID
#         # Get the queue position for the user
#         queue_position = CallRecord.get_queue_position(user_id=user_id, user_type=user_type)

#         if queue_position is not None:
#             channel_layer = get_channel_layer()
#             print("Sending WebSocket message to group:", f'doctor_call_notifications_{available_doctor.doctor_field.id}')
#             async_to_sync(channel_layer.group_send)(
#                 f'queue_updates_{user_type}_{user_id}',
#                 {
#                     'type': 'send_queue_position',
#                     'queue_position': queue_position
#                 }
#             )
#             return Response({"queue_position": queue_position}, status=status.HTTP_200_OK)
#         else:
#             return Response({"error": "No active calls found."}, status=status.HTTP_404_NOT_FOUND)
        

class UpdateCallStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        call_id = request.data.get("call_id")
        new_status = request.data.get("call_status")
        if new_status not in ['initiated', 'in_progress', 'ended', 'missed', 'scheduled']:
            return Response({"error": "Invalid status."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            call_record = CallRecord.objects.get(id=call_id)
            if call_record:
                call_record.status = new_status
                call_record.save()
                try:
                    # Notify doctors or perform other actions
                    self.notify_doctors_status_update(call_record)
                except Exception as e:
                    print("Error notifying doctors:", e)
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                return Response({
                    "message": "Call status updated successfully.",
                    "status": new_status
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Call record not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def notify_doctors_status_update(self, call_record):
        channel_layer = get_channel_layer()
        # Prepare the status update data to be sent to doctors
        status_update_data = {
            "call_id": call_record.id,
            "new_status": call_record.status
        }
        # Send the status update to the WebSocket group for all doctors
        async_to_sync(channel_layer.group_send)(
            "doctor_call_notifications_all",  # Group name that all doctors are subscribed to
            {
                "type": "send_call_status_update",  # Function in the WebSocket consumer to handle the event
                "data": status_update_data  # Data to send
            }
        )
@method_decorator(csrf_exempt, name='dispatch')
class UpdateCallWebStatusView(View):
    def post(self, request, *args, **kwargs):
        call_id = request.POST.get("call_id")
        new_status = request.POST.get("call_status")

        # Check for valid status
        if new_status not in ['initiated', 'in_progress', 'ended', 'missed', 'scheduled']:
            return JsonResponse({"error": "Invalid status."}, status=400)

        try:
            # Fetch the call record based on the call ID
            call_record = get_object_or_404(CallRecord, id=call_id)
            print(call_record)
            
            # Update the call status
            call_record.status = new_status
            call_record.save()

            try:
                # Notify doctors or perform other actions
                self.notify_doctors_status_update(call_record)
            except Exception as notify_error:
                print("Error notifying doctors:", notify_error)
                return JsonResponse({"error": "Failed to notify doctors."}, status=500)

            # Return a successful response
            return JsonResponse({
                "success": True,  # Add success property
                "message": "Call status updated successfully.",
                "status": new_status
            }, status=200)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    def notify_doctors_status_update(self, call_record):
        channel_layer = get_channel_layer()
        # Prepare the status update data to be sent to doctors
        status_update_data = {
            "call_id": call_record.id,
            "new_status": call_record.status
        }
        # Send the status update to the WebSocket group for all doctors
        async_to_sync(channel_layer.group_send)(
            "doctor_call_notifications_all",  # Group name that all doctors are subscribed to
            {
                "type": "send_call_status_update",  # Function in the WebSocket consumer to handle the event
                "data": status_update_data  # Data to send
            }
        )
        
