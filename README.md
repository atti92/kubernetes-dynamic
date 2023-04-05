# kubernetes-dynamic

This project aims to provide an easy interface over kubernetes API based on the official kubernetes package.

Basic syntax is very similar to kubectl.

`client.pods.get()` is the same as `kubectl get pods`

## Example Usage

```python
import kubernetes_dynamic as kd

client = kd.K8sClient()
pods: list[kd.models.V1Pod] = client.pods.get()
for pod in pods:
    print(pod.metadata.name)
```

### Custom resources

```python
import kubernetes_dynamic as kd

class MyModel(kd.models.ResourceItem):
    field: str


api: ResourceApi[MyModel] = kc.cl.get_api("mycustomresources", MyModel)
api: ResourceApi[MyModel] = kc.cl.get_api(kind="MyCustomResource", object_type=MyModel)
items: List[MyModel] = api.get()
item: Optional[MyModel] = api.get(name="exact-name")
if item:
    item.field = "modified"
    item.patch()
else:
    item = MyModel(metadata={"name": "exact-name", "namespace": "namespace-name"}, field="created", client=kd.cl)
    item.create()
    # item = MyModel(field="created")
    # item.metadata.name = "exact-name"

    # item = MyModel(metadata={"name": "exact-name"}, field="created")

    # item = MyModel(metadata=kd.models.V1Metadata(name="exact-name"), field="created")
    # item.create(namespace="namespace-name")
```

## Models

We aim to provide pydantic models for all reasources.

Because the model names are exactly the same as in the `kubernetes` package, make sure you import the models from `kubernetes_dynamic.models`

- Proper type hinting
- All models are flexible (less dependent on kubernetes version):
  - accept extra values
  - all optional (type checker is tricked into assuming everything exists)
- Models created by queries have a reference to the client it was created by, manually creating models creates a default client(without arguments), or you can specify `client` manually.
- Base model contains common methods for all models:
  - refresh
  - patch
  - create
  - read
  - delete
  - is_ready
- additional features for specific models (just examples):
  - configmap:
    - from_path
  - ingress:
    - get_default_host
  - namespace:
    - annotate
    - ensure
  - pod:
    - get_restarts
    - exec
    - disk_usage
    - get_controller_type
    - get_env
  - secret
    - exists
    - set
    - decode

## Subresources

Subresources are available under the main resource api objects:

- example: `client.pods.exec`

## Work in progress

Expect breaking changes
