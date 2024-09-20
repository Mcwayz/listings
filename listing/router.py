class ListingRouter:
    # Define the set of app labels that this router will apply to.
    # In this case, it only applies to the 'listing' app.
    route_app_labels = {'listing'}

    # Define the database to use when reading objects.
    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'listings'
        return None

    # Define the database to use when writing objects.
    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'listings'
        return None

    # Define if relationships between objects from different databases are allowed.
    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels:
            return True
        return None

    # Control which database migrations are applied to.
    def allow_migrate(self, db, app_label, **hints):
        if app_label in self.route_app_labels:
            return db == 'listings'
        return None
