from django.urls import path
from blockchain import views as blockchain_views


urlpatterns = [
    path('get-chain/', blockchain_views.GetChain.as_view(), name='get_chain'),
    path('mine-block/', blockchain_views.MineBlock.as_view(), name='mine_block'),
    path('check-chain/', blockchain_views.CheckBlockchain.as_view(), name='check_chain'),
]
