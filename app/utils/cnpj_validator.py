
LENGTH_CNPJ = 14

def is_cnpj_valid(cnpj: str) -> bool:
    if len(cnpj) != LENGTH_CNPJ:
        return False

    return True


def cnpj_formatter(cnpj: str):
    new_cnpj = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12], cnpj[12:14])
    return new_cnpj