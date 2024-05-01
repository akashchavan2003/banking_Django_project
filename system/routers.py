class OtherDatabaseRouter:
    def db_for_read(self, model, **hints):
        # Route models from the 'system' app to the 'other_database'
        if model._meta.app_label == 'system':
            return 'other_database'
        return None

    def db_for_write(self, model, **hints):
        # Route models from the 'system' app to the 'other_database'
        if model._meta.app_label == 'system':
            return 'other_database'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if either object is from the 'system' app
        if obj1._meta.app_label == 'system' or obj2._meta.app_label == 'system':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Allow migrations for the 'system' app only if it's the 'other_database'
        if app_label == 'system':
            return db == 'other_database'
        return None

