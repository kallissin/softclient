class KeyTypeError(Exception):
    keys_list = ["type", "description", "user_id"]

    def __init__(self, data: dict):
        self.message = {
            "status": "error",
            "message": [f"{key} is required" for key in self.keys_list if key not in data.keys()]
        }
        self.code = 400

        super().__init__(self.message, self.code)
