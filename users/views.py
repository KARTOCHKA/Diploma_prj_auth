from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import UserRegistrationForm, UserSMSVerificationForm
from .permissions import IsVerifiedUser
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render, redirect
from twilio.rest import Client
from django.conf import settings
import random
import string


def generate_verification_code(length=6):
    """
    Generate a random code of the specified length.

    Parameters:
        length (int): The length of the code to be generated. Defaults to 6.

    Returns:
        str: The generated random code.
    """
    # Generate a random code of the specified length
    return ''.join(random.choices(string.digits, k=length))


def send_verification_sms(phone_number, verification_code):
    """
    Sends a verification SMS to the specified phone number.

    Parameters:
        phone_number (str): The phone number to send the SMS to.
        verification_code (str): The verification code to include in the SMS.

    Returns:
        None
    """
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
        operation_summary="User registration POST parameters",
        operation_description="User registration POST parameters",
    )
    def post(self, request):
        """
        Perform user registration.

        Parameters:
            request (Request): The HTTP request object.

        Returns:
            Response: The HTTP response object with the result of the registration.

        Raises:
            None.
        """
        form = UserRegistrationForm(request.data)

        if form.is_valid():
            user = form.save()

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

            return redirect('user-verification')

        response_data = {'message': 'User registration failed'}
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        query_serializer=UserSerializer(),
        operation_summary="User registration",
        operation_description="Description of what user GET"
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
        operation_summary="User SMS Verification",
        operation_description="Display the verification form to verify a user."
    )
    def get(self, request):
        # Get the phone number from the session
        phone_number = request.session.get('phone', '')

        # Render the verification form with the phone number
        form = UserSMSVerificationForm()
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
        """
        Perform user verification by providing the phone number and verification code.

        Args:
            request: The HTTP request object.

        Returns:
            A redirect to the home page if the verification is successful.
            A rendered HTML page with the verification form if the verification fails.

        Raises:
            None.
        """
        # Get the phone number from the session
        phone_number = request.session.get('phone', '')

        form = UserSMSVerificationForm(request.POST)

        if form.is_valid():
            verification_code = form.cleaned_data['verification_code']

            try:
                user_verification = UserVerification.objects.get(
                    phone=phone_number,
                    verification_code=verification_code,
                    attempts_remaining__gt=0,
                    verified=False,
                )

                # Mark the user as verified and save
                user_verification.user.verified = True
                user_verification.user.save()
                user_verification.verified = True
                user_verification.save_data_joint()
                user_verification.save()

                # Redirect to the home page upon successful verification
                return redirect('user-success')
            except UserVerification.DoesNotExist:
                form.add_error('verification_code', 'Invalid verification code')

        return render(request, 'users/verification.html', {'form': form})


class HomePage(APIView):
    permission_classes = [IsVerifiedUser]

    @swagger_auto_schema(
        responses={
            200: HomePageResponseSerializer(),
        },
        operation_summary="List Verified Users",
        operation_description="Get a list of all verified users."
    )
    def get(self, request):
        """
        Get a list of all verified users.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered success HTML page with the verified users.
        """
        # Fetch all verified users
        verified_users = User.objects.filter(verified=True).order_by('-id')
        return render(request, 'users/success.html', {'verified_users': verified_users})

    @swagger_auto_schema(
        request_body=CreateUserSerializer,
        responses={
            200: HomePageResponseSerializer(),
        },
        operation_summary="Create a New User",
        operation_description="Create a new user with the provided data."
    )
    def post(self, request):
        """
        Create a new user with the provided data.

        Parameters:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered registration HTML page.
        """
        return render(request, 'users/registration.html')
