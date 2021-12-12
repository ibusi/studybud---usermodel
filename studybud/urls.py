#ここでURLを作成する


from django.contrib import admin
from django.urls import path, include
#When to use include()
#You should always use include() when you include other URL patterns. 
#admin.site.urls is the only exception to this.



urlpatterns = [
    #python manage.py createsuperuserでアドミンにアクセスできるユーザーを作成
    path('admin/', admin.site.urls),
    #''の部分はそのページのホームの部分。urlの追加は無し。
    path('', include('base.urls')),
    
]
