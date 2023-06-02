from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from app1.models import Ishchi
from .formats import ishchi_format
from .serializer import IshchiSerializer

from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class IshchiView(GenericAPIView):

    serializer_class = IshchiSerializer
    permission_classes = IsAuthenticated,
    authentication_classes = TokenAuthentication,

    def get(self, requests, pk=None):
        if pk:
            ishchi = Ishchi.objects.filter(id=pk).first()
            if not ishchi:
                return Response({

                    "Error": "Bunaqa idilik shaxs to'pilmadi("

                }, status=404 )

            ctx = {
                "result": ishchi_format(ishchi)
            }
            return Response(ctx)
        else:

            ishchilar = Ishchi.objects.all()
            bosh_list = []
            for i in ishchilar:
                bosh_list.append(ishchi_format(i))


            ctx = {
                'result': bosh_list
            }

            return Response(ctx)

    def post(self, requests):

        data = requests.data
        ser = self.get_serializer(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()

        return Response({
            'Natija': 'Это пост запрос !'

        })


    def put(self, requests, pk):
        data = requests.data
        ishchi = Ishchi.objects.filter(pk=pk).first()

        if not ishchi:
            return Response({

                "Error": "Bunaqa idilik ishchi yoq!!"
            })

        else:
            ser = self.get_serializer(data=data, instance=ishchi, partial=True)
            ser.is_valid(raise_exception=True)
            ser.save()
        #998117968

        return Response({
            'Natija': 'Это PUT запрос !'

        })

    def delete(self, requests, pk):
        ishchi = Ishchi.objects.filter(id=pk).first()

        if not ishchi:
            return Response({ "Error": 'Bunaqa idilik ishchi topilmadi(( ' }, status=404 )
        else:
            ishchi.delete()
            return Response({"Success": 'Операция успешно завершено ! '})



