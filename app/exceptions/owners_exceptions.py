class KeyRequiredError(Exception):
    list_keys = ['name', 'username', 'password']

    def __init__(self, data: dict):
        self.message = {
            "status": "error",
            "message": [f"{key} is required" for key in self.list_keys if key not in data.keys()]
        }
        self.code = 400

        super().__init__(self.message, self.code)
