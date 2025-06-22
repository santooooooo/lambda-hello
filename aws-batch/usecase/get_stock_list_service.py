from typing import List
from ..domain.repository.jquants.jquants_repository import JquantsRepository
from ..infra.jquants.jquants_repository_impl import JquantsRepositoryImpl
from ..domain.model.stock import Stock

class GetStockListService:
    jquantsRepository: JquantsRepository

    def __init__(self):
        self.jquantsRepository = JquantsRepositoryImpl()

    def get(self, idToken: str) -> List[Stock]:
        return self.jquantsRepository.get_stock_list(idToken)
