from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import UserRegistrationForm, UserVerificationForm
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from twilio.rest import Client
from django.conf import settings
import random
import string


def generate_verification_code(length=6):
    # Generate a random code of the specified length
    return ''.join(random.choices(string.digits, k=length))


def send_verification_sms(phone_number, verification_code):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body=f'Your verification code is: {verification_code}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )


class UserRegistration(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={200: UserResponseSerializer()},
        operation_summary="Summary of your API endpoint",
        operation_description="Description of your API endpoint",
    )
    def post(self, request):
        form = UserRegistrationForm(request.data)

        if form.is_valid():
            user = form.save()
            user.save()

            request.session['phone'] = request.data['phone']

            # Create a UserVerification record
            verification_code = generate_verification_code()
            user_verification = UserVerification(
                user=user,
                phone=request.data['phone'],
                verification_code=verification_code,
            )
            user_verification.save()

            # Send the verification code via SMS
            send_verification_sms(request.data['phone'], verification_code)

            return redirect(reverse('user-verification'))

        response_data = {'message': 'User registration failed'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        query_serializer=UserSerializer(),
        operation_summary="Summary of GET parameters"  # Use UserSerializer for query parameters
    )
    def get(self, request):
        # Render the registration form
        form = UserRegistrationForm()
        return render(request, 'users/registration.html', {'form': form})


class Verification(APIView):
    @swagger_auto_schema(
        responses={
            200: VerificationFormResponseSerializer(),  # Use your form response serializer
        },
        operation_summary="Show Verification Form",
        operation_description="Display the verification form to verify a user."
    )
    def get(self, request):
        # Get the phone number from the session
        phone_number = request.session.get('phone', '')

        # Render the verification form with the phone number
        form = UserVerificationForm(phone=phone_number)
        return render(request, 'users/verification.html', {'form': form})

    @swagger_auto_schema(
        request_body=VerificationRequestSerializer,
        responses={
            200: VerificationResponseSerializer(),
            400: VerificationErrorResponseSerializer(),
        },
        operation_summary="Verify User",
        operation_description="Verify a user by providing the phone number and verification code."
    )
    def post(self, request):
        # Get the phone number from the session
        phone_number = request.session.get('phone', '')

        form = UserVerificationForm(request.POST, phone=phone_number)

        if form.is_valid():
            phone_number = form.cleaned_data['phone']
            verification_code = form.cleaned_data['verification_code']

            try:
                user_verification = UserVerification.objects.get(
                    phone_number=phone_number,
                    verification_code=verification_code,
                    attempts_remaining__gt=0,
                    verified=False,
                )

                # Mark the user as verified and save
                user_verification.user.verified = True
                user_verification.user.save()
                user_verification.verified = True
                user_verification.save()

                # Redirect to the home page upon successful verification
                return redirect(reverse('user-success'))
            except UserVerification.DoesNotExist:
                form.add_error('verification_code', 'Invalid verification code')

        return render(request, 'users/verification.html', {'form': form})


class HomePage(APIView):
    @swagger_auto_schema(
        responses={
            200: HomePageResponseSerializer(),
        },
        operation_summary="List Verified Users",
        operation_description="Get a list of all verified users."
    )
    def get(self, request):
        print("HomePage view is executed")
        # Fetch all verified users
        verified_users = UserVerification.objects.filter(verified=True).select_related('user')

        # Serialize the user data using your UserVerificationSerializer
        serializer = UserVerificationSerializer(verified_users, many=True)

        # Pass the verified_users context variable to the 'success.html' template
        return render(request, 'users/success.html', {'verified_users': serializer.data})

    @swagger_auto_schema(
        request_body=CreateUserSerializer,
        responses={
            200: HomePageResponseSerializer(),
        },
        operation_summary="Create a New User",
        operation_description="Create a new user with the provided data."
    )
    def post(self, request):
        return render(request, 'users/registration.html')
