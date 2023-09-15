from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .forms import UserRegistrationForm, UserSMSVerificationForm, UserProfileForm, UserVerificationForm
from .permissions import IsVerifiedUser
from .serializers import *
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render, redirect
from twilio.rest import Client
from django.conf import settings
import random
import string


@api_view(['GET'])
@permission_classes([IsVerifiedUser])
def get_user_profile(request):
    user = request.user

    # Get users who entered the current user's invite code
    users_with_invite = User.objects.filter(invite_code=user.invite_code).exclude(id=user.id)

    # Serialize the user's profile data
    profile_serializer = UserProfileSerializer(user)

    # Serialize the users who entered the invite code
    users_with_invite_serializer = UserProfileSerializer(users_with_invite, many=True)

    data = {
        'profile': profile_serializer.data,
        'users_with_invite': users_with_invite_serializer.data
    }

    return Response(data)


@api_view(['GET'])
@permission_classes([IsVerifiedUser])
def get_users_with_invite_code(request):
    user = request.user

    # Get users who entered the current user's invite code
    users_with_invite = User.objects.filter(invite_code=user.invite_code).exclude(id=user.id)

    # Serialize the users who entered the invite code
    users_with_invite_serializer = UserSerializer(users_with_invite, many=True)

    return Response(users_with_invite_serializer.data)


@api_view(['POST'])
@permission_classes([IsVerifiedUser])
def enter_invite_code(request):
    user = request.user
    invite_code = request.data.get('invite_code')

    if not invite_code:
        return Response({'message': 'Invite code is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        target_user = User.objects.get(invite_code=invite_code)
    except User.DoesNotExist:
        return Response({'message': 'Invalid invite code'}, status=status.HTTP_400_BAD_REQUEST)

    if target_user == user:
        return Response({'message': 'You cannot enter your own invite code'}, status=status.HTTP_400_BAD_REQUEST)

    if target_user.verified:
        return Response({'message': 'User with this invite code is already verified'},
                        status=status.HTTP_400_BAD_REQUEST)

    # Assign the target user's invite code to the current user
    user.invite_code = invite_code
    user.save()

    return Response({'message': 'Invite code entered successfully'})


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
        name = request.data['name']
        password = request.data['password']
        existing_user = User.objects.filter(name=name, password=password).exists()

        if existing_user:
            return redirect('user-success')

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
        print(form, request.user)
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
        print(phone_number)
        print(request.user)
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
        print(request.user)
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


class UserProfile(APIView):
    permission_classes = [IsVerifiedUser]

    def get(self, request):
        user = request.user
        print(user)
        user_data = {
            'name': user.name,
            'phone': user.phone,
            'invite_code': user.invite_code,
            'verified': user.verified,
        }
        form = UserProfileForm(instance=user, initial=user_data)
        return render(request, 'users/profile.html', {'form': form})

    def put(self, request):
        user = request.user
        form = UserProfileForm(request.data, instance=user)

        if form.is_valid():
            form.save()
            return Response({'message': 'User profile updated successfully'})
        else:
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
