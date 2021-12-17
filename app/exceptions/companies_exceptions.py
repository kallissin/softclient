class CNPJFormatError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "CNPJ must have 14 digits."
        }, 400


class InvalidIDError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "Company ID does not exist."
        }, 400
        
class CNPJExistsError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "The provided CNPJ already exists."
        }, 400        
        
class TradingNameExistsError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "The provided Trading Name already exists."
        }, 400                
        
class CompanyNameExistsError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "The provided Company Name already exists."
        }, 400      
        
class FailedToLoginError(Exception):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.message = {
            "error": "Username or password does not exist."
        }, 404                       