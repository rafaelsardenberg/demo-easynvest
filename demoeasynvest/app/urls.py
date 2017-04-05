from django.conf.urls import url
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view
from app import views
from app.views import TituloViewSet,OperacaoViewSet

router = routers.DefaultRouter()
router.register(r'titulo', TituloViewSet, base_name="titulo")
router.register(r'operacao', OperacaoViewSet, base_name="operacao")
urlpatterns = router.urls
urlpatterns.append(url(r'^comparartitulos/', views.comparar))
urlpatterns.append(url(r'^importar/', views.importar))

schema_view = get_swagger_view(title='Demo - Easynvest')
urlpatterns.append(url(r'^swagger/', schema_view))