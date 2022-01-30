from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Room, User

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password2']

class RoomForm(ModelForm):
    #普通、クラスに対して追加の情報や機能を差し挟むためには、初期化子の中で親クラスのメソッドを呼んだりメンバ変数や
    #プロパティを設定したりメソッドを定義する文(def文)を書いたりする。
    #がそうしなくも「そういうことをかわりにやってくれる機能」がメタクラスを指定したことで、class文の機能に追加されている
    #class Meta:以下にそのモデルのメタデータを指定できる。
    class Meta:

        #RoomのためのFormを作る
        model = Room

        #Formのフィールド（選択事項）をRoomのどれにするか
        #__all__は全てをフィールドにに含める（含めることができないものもある。今回はupdatedとcreated）
        fields = '__all__'

        #excludeで上のallから除外するのを指定する
        exclude = ['host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar','name', 'username', 'email', 'bio']