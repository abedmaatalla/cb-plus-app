from django.conf.urls import url



websocket_urlpatterns = [
    # request status change
    url(r'^ws/request/(?P<request_id>[-\w\d]+)/$', consumers.RequestConsumer),
    # new request
    url(r'^ws/driver/requests/(?P<driver_id>[-\w\d]+)/$', consumers.DriverConsumer),
]

