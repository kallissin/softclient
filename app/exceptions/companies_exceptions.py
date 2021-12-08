class CNPJFormatError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "CNPJ must have 14 digits."
        }, 404


class InvalidIDError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "Company ID does not exist."
        }, 404
        
class InvalidTokenError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "The provided token is invalid or does not exist."
        }, 404        