from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm


# rooms =[
#     {'id': 1, 'name': 'Lets learn python!'},
#     {'id': 2, 'name': 'Design with me'},
#     {'id': 3, 'name': 'Frontend developer'},
# ]


def loginPage(request):
    page = 'login'

    #Read-only attribute which is always True (as opposed to AnonymousUser.is_authenticated which is always False).
    #This is a way to tell if the user has been authenticated. This does not imply any permissions and 
    #doesn’t check if the user is active or has a valid session. Even though normally you will 
    #check this attribute on request.user to find out whether it has been populated by the 
    #AuthenticationMiddleware (representing the currently logged-in user), you should 
    #know this attribute is True for any User instance.
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        #from django.contrib.auth.models import UserからUserモデルをインポートすることでUserオブジェクトが使用できる

        #try-except文
        #文法的に正しいコードを書いても、実行時にエラーが発生することがある。これが「例外」というもので
        #英語ではExceptionという
        #try: 
            #例外が発生するかもしれないが、実行したい処理。
        #except （エラー名（TypeError等）を記述するとどの例外に対して処理を行うのかを指定できる）:
            #例外発生時に行う処理
        #まずは、tryの中に指定された処理が実行される。例外が発生しなければ、except文はスキップされる。
        #しかし、try実行中にexceptキーワードの後に指定したエラー名と一致する例外が発生すると、
        #except文が実行され、それ以降に記述された処理も実行される。
        #このように「except」ブロックで例外を捉えて処理をすることで、エラー発生箇所で処理が停止することはない。        
        try:
            #usernameはUserモデルが持っているフィールドの一つ
            #上で宣言したUsername（ログインページで入力するUsename）と
            #フィールドのUsernameが一致しているかgetの（）内で条件をつけて一致するならエラーはない
            user = User.objects.get(username=username)
        except:
            #from django.contrib import messagesからメッセージフレームワークをインポートしている
            messages.error(request, 'User doesnt exist')
        
        #authenticateはエラーを返すかマッチするユーザーのオブジェクトを返す
        user = authenticate(request, username=username, password=password)            

        if user is not None:

            #loginはsessionの作成と指定ユーザーをログインさせる
            #今回のでいうとredirectでユーザーをhomeにログインさせている
            login(request, user)

            #ridirectはtemplates(html)に何も渡さない。単に対象のURLに遷移したいときに使用する。
            #renderはredirectと違いtemplates(html)に変数等を渡せる。
            #renderで記述した内容をHttpResponseに渡すことでレンダリングする。
            return redirect('home')
        else:
            messages.error(request, 'Username or password doesnt exist')
                        
    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    #ログアウトさせる（loginで作成されたsession idを削除する） 
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #save() メソッドはオプション commit キーワード引数を持っている。この引数には True または False を指定する。
            #save() をcommit=False で呼び出すと、データベースに保存する前のモデルオブジェクトを返す。
            #返されたオブジェクトに対して最終的に save() を呼び出すかどうかは自由。この機能は、オブジェクトを実際に
            #保存する前に何らかの処理を行いたい場合に便利。commit はデフォルトでは True に設定されている。
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')

    return render(request, 'base/login_register.html', {'form' : form})

#render() 関数は、第1引数として requestを、（セッションの情報や、requestの種類（getかpost）の情報が入っている）
#（ウェブサイトの中のリンクをクリックして他のサイトに移動する時等、基本的使われるmethodは「GET」）
#（POSTは個人情報やパスワードなども安心してサーバーに送信することができる送信（request）方法。）
#requestは簡単に言えば、HttpRequestオブジェクトのこと。
#HttpRequestオブジェクトはdjango内で、システムを通じてステータスを渡すものになる
#訪問者があるページのURLをふんだ際に、該当ページを出力するようにリクエストが発生する。
#そのリクエストが発生された時に、djangoはリクエストに関するデータを含んだHttpRequestオブジェクトを作る。
#するとdjangoは作成したHttpRequestオブジェクトをdjango内のシステム(views.pyなど)に最初のオブジェクトとして渡す。
#渡した後、システム内でHttpRequestオブジェクトの読み込みを行い、返り値としてHttpResponseオブジェクトを返す。
#この説明であったHttpRequestオブジェクトが「request」の正体。
#第2引数としてテンプレート名を、
#第3引数（任意）として辞書を受け取る。この関数はテンプレートを指定のコンテキストでレンダリングし、
#その HttpResponse オブジェクトを返す。
#テンプレートに変数（主にディクショナリー）を渡すには第三引数にテンプレート内で利用したい変数を入れた辞書を渡す。
#｛'テンプレート内での変数名を作成'：テンプレートに渡したいディクショナリーの変数名やテキストを記述｝
#今回の例で行くと｛roomsというディクショナリーの変数名を作成：それは上記で作成済みのroomsディクショナリー｝
def home(request):

    #request.GETはdjangoで使われるメソッドでrequestは辞書型のデータではないので
    #requst.get(pythonで使われる辞書型のデータを取得するメソッド)でデータの取得はできないが
    #request.GETをつける事でrequestのデータを辞書型として扱い取得することができる
    #inline ifステイトメントは一行で記述するif文
    #条件式が真のときに評価される式か値 if 条件式 else 条件式が偽のときに評価される式か値
    #今回のを分かりやすくするともし if request.GET.get('q') != None だったら q = request.GET.get('q')
    #違うかったら else ''
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #filterでは結果はオブジェクトのリストとして返される。 しかし、場合によってはひとつのオブジェクトだけが返ることを
    #期待する場合もある。 そのときはgetを利用する。
    #topicは子のオブジェクトなのでtopic__nameとすることで親のclassのTopicの名前を指定することになる
    #かつ↑で取得したqと一致したのを取得
    #部分一致（大文字小文字区別無し）させたい場合はicontainsを使う。
    #部分一致（大文字小文字区別有り）させたい場合はcontainsを使う。
    #Qで|(or)が使用できるようになる
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
        )

    topics = Topic.objects.all()

    #countでアイテムの数を取得
    room_count = rooms.count()

    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count}
    return render(request, 'base/home.html', context)


