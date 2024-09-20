class AuthRouter:
    # Define the set of app labels that this router will apply to.
    # This includes the built-in Django apps like 'auth', 'admin', 'contenttypes', 'sessions', and any other specified apps.
    route_app_labels = {'user', 'admin', 'contenttypes', 'sessions', 'auth'}

    # Define the database to use when reading objects.
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'users'
        return None

    # Define the database to use when writing objects.
    def db_for_write(self, model, **hints):
        # If the model belongs to one of the apps in route_app_labels, use the 'users' database.
        if model._meta.app_label in self.route_app_labels:
            return 'users'
        return None

    # Define if relationships between objects from different databases are allowed.
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels:
            return True
        return None

    # Control which database migrations are applied to.
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'users'
        return None
