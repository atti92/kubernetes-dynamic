from kubernetes_dynamic.models.ingress import V1Ingress


def test_ingress_init():
    pod = V1Ingress.parse_obj(dict(metadata={"name": "my_ingress"}))
    assert pod.metadata.name == "my_ingress"


def test_ingress_get_default_host(mock_client):
    mock_client.ingresses.get.return_value = [
        V1Ingress.parse_obj(dict(metadata={"name": "my_namespace"}, spec={"rules": [{"host": "hostname"}]}))
    ]
    assert V1Ingress.get_default_host() == "https://hostname"


def test_ingress_get_default_host_empty(mock_client):
    mock_client.ingresses.get.return_value = []
    assert V1Ingress.get_default_host() is None
