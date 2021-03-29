from django.urls import include, path
from rest_framework import routers
from api.restshop import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'cart', views.CartViewSet)
router.register(r'cartcontent', views.CartContentViewSet)
router.register(r'menu', views.MenuViewSet)
router.register(r'company', views.CompanyViewSet)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]