from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Topic(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

#python manage.py makemigrationsでマイグレーションファイルを作成する
#python manage.py migrateでモデルをデータベースに反映させる
#migrateをすることで、データベース構成を変更したり、その変更を取り消したりすることが出来るが、
#データベース構成のバージョン管理をするのに、makemigrationsでマイグレーションファイルを作成する。

#modles.Modelについて。Pythonではクラスの宣言において()中に継承するクラスを指定する。つまりmodles.Modelの子ということ
#一つのインスタンスに対してデフォルトでidが作成される。1からインスタンスごとに増える。
class Room(models.Model):

    #この親Userはimportした分
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    # もしclass Topicが class Roomよりも下に定義されていたら'Topic'の様に''で囲む
    #SET_NULLは親が消えても子が残る
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)

    #フォームとは 検索する単語を検索ウィンドウと呼ばれる文字入力フォームに入力をする。この文字入力フォームもフォームの一部。
    #他には様々なWebサービスでアカウントを作るときに、住所や年齢、電話番号などの個人情報を入力する。
    #これらを入力する場所もフォームであると言える。
    #nullもblankもデフォルトはFalse
    #blankはDjangoのフォームからの投稿が空かどうかを判定するもの、
    #nullはデータベースの中身が空かどうかを判定するもの。
    #それぞれ、blank=Trueとnull=Trueのときに、対象が空であることを許容することになる。
    description = models.TextField(null=True, blank=True)

    #ManyToManyFieldとは多対多の参照をする時に必要になる
    #親クラスにUserを指定しroomが子になる
    #
    participants = models.ManyToManyField(User, related_name='participants')
    #auto_now インスタンスがアップデート（セーブ）される度にスナップショット(DataTimeField)が自動で取られる
    updated = models.DateTimeField(auto_now=True)

    #aouto_now_addは一番最初にインスタンスが作られた時の情報のみ保存
    created = models.DateTimeField(auto_now_add=True)

    #メタデータとは主となるデータの説明書きが書いてあるデータのこと
    
    #モデルのメタデータをMetaという名前のクラスでモデルの中に作る。
    #モデルのメタデータとは、「フィールド定義じゃない何か」で、並べる時の順番指定(ordering)や、
    #DBのテーブル名や(db_table)、表示名の単数形と複数形(verbose_name と verbose_name_plural)などを指定する。
    #Metaは必須ではないので、必要になったら書く。
    class Meta:
        #ordering属性はオブジェクトのデフォルトの並び方を変更するときに使う。
        #‐で新しいのが先に来る。‐なしだと新しいのが一番後に来る
        #-updatedと-created二つ指定しているが別に一つでも良い。たとえば-idでも」表示は一緒
        ordering =['-updated', '-created']

    #__something__はコンストラクター（インスタンス作成時に自動で実行される）を意味する。
    def __str__(self):
        return self.name




class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    #Room親の名前を指定し、on_delete親が削除された時、models.CASCADEこのクラス（Message）も削除される
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[0:50]