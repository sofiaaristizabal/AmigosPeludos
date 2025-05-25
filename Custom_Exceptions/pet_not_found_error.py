class Pet_Not_Found_Error(Exception):
    """Custom exception raised when a pet cannot be found."""
    
    def __init__(self, pet_id=None, message="Pet not found"):
        self.pet_id = pet_id
        self.message = message
        if pet_id:
            self.message = f"Owner with ID '{pet_id}' not found."
        super().__init__(self.message)

    def __str__(self):
        return self.message