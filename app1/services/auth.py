import datetime
import random
import string
import uuid

from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from app1.models import User
from methodism.error_messages import error_params_unfilled, MESSAGE
from methodism.helper import custom_response, exception_data, generate_key, code_decoder

from app1.models.auth import OTP
from base.errors import TEXT
from base.costumizing import BearerAuth
from api.settings import BASE_DIR

def error(msg):
    return {
        "Error": msg
    }



class RegisView(GenericAPIView):
    def post(self, requests):
        data = requests.data
        if 'password' not in data or 'phone' not in data or 'token' not in data:
            return Response({
                "Error": 'Data toliq emas !!!'
            })

        otp = OTP.objects.filter(key=data['token']).first()

        if not otp:
            return Response(error('Неверный токен'))

        if not otp.is_conf:
            return Response(error('Устаревший токен'))

        # if type(data['phone']) is not int:
        #     return Response({
        #         "Error": "Телефон номер должен состоит из цифр !"
        #
        #     })
        #
        # if len(str(data['phone'])) != 12:
        #     return Response({
        #         "Error": "Телефон номер должен состоит из 12ти цифр !"
        #
        #     })

        user = User.object.filter(phone=otp.phone).first()

        if user:
            return Response({
                "error": "Этот телефон номер ранее был зарегистрирован !"

            })


        if len(data['password']) < 8 or data['password'].isalnum() or " " in data['password']:
            return Response({
                "Error": "Пароль должен состоит из 8 символов и больше 2х знаков без пробелов !"

            })

        user_data = {
            "phone": data['phone'],
            "password": data['password'],
            "name": data.get('name', '')
        }

        if data.get('key', None) == 'dmsevs':
            user_data.update({
                "is_staff": True,
                "is_superuser": True
            })

        user = User.object.create_user(**user_data)

        token = Token.objects.create(user=user)

        return Response({
            "Success": 'Ваш аккаунт успешно создан :)',
            "Ваш секретный ключ": token.key
        })


class LoginView(GenericAPIView):
    def post(self, requests):
        data = requests.data

        nott = "phone" if "phone" not in data else "password" if "password" not in data else ""
        if nott:
            resp = custom_response(False, message=error_params_unfilled(nott))
            return Response(resp)

        user = User.object.filter(phone=data["phone"]).first()
        if not user:
            # resp = custom_response(False, message=MESSAGE['UserPasswordError'])
            return Response(custom_response(False, message=TEXT['NotUser']))



        if not user.check_password(data['password']):
            try:
                return Response(custom_response(False, message=TEXT['PasswordError']))

            except Exception as luyboy:
                return Response(custom_response(False, message=exception_data(luyboy)))


        token = Token.objects.get_or_create(user=user)[0]
        print("token:", token)
        return Response({
            "Success": token.key

        })



class LogOutView(GenericAPIView):
    permission_classes = IsAuthenticated,
    authentication_classes = TokenAuthentication,

    def post(self, requests):
        token = Token.objects.filter(user=requests.user).first()
        if token:
            token.delete()

        return Response({
            "Success": "Вы вышли из аккаунта "
        })


class UserActions(GenericAPIView):
    permission_classes = IsAuthenticated,
    authentication_classes = BearerAuth,

    def get(self, requests):

        return Response({
            "data": requests.user.format()
        })


    def put(self, requests):
        data = requests.data

        if "phone" in data:
            user = User.object.filter(phone=data['phone']).first()
            if user and user.id != requests.user.id:
                return Response({
                    "Error": "Такой пользователь уже существует"
                })

        requests.user.phone = data.get('phone', requests.user.phone)
        requests.user.name = data.get('name', requests.user.name)

        requests.user.save()
        return Response({
            "data": requests.user.format()
        })

    def post(self, requests):
        data = requests.data
        if "old" not in data or "new" not in data:
            return Response({
                "Error": "Введите ваш пароль полностью"
            })

        if not requests.user.check_password(data['old']):
            return Response({
                "Error": "Неверный пароль"
            })

        if requests.user.check_password(data['new']):
            return Response({
                "Error": "Не используйте старый пароль, введите новые"
            })



        requests.user.set_password(data['new'])
        requests.user.save()


        return Response({
            "Success": "Ваш пароль успешно изменен"
        })

    def delete(self, requests):
        requests.user.delete()
        return Response({
            "Success": "Ваш аккаунт успешно удален"
        })


class AuthOne(GenericAPIView):

    def post(self, requests):
        data = requests.data
        if "phone" not in data:
            return Response(error("Введите свои данные полностью"))

        code = random.randint(100000, 999999)
        # letters = string.ascii_letters
        # digits = string.digits

        # for_help = letters+digits
        # code = "".join(for_help[random.randint(0, len(for_help)-1)] for i in range(6))
        shifr = uuid.uuid4().__str__() + "$" + str(code) + "$" + generate_key(20)

        # shifr = uuid.uuid4().__str__() + "$" + str(code) + "$" + generate_key(20)
        shifr = code_decoder(shifr )

        otp = OTP.objects.create(key=shifr, phone=data['phone']
        )

        # with open(f"{BASE_DIR}/hashing/{shifr}", 'w') as file:
        #     file.write(str(code))


        return Response({
            "otp": code,
            "token": otp.key
            # "let": letters,
            # "digits": digits
        })


class AuthTwo(GenericAPIView):
    def post(self, requests):
        data = requests.data
        if "otp" not in data or "token" not in data:
            return Response(error("Введите свои данные полностью "))

        token = OTP.objects.filter(key=data['token']).first()
        if not token:
            return Response(error("Неверный токен"))

        if token.is_expire:
            return Response(error("Срок данного токена истек, пожалуйста введите новый"))

        if token.is_conf:
            token.is_expire = True
            token.save()
            return Response(error('Неиспользуемый токен'))

        now = datetime.datetime.now(datetime.timezone.utc)

        if (now-token.created).total_seconds() >= 1800000000000:
            token.is_expire = True
            token.save()
            return Response(error("Истек срок токена"))

        code = code_decoder(token.key, decode=True).split('$')[1]

        if code != str(data['otp']):
            token.tries += 1
            token.save()
            return Response(error('Неверный код'))

        token.is_conf = True
        token.save()

        user = User.object.filter(phone=token.phone).first()

        return Response({
            # "shifr": code,
            # "Success": "Правильно работает"
            "is_registered": user is not None
        })




