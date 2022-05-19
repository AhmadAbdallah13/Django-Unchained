from django.urls import path
from cryptocurrency import views as cryptocurrency_views

urlpatterns = [
    path('add-transaction/', cryptocurrency_views.AddTransaction.as_view(), name='add_transaction'),
    path('connect-node/', cryptocurrency_views.ConnectNode.as_view(), name='connect_node'),
    path('replace-chain/', cryptocurrency_views.ReplaceChain.as_view(), name='replace_chain'),
]
