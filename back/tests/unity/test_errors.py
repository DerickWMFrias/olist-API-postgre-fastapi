import pytest
import uuid
from errors.errors import NotFoundError

@pytest.mark.unity
def test_POST_users_1_successful_register(client):
    e_msg = "Usuário não existe"
    l_msg = "ID 123 não encontrado no banco de produção"

    with pytest.raises(NotFoundError) as exc_info:
        raise NotFoundError(err_msg=e_msg, log_msg=l_msg)
    
    assert exc_info.value.err_msg == e_msg
    assert exc_info.value.log_msg == l_msg

    assert str(exc_info.value) == e_msg