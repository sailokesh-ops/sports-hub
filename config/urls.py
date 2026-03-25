from core.views import home,live_scores,news,signup_view,login_view,logout_view
from core.views import add_favorite,favorites,reels,fixtures
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home),
    path('live/',live_scores),
    path('news/',news),
    path('signup/',signup_view),
    path('login/',login_view),
    path('logout/',logout_view),
    path('add-favorite/',add_favorite),
    path('favorites/',favorites),
    path('reels/',reels),
    path('fixtures/',fixtures)
]
