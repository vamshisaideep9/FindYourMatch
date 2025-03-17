class ChatDBRouter:

    """
    Direct all chat-related models to the 'chats_db' database
    
    """

    route_app_labels = {"randomchats"}

    def db_for_read(self, model, **hints):
        """
        Reads from the chat database
        """
        if model._meta.app_label in self.route_app_labels:
            return "chats_db"
        return None
    
    def db_for_write(self, model, **hints):
        """Writes to the chat database."""
        if model._meta.app_label in self.route_app_labels:
            return "chats_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
    
        if (
            obj1._meta.app_label in self.route_app_labels
            or obj2._meta.app_label in self.route_app_labels
        ):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure only chat models migrate in chat_db."""
        if app_label in self.route_app_labels:
            return db == "chats_db"
        return None
    
