class InvalidBirthDateError(Exception):
    ...

class KeyTypeError(Exception):
    list_keys = ["name", "email", "password", "active", "role", "company_id"]

    def __init__(self, data: dict):
        self.message = {
            "status": "error",
            "message": [f"{key} is required" for key in self.list_keys if key not in data.keys()]
        }
        self.code = 400

        super().__init__(self.message, self.code)

class InvalidRoleError(Exception):
    ...