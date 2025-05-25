class Owner_Not_Found_Error(Exception):
    """Custom exception raised when an owner cannot be found."""
    
    def __init__(self, owner_id=None, message="Owner not found"):
        self.owner_id = owner_id
        self.message = message
        if owner_id:
            self.message = f"Owner with ID '{owner_id}' not found."
        super().__init__(self.message)

    def __str__(self):
        return self.message