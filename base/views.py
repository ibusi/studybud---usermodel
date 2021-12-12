from django.shortcuts import render, redirect
from .models import Room
from .forms import RoomForm


# rooms =[
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developer'},
# ]

#render() 関数は、第1引数として request オブジェクトを、第2引数としてテンプレート名を、
#第3引数（任意）として辞書を受け取る。この関数はテンプレートを指定のコンテキストでレンダリングし、
#その HttpResponse オブジェクトを返す。
#テンプレートに変数（主にディクショナリー）を渡すには第三引数にテンプレート内で利用したい変数を入れた辞書を渡す。
#｛'テンプレート内での変数名を作成'：テンプレートに渡したいディクショナリーの変数名やテキストを記述｝
#今回の例で行くと｛roomsというディクショナリーの変数名を作成：それは上記で作成済みのroomsディクショナリー｝
def home(request):
    #objectはmodelマネージャー
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render(request, 'base/home.html', context)


#pkはプライマリーキー(primary key)の略
def room(request, pk):
#    room = None
#    for i in rooms:
#        if i['id'] == int(pk):
#            room = i
#一つのインスタンスに対してデフォルトでidが作成される。1からインスタンスごとに増える。
#getは他と被らないvalueを使ってシングルアイテムをゲットできる。IDは一つしかないので被る事はない。
#それを（id=pk）でpkに渡している
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render(request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    
    #room_form.htmlで指定したformのmethod
    if request.method == 'POST':
        #request.postで全てのPOSTのデータをformに送る
        form = RoomForm(request.POST)
        #is_validは、フォームに入力された値にエラーがないかをバリデートするメソッド。
        #例えば、IntegerFieldの項目に数値以外のものが入った場合や、必須の項目が空欄だった場合にエラーとなる。
        if form.is_valid():
            #saveはデータベースにセーブする
            form.save()
            #redirectでしてしたページにユーザーを送る。今回はホーム（urls.pyで名前指定してる）
            return redirect('home')

    context ={'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)

    #インスタンスに情報を入れることでフォームにあらかじめ記述された状態ができる
    form = RoomForm(instance=room)

    context = {'form': form}
    return render(request, 'base/room_form.html', context)