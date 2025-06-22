import re
from ..domain.repository.jquants.jquants_repository import JquantsRepository
from ..infra.jquants.jquants_repository_impl import JquantsRepositoryImpl


class GetJquantsTemporaryTokenService:
    jquantsRepository: JquantsRepository

    def __init__(self):
        self.jquantsRepository = JquantsRepositoryImpl()

    def get_token(self, email: str, password: str) -> str:
        return self.jquantsRepository.get_refresh_token(email, password)

    def get_id_token(self, refreshToken: str) -> str:
        return self.jquantsRepository.get_id_token(refreshToken)
