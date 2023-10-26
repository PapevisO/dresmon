class BaseProvider:

    PROVIDER_MAPPING = {}

    @classmethod
    def register_provider(cls, provider_name):
        def decorator(subclass):
            cls.PROVIDER_MAPPING[provider_name] = subclass
            return subclass
        return decorator

    def get_domains(self, container):
        raise NotImplementedError("Each provider must implement the 'get_domains' method.")
