from .base_provider import BaseProvider

@BaseProvider.register_provider('traefik')
class TraefikProvider(BaseProvider):

    def get_domains(self, container):
        # Extract domains from Traefik labels
        labels = container.attrs['Config']['Labels']
        domains = []
        for key, value in labels.items():
            if key.startswith("traefik.http.routers.") and key.endswith(".rule"):
                # Extract domain from rule like "Host(`example.com`)"
                domain = value.split("`")[1]
                domains.append(domain)
        return domains
