from rest_framework.serializers import ModelSerializer
from base.models import Room

# serializerとは
# 一言で表すと、データの入出力を扱い、モデルでの橋渡しをするクラスのこと。
# シリアライズ（入力）：複雑な入力値をモデルに合わせてバリデーションしてレコードに伝える
# デシリアライズ（出力）：Model（レコード）を適切な形式にフォーマットしてpythonで扱えるようにする

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'