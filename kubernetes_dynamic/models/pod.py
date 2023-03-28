from __future__ import annotations

from typing import TYPE_CHECKING

from ..resource import ResourceItem

if TYPE_CHECKING:
    from . import V1ObjectMeta, V1PodSpec, V1PodStatus


class V1Pod(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1PodSpec
    status: V1PodStatus

    @classmethod
    def get_restarts(cls):
        """Get pod restarts."""
        pod_restarts: dict[str, dict] = {}
        for pod in cls.default_client().pods.get():
            pod_restarts[pod.metadata.name] = {}
            for container in pod.status.containerStatuses:
                if container.restartCount > 0:
                    pod_restarts[pod.metadata.name][container.name] = {
                        "restart_count": container.restartCount,
                        "last_restart_reason": container.lastState.terminated.reason,
                        "last_restart_finished_at": container.lastState.terminated.finishedAt,
                    }
                else:
                    pod_restarts[pod.metadata.name][container.name] = {
                        "restart_count": container.restartCount,
                        "last_restart_reason": "N/A",
                        "last_restart_finished_at": "N/A",
                    }
        return pod_restarts

    def exec(
        self,
        command: str | list[str],
        container: str = "",
        stdin: bool = True,
        stdout: bool = True,
        stderr: bool = True,
        tty: bool = True,
    ) -> str:
        """Run command on pod."""
        response = self.client.stream(
            self.client.pods.exec.get,  # type: ignore
            self.metadata.name,
            self.metadata.namespace,
            container=container,
            command=command,
            stdin=stdin,
            stdout=stdout,
            stderr=stderr,
            tty=tty,
        )
        return response

    def disk_usage(self, container: str = "") -> dict[str, dict[str, int]]:
        """Get disc usage on a pod's container."""
        data = {}
        output = self.exec(["df", "--output=used,size,avail,pcent,target"], container)
        for line in output.splitlines()[1:]:
            used, size, avail, pcent, target = line.split()
            data[target] = {
                "used": int(used),
                "size": int(size),
                "avail": int(avail),
                "pcent": int(pcent.strip("%")),
            }
        return data

    def get_controller_type(self) -> str:
        """Get pod controller type."""
        controller = self.metadata.ownerReferences[0].kind
        controller = "Deployment" if controller == "ReplicaSet" else controller
        return controller

    def get_env(self) -> dict[str, str]:
        """Get environment variables from a pod."""
        env = self.exec("env")
        return {item.split("=", 1)[0]: item.split("=", 1)[1] for item in env.splitlines()}
