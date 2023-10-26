from .base_provider import BaseProvider

@BaseProvider.register_provider('jwilder-nginx-proxy')
class JWilderNginxProxyProvider(BaseProvider):

    def get_domains(self, container):
        # Extract domains from JWilder's environment variables
        env_vars = container.attrs['Config']['Env']
        for env in env_vars:
            if env.startswith("VIRTUAL_HOST="):
                return env.split("=")[1].split(",")
        return []
