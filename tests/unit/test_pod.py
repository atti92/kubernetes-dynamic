from datetime import datetime

from kubernetes_dynamic.models.pod import V1Pod


def test_pod_init():
    pod = V1Pod.parse_obj(dict(metadata={"name": "my_pod"}))
    assert pod.metadata.name == "my_pod"


def test_pod_get_restarts(mock_client):
    finished_at = datetime.utcnow()
    pod_1 = V1Pod.parse_obj(
        dict(
            metadata={"name": "pod-1"},
            status={
                "containerStatuses": [
                    {
                        "name": "container-1",
                        "restartCount": 1,
                        "lastState": {"terminated": {"reason": "reason", "finishedAt": finished_at}},
                    }
                ]
            },
        )
    )
    pod_2 = V1Pod.parse_obj(
        dict(
            metadata={"name": "pod-2"},
            status={
                "containerStatuses": [
                    {
                        "name": "container-2",
                        "restartCount": 0,
                        "lastState": {"terminated": {"reason": "", "finishedAt": None}},
                    }
                ]
            },
        )
    )

    mock_client.pods.get.return_value = [pod_1, pod_2]
    assert V1Pod.get_restarts() == {
        "pod-1": {
            "container-1": {
                "last_restart_finished_at": finished_at,
                "last_restart_reason": "reason",
                "restart_count": 1,
            }
        },
        "pod-2": {
            "container-2": {
                "last_restart_finished_at": "N/A",
                "last_restart_reason": "N/A",
                "restart_count": 0,
            }
        },
    }


def test_pod_exec(mock_client):
    pod = V1Pod.parse_obj(dict(metadata={"name": "my_pod", "namespace": "my_namespace"}))
    assert pod.exec("command", "container") == mock_client.stream.return_value
    mock_client.stream.assert_called_with(
        pod._api.exec.get,
        "my_pod",
        "my_namespace",
        container="container",
        command="command",
        stdin=True,
        stdout=True,
        stderr=True,
        tty=True,
    )


def test_pod_disk_usage(mock_client):
    pod = V1Pod.parse_obj(dict(metadata={"name": "my_pod"}))
    mock_client.stream.return_value = """    Used 1K-blocks    Avail Use% Mounted on
12370080 104845292 92475212  12% /
        0     65536    65536   0% /dev
        0  16440724 16440724   0% /sys/fs/cgroup
12370080 104845292 92475212  12% /tmp
        0     65536    65536   0% /dev/shm
        8  32022312 32022304   1% /opt/kx/lic
        12  32022312 32022300   1% /run/secrets/kubernetes.io/serviceaccount
        0  16440724 16440724   0% /proc/acpi
        0  16440724 16440724   0% /proc/scsi
        0  16440724 16440724   0% /sys/firmware"""
    assert pod.disk_usage("container") == {
        "/": {"used": 12370080, "size": 104845292, "avail": 92475212, "pcent": 12},
        "/dev": {"used": 0, "size": 65536, "avail": 65536, "pcent": 0},
        "/sys/fs/cgroup": {"used": 0, "size": 16440724, "avail": 16440724, "pcent": 0},
        "/tmp": {"used": 12370080, "size": 104845292, "avail": 92475212, "pcent": 12},
        "/dev/shm": {"used": 0, "size": 65536, "avail": 65536, "pcent": 0},
        "/opt/kx/lic": {"used": 8, "size": 32022312, "avail": 32022304, "pcent": 1},
        "/run/secrets/kubernetes.io/serviceaccount": {
            "used": 12,
            "size": 32022312,
            "avail": 32022300,
            "pcent": 1,
        },
        "/proc/acpi": {"used": 0, "size": 16440724, "avail": 16440724, "pcent": 0},
        "/proc/scsi": {"used": 0, "size": 16440724, "avail": 16440724, "pcent": 0},
        "/sys/firmware": {"used": 0, "size": 16440724, "avail": 16440724, "pcent": 0},
    }


def test_pod_get_controller_type_replicaset():
    pod = V1Pod.parse_obj(dict(metadata={"name": "my_pod", "ownerReferences": [{"name": "", "kind": "ReplicaSet"}]}))
    assert pod.get_controller_type() == "Deployment"


def test_pod_get_controller_type_other():
    pod = V1Pod.parse_obj(dict(metadata={"name": "my_pod", "ownerReferences": [{"name": "", "kind": "Other"}]}))
    assert pod.get_controller_type() == "Other"


def test_pod_get_env(mock_client):
    pod = V1Pod.parse_obj(dict(metadata={"name": "my_pod"}))
    mock_client.stream.return_value = """RT_KODBC_ASSEMBLY_NORTH_0_SERVICE_HOST=10.218.54.243
INSIGHTS_GUI_GATEWAY_PORT_10001_TCP_PROTO=tcp
RT_KODBC_ASSEMBLY_SOUTH_2_PORT_7000_UDP_PORT=7000
RT_KODBC_ASSEMBLY_NORTH_1_PORT_6000_TCP=tcp://10.218.53.117:6000
RT_KODBC_ASSEMBLY_NORTH_2_PORT_8000_UDP_ADDR=10.218.52.165
INSIGHTS_KEYCLOAK_SERVICE_HOST=10.218.52.249
_=/usr/bin/env"""
    assert pod.get_env() == {
        "RT_KODBC_ASSEMBLY_NORTH_0_SERVICE_HOST": "10.218.54.243",
        "INSIGHTS_GUI_GATEWAY_PORT_10001_TCP_PROTO": "tcp",
        "RT_KODBC_ASSEMBLY_SOUTH_2_PORT_7000_UDP_PORT": "7000",
        "RT_KODBC_ASSEMBLY_NORTH_1_PORT_6000_TCP": "tcp://10.218.53.117:6000",
        "RT_KODBC_ASSEMBLY_NORTH_2_PORT_8000_UDP_ADDR": "10.218.52.165",
        "INSIGHTS_KEYCLOAK_SERVICE_HOST": "10.218.52.249",
        "_": "/usr/bin/env",
    }