#pkはプライマリーキー(psrimary key)の略
def room(request, pk):
#    room = None
#    for i in rooms:
#        if i['id'] == int(pk):
#            room = i
#class.objects.getで指定したオブジェクトを取得する。（多対１）
#一つのインスタンスに対してデフォルトでidが作成される。1からインスタンスごとに増える。
#getは他と被らないvalueを使ってシングルアイテムをゲットできる。IDは一つしかないので被る事はない。
#かつid=pkでidとpkが一致しているか条件を指定している。（IDはデフォルトのプライマリーキーなので絶対一致する）
    room = Room.objects.get(id=pk)

    #インスタンス名.モデル名_set.all()で1対多の参照が可能（親から子）
    #今回のいえばメッセージ作成時はルームの指定も必須（ルームはメッセージの親だから）
    #そこでいくらか作成されているメッセージを全て参照している

    #ユーザーは、djangoに備えられたメソッドを使うことによって、モデルからデータを取り出すことができ、
    #その一連のデータがquerysetと呼ばれる。
    #order_by('hoge')とするとhogeの昇順でならんでいく
    room_messages = room.message_set.all().order_by('-created')

    if request.method == 'POST':
        #createは必要な条件を入力したらインスタンスを作成できる
        message = Message.objects.create(
            user=request.user,
            room=room,
            #この'bodyはroom.htmlで作成した'body'
            body=request.POST.get('body')
        )
        #redirect先が'room'だけだとroomのどのパラメーターのurlの所に移動するのかわからずエラーになる
        #ので第二引数でパラメーターの指定をする
        #pk=room.idとしているが必ずもpk=としなければならないわけではない。room.idだけでもOK
        #redirectの第二引数は可変長引数（引数の数が決まっていない引数のこと。型が同じであれば任意の数設定することができる）
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages': room_messages}
    return render(request, 'base/room.html', context)

#login_requiredはsession idがあるかどうかを確認しなかったら指定のURLに移動させる
@login_required(login_url='login')
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

@login_required(login_url='login')
def updateRoom(request, pk):

    #get()メソッドは辞書型のオブジェクトから値を取得するために使用する。
    #辞書型とは、キーと値（バリュー）を組み合わせたデータ型。
    #辞書型オブジェクト.get(key, default=None)
    #get()メソッドでは第一引数にキーを指定し、第二引数にそのキーが存在しなかった場合に返す値を指定する。
    #第二引数は指定しなければ、デフォルトのNoneが返されるようになる。
    #以上からmodelで作成され保存されるデータは辞書型として扱われる事がわかる。多分
    room = Room.objects.get(id=pk)

    #インスタンスに情報を入れることでフォームにあらかじめ記述された状態ができる
    form = RoomForm(instance=room)

    #ルーム作成者とアップデートしようとしているユーザーが同じか確認
    if request.user != room.host:
        #HttpResponseは
        #文字列の情報を渡す、ファイルを表示、ダウンロードなど様々なことができる。
        #テンプレート(HTML)の表示もできるが、手間がかかるため、不向き。
        #下記のrenderはこれのショートカット関数。
        #renderは
        #関数ベースビューで一番多用される。
        #テンプレート単体や文字列を反映したテンプレートを簡単に表示できる。
        #ファイルの表示などには不向き。
        #redirectは
        #webページに来たユーザを別のURLに転送する。
        #サイトの表示用ではない。
        return HttpResponse('You are not allowed here‼')

    #サブミットボタンが押された後の動作をifで書いている
    #サブミットが押されたことでリクエストが発生、それがPOSTか確認
    if request.method == 'POST':

        #POST方式であればrequest.POSTとすることでrequestからデータを辞書型で取得できる。
        #（request.POST["id"]等にして指定したものを取得することもできる。（今回は指定せずに全データ））
        #instance=roomとすることでIDが同じページに情報が上書きされる
        #ModelForm から生成されたフォームは save() メソッドを備えている。
        #このメソッドは、フォームに結びつけられたデータから、モデルオブジェクトを生成してデータベースに保存する。
        #ModelForm のサブクラスは既存のモデルイ ンスタンスをキーワード引数 instance にしてインスタンス化できる。
        #instance を指定してモデルフォームを生成すると、モデルフォームの save() はこのインスタンスを更新して保存する。
        #instance を指定しな ければ、 save() はモデルフォームで指定しているモデルの新たなインスタン スを生成します
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here‼')

    if request.method =='POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})