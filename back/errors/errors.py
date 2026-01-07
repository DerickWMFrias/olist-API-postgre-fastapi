"""
Neste arquivo definimos todos os erros que a aplicação pode levantar
"""

class BusinessError(Exception):
    """Classe base para erros de regra de negócio"""
    pass

class UnauthorizedError(BusinessError):
    """Lançado quando se quer mandar uma exceção 401 com mensagens custom
    
    err_msg: Mensagem retornada como Response
    log_msg: Mensagem mostrada em logs internos
    """
    def __init__(self, err_msg: str, log_msg: str):
        self.err_msg = err_msg
        self.log_msg = log_msg
        super().__init__(self.err_msg)


class NotFoundError(BusinessError):
    """Lançado quando se quer mandar uma exceção 404 com mensagens custom
    
    err_msg: Mensagem retornada como Response
    log_msg: Mensagem mostrada em logs internos
    """
    def __init__(self, err_msg: str, log_msg: str):
        self.err_msg = err_msg
        self.log_msg = log_msg
        super().__init__(self.err_msg)


class NoEmailFoundError(BusinessError):
    """Lançada quando o e-mail não existe no sistema"""
    def __init__(self, email: str):
        self.message = f"Nenhum usuário encontrado com o e-mail: {email}"
        super().__init__(self.message)



class EmailAlreadyRegisteredError(BusinessError):
    """Lançada quando se tenta registrar um e-email ja esta cadastrado"""
    def __init__(self, email: str):
        self.message = f"Email {{email}} is already registered"
        super().__init__(self.message)