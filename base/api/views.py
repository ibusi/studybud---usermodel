from rest_framework.decorators import api_view
from rest_framework.response import Response
from base.models import Room
from .serializers import RoomSerializer

#受け付けるrequestの種類を記述（今回はGETのみ受け付ける）
@api_view(['GET'])
def getRoutes(requst):

    #リストを定義するには、
    #角かっこ[]の中にそのリストに含めるデータをカンマで区切って並べていく。
    #リストには任意の種類のデータを好きな数だけ格納できる。なお、リストに格納する個々のデータのことを「要素」と呼ぶ。
    #要素には「0始まり」で番号（インデックス）が割り振られ、要素の値を使いたいときにはこれを使用する。
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id'
    ]

    return Response(routes)

    #The safe parameter decides on the type of python data type (tuples, dictionaries, strings 
    #etc.) you're wanting to pass. So concisely explained, it is the influencer of the data, 
    # JSON is to receive and pass across.
    #why is it mostly set to False?
    #The JSON Response in Django set save=True by default, and the safe parameter as a data influencer 
    #makes JSON accept the Python Data-Type {Dictionaries} and nothing less. So, at this point any data 
    #sent contrary to {Dictionaries} would actually fire up errors.
    #So, setting the safe parameter to False actually influences JSON to receive any Python Data Type.
    #its better to set it the safe parameter to False because it makes JSON accept both {Dictionaries} and others.
    #　return JsonResponse(routes, safe=False)


@api_view(['GET'])
def getRooms(request):
    rooms = Room.objects.all()

    #クエリセットとは、モデルのオブジェクトのリストのこと。

    #Serializerをインスタンス化する際の引数
    #serializer = Serializer(instance, data=data, partial=True)
    #や、
    #serializer = Serializer(queryset, many=True)
    #等々

    #複数のオブジェクトをシリアライズする場合はmany=Trueの記述が必要
    #今回はroomsの全てのオブジェクトが対象なのでmany=Trueになる
    serializer = RoomSerializer(rooms, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getRoom(request, pk):
    room = Room.objects.get(id=pk)
    serializer = RoomSerializer(room, many=False)
    return Response(serializer.data)