from django.conf.urls import url

from main import consumers

websocket_urlpatterns = [
    # request status change
    url(r'^ws/stock/(?P<user_id>[-\w\d]+)/$', consumers.StockUser),
    # new request
]
