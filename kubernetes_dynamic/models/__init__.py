__all__ = [
    "AdmissionregistrationV1ServiceReference",
    "AdmissionregistrationV1WebhookClientConfig",
    "ApiextensionsV1ServiceReference",
    "ApiextensionsV1WebhookClientConfig",
    "ApiregistrationV1ServiceReference",
    "AuthenticationV1TokenRequest",
    "CoreV1EndpointPort",
    "CoreV1Event",
    "CoreV1EventList",
    "CoreV1EventSeries",
    "DiscoveryV1EndpointPort",
    "EventsV1Event",
    "EventsV1EventList",
    "EventsV1EventSeries",
    "StorageV1TokenRequest",
    "V1APIGroup",
    "V1APIGroupList",
    "V1APIResource",
    "V1APIResourceList",
    "V1APIService",
    "V1APIServiceCondition",
    "V1APIServiceList",
    "V1APIServiceSpec",
    "V1APIServiceStatus",
    "V1APIVersions",
    "V1AWSElasticBlockStoreVolumeSource",
    "V1Affinity",
    "V1AggregationRule",
    "V1AttachedVolume",
    "V1AzureDiskVolumeSource",
    "V1AzureFilePersistentVolumeSource",
    "V1AzureFileVolumeSource",
    "V1Binding",
    "V1BoundObjectReference",
    "V1CSIDriver",
    "V1CSIDriverList",
    "V1CSIDriverSpec",
    "V1CSINode",
    "V1CSINodeDriver",
    "V1CSINodeList",
    "V1CSINodeSpec",
    "V1CSIPersistentVolumeSource",
    "V1CSIStorageCapacity",
    "V1CSIStorageCapacityList",
    "V1CSIVolumeSource",
    "V1Capabilities",
    "V1CephFSPersistentVolumeSource",
    "V1CephFSVolumeSource",
    "V1CertificateSigningRequest",
    "V1CertificateSigningRequestCondition",
    "V1CertificateSigningRequestList",
    "V1CertificateSigningRequestSpec",
    "V1CertificateSigningRequestStatus",
    "V1CinderPersistentVolumeSource",
    "V1CinderVolumeSource",
    "V1ClaimSource",
    "V1ClientIPConfig",
    "V1ClusterRole",
    "V1ClusterRoleBinding",
    "V1ClusterRoleBindingList",
    "V1ClusterRoleList",
    "V1ComponentCondition",
    "V1ComponentStatus",
    "V1ComponentStatusList",
    "V1Condition",
    "V1ConfigMap",
    "V1ConfigMapEnvSource",
    "V1ConfigMapKeySelector",
    "V1ConfigMapList",
    "V1ConfigMapNodeConfigSource",
    "V1ConfigMapProjection",
    "V1ConfigMapVolumeSource",
    "V1Container",
    "V1ContainerImage",
    "V1ContainerPort",
    "V1ContainerState",
    "V1ContainerStateRunning",
    "V1ContainerStateTerminated",
    "V1ContainerStateWaiting",
    "V1ContainerStatus",
    "V1ControllerRevision",
    "V1ControllerRevisionList",
    "V1CronJob",
    "V1CronJobList",
    "V1CronJobSpec",
    "V1CronJobStatus",
    "V1CrossVersionObjectReference",
    "V1CustomResourceColumnDefinition",
    "V1CustomResourceConversion",
    "V1CustomResourceDefinition",
    "V1CustomResourceDefinitionCondition",
    "V1CustomResourceDefinitionList",
    "V1CustomResourceDefinitionNames",
    "V1CustomResourceDefinitionSpec",
    "V1CustomResourceDefinitionStatus",
    "V1CustomResourceDefinitionVersion",
    "V1CustomResourceSubresourceScale",
    "V1CustomResourceSubresources",
    "V1CustomResourceValidation",
    "V1DaemonEndpoint",
    "V1DaemonSet",
    "V1DaemonSetCondition",
    "V1DaemonSetList",
    "V1DaemonSetSpec",
    "V1DaemonSetStatus",
    "V1DaemonSetUpdateStrategy",
    "V1DeleteOptions",
    "V1Deployment",
    "V1DeploymentCondition",
    "V1DeploymentList",
    "V1DeploymentSpec",
    "V1DeploymentStatus",
    "V1DeploymentStrategy",
    "V1DownwardAPIProjection",
    "V1DownwardAPIVolumeFile",
    "V1DownwardAPIVolumeSource",
    "V1EmptyDirVolumeSource",
    "V1Endpoint",
    "V1EndpointAddress",
    "V1EndpointConditions",
    "V1EndpointHints",
    "V1EndpointSlice",
    "V1EndpointSliceList",
    "V1EndpointSubset",
    "V1Endpoints",
    "V1EndpointsList",
    "V1EnvFromSource",
    "V1EnvVar",
    "V1EnvVarSource",
    "V1EphemeralContainer",
    "V1EphemeralVolumeSource",
    "V1EventSource",
    "V1Eviction",
    "V1ExecAction",
    "V1ExternalDocumentation",
    "V1FCVolumeSource",
    "V1FlexPersistentVolumeSource",
    "V1FlexVolumeSource",
    "V1FlockerVolumeSource",
    "V1ForZone",
    "V1GCEPersistentDiskVolumeSource",
    "V1GRPCAction",
    "V1GitRepoVolumeSource",
    "V1GlusterfsPersistentVolumeSource",
    "V1GlusterfsVolumeSource",
    "V1GroupVersionForDiscovery",
    "V1HTTPGetAction",
    "V1HTTPHeader",
    "V1HTTPIngressPath",
    "V1HTTPIngressRuleValue",
    "V1HorizontalPodAutoscaler",
    "V1HorizontalPodAutoscalerList",
    "V1HorizontalPodAutoscalerSpec",
    "V1HorizontalPodAutoscalerStatus",
    "V1HostAlias",
    "V1HostPathVolumeSource",
    "V1IPBlock",
    "V1ISCSIPersistentVolumeSource",
    "V1ISCSIVolumeSource",
    "V1Ingress",
    "V1IngressBackend",
    "V1IngressClass",
    "V1IngressClassList",
    "V1IngressClassParametersReference",
    "V1IngressClassSpec",
    "V1IngressList",
    "V1IngressLoadBalancerIngress",
    "V1IngressLoadBalancerStatus",
    "V1IngressPortStatus",
    "V1IngressRule",
    "V1IngressServiceBackend",
    "V1IngressSpec",
    "V1IngressStatus",
    "V1IngressTLS",
    "V1JSONSchemaProps",
    "V1Job",
    "V1JobCondition",
    "V1JobList",
    "V1JobSpec",
    "V1JobStatus",
    "V1JobTemplateSpec",
    "V1KeyToPath",
    "V1LabelSelector",
    "V1LabelSelectorRequirement",
    "V1Lease",
    "V1LeaseList",
    "V1LeaseSpec",
    "V1Lifecycle",
    "V1LifecycleHandler",
    "V1LimitRange",
    "V1LimitRangeItem",
    "V1LimitRangeList",
    "V1LimitRangeSpec",
    "V1ListMeta",
    "V1LoadBalancerIngress",
    "V1LoadBalancerStatus",
    "V1LocalObjectReference",
    "V1LocalSubjectAccessReview",
    "V1LocalVolumeSource",
    "V1ManagedFieldsEntry",
    "V1MutatingWebhook",
    "V1MutatingWebhookConfiguration",
    "V1MutatingWebhookConfigurationList",
    "V1NFSVolumeSource",
    "V1Namespace",
    "V1NamespaceCondition",
    "V1NamespaceList",
    "V1NamespaceSpec",
    "V1NamespaceStatus",
    "V1NetworkPolicy",
    "V1NetworkPolicyEgressRule",
    "V1NetworkPolicyIngressRule",
    "V1NetworkPolicyList",
    "V1NetworkPolicyPeer",
    "V1NetworkPolicyPort",
    "V1NetworkPolicySpec",
    "V1NetworkPolicyStatus",
    "V1Node",
    "V1NodeAddress",
    "V1NodeAffinity",
    "V1NodeCondition",
    "V1NodeConfigSource",
    "V1NodeConfigStatus",
    "V1NodeDaemonEndpoints",
    "V1NodeList",
    "V1NodeSelector",
    "V1NodeSelectorRequirement",
    "V1NodeSelectorTerm",
    "V1NodeSpec",
    "V1NodeStatus",
    "V1NodeSystemInfo",
    "V1NonResourceAttributes",
    "V1NonResourceRule",
    "V1ObjectFieldSelector",
    "V1ObjectMeta",
    "V1ObjectReference",
    "V1Overhead",
    "V1OwnerReference",
    "V1PersistentVolume",
    "V1PersistentVolumeClaim",
    "V1PersistentVolumeClaimCondition",
    "V1PersistentVolumeClaimList",
    "V1PersistentVolumeClaimSpec",
    "V1PersistentVolumeClaimStatus",
    "V1PersistentVolumeClaimTemplate",
    "V1PersistentVolumeClaimVolumeSource",
    "V1PersistentVolumeList",
    "V1PersistentVolumeSpec",
    "V1PersistentVolumeStatus",
    "V1PhotonPersistentDiskVolumeSource",
    "V1Pod",
    "V1PodAffinity",
    "V1PodAffinityTerm",
    "V1PodAntiAffinity",
    "V1PodCondition",
    "V1PodDNSConfig",
    "V1PodDNSConfigOption",
    "V1PodDisruptionBudget",
    "V1PodDisruptionBudgetList",
    "V1PodDisruptionBudgetSpec",
    "V1PodDisruptionBudgetStatus",
    "V1PodFailurePolicy",
    "V1PodFailurePolicyOnExitCodesRequirement",
    "V1PodFailurePolicyOnPodConditionsPattern",
    "V1PodFailurePolicyRule",
    "V1PodIP",
    "V1PodList",
    "V1PodOS",
    "V1PodReadinessGate",
    "V1PodResourceClaim",
    "V1PodSchedulingGate",
    "V1PodSecurityContext",
    "V1PodSpec",
    "V1PodStatus",
    "V1PodTemplate",
    "V1PodTemplateList",
    "V1PodTemplateSpec",
    "V1PolicyRule",
    "V1PortStatus",
    "V1PortworxVolumeSource",
    "V1Preconditions",
    "V1PreferredSchedulingTerm",
    "V1PriorityClass",
    "V1PriorityClassList",
    "V1Probe",
    "V1ProjectedVolumeSource",
    "V1QuobyteVolumeSource",
    "V1RBDPersistentVolumeSource",
    "V1RBDVolumeSource",
    "V1ReplicaSet",
    "V1ReplicaSetCondition",
    "V1ReplicaSetList",
    "V1ReplicaSetSpec",
    "V1ReplicaSetStatus",
    "V1ReplicationController",
    "V1ReplicationControllerCondition",
    "V1ReplicationControllerList",
    "V1ReplicationControllerSpec",
    "V1ReplicationControllerStatus",
    "V1ResourceAttributes",
    "V1ResourceClaim",
    "V1ResourceFieldSelector",
    "V1ResourceQuota",
    "V1ResourceQuotaList",
    "V1ResourceQuotaSpec",
    "V1ResourceQuotaStatus",
    "V1ResourceRequirements",
    "V1ResourceRule",
    "V1Role",
    "V1RoleBinding",
    "V1RoleBindingList",
    "V1RoleList",
    "V1RoleRef",
    "V1RollingUpdateDaemonSet",
    "V1RollingUpdateDeployment",
    "V1RollingUpdateStatefulSetStrategy",
    "V1RuleWithOperations",
    "V1RuntimeClass",
    "V1RuntimeClassList",
    "V1SELinuxOptions",
    "V1Scale",
    "V1ScaleIOPersistentVolumeSource",
    "V1ScaleIOVolumeSource",
    "V1ScaleSpec",
    "V1ScaleStatus",
    "V1Scheduling",
    "V1ScopeSelector",
    "V1ScopedResourceSelectorRequirement",
    "V1SeccompProfile",
    "V1Secret",
    "V1SecretEnvSource",
    "V1SecretKeySelector",
    "V1SecretList",
    "V1SecretProjection",
    "V1SecretReference",
    "V1SecretVolumeSource",
    "V1SecurityContext",
    "V1SelfSubjectAccessReview",
    "V1SelfSubjectAccessReviewSpec",
    "V1SelfSubjectRulesReview",
    "V1SelfSubjectRulesReviewSpec",
    "V1ServerAddressByClientCIDR",
    "V1Service",
    "V1ServiceAccount",
    "V1ServiceAccountList",
    "V1ServiceAccountTokenProjection",
    "V1ServiceBackendPort",
    "V1ServiceList",
    "V1ServicePort",
    "V1ServiceSpec",
    "V1ServiceStatus",
    "V1SessionAffinityConfig",
    "V1StatefulSet",
    "V1StatefulSetCondition",
    "V1StatefulSetList",
    "V1StatefulSetOrdinals",
    "V1StatefulSetPersistentVolumeClaimRetentionPolicy",
    "V1StatefulSetSpec",
    "V1StatefulSetStatus",
    "V1StatefulSetUpdateStrategy",
    "V1Status",
    "V1StatusCause",
    "V1StatusDetails",
    "V1StorageClass",
    "V1StorageClassList",
    "V1StorageOSPersistentVolumeSource",
    "V1StorageOSVolumeSource",
    "V1Subject",
    "V1SubjectAccessReview",
    "V1SubjectAccessReviewSpec",
    "V1SubjectAccessReviewStatus",
    "V1SubjectRulesReviewStatus",
    "V1Sysctl",
    "V1TCPSocketAction",
    "V1Taint",
    "V1TokenRequestSpec",
    "V1TokenRequestStatus",
    "V1TokenReview",
    "V1TokenReviewSpec",
    "V1TokenReviewStatus",
    "V1Toleration",
    "V1TopologySelectorLabelRequirement",
    "V1TopologySelectorTerm",
    "V1TopologySpreadConstraint",
    "V1TypedLocalObjectReference",
    "V1TypedObjectReference",
    "V1UncountedTerminatedPods",
    "V1UserInfo",
    "V1ValidatingWebhook",
    "V1ValidatingWebhookConfiguration",
    "V1ValidatingWebhookConfigurationList",
    "V1Volume",
    "V1VolumeAttachment",
    "V1VolumeAttachmentList",
    "V1VolumeAttachmentSource",
    "V1VolumeAttachmentSpec",
    "V1VolumeAttachmentStatus",
    "V1VolumeDevice",
    "V1VolumeError",
    "V1VolumeMount",
    "V1VolumeNodeAffinity",
    "V1VolumeNodeResources",
    "V1VolumeProjection",
    "V1VsphereVirtualDiskVolumeSource",
    "V1WebhookConversion",
    "V1WeightedPodAffinityTerm",
    "V1WindowsSecurityContextOptions",
    "V1alpha1AllocationResult",
    "V1alpha1ClusterCIDR",
    "V1alpha1ClusterCIDRList",
    "V1alpha1ClusterCIDRSpec",
    "V1alpha1MatchResources",
    "V1alpha1NamedRuleWithOperations",
    "V1alpha1ParamKind",
    "V1alpha1ParamRef",
    "V1alpha1PodScheduling",
    "V1alpha1PodSchedulingList",
    "V1alpha1PodSchedulingSpec",
    "V1alpha1PodSchedulingStatus",
    "V1alpha1ResourceClaim",
    "V1alpha1ResourceClaimConsumerReference",
    "V1alpha1ResourceClaimList",
    "V1alpha1ResourceClaimParametersReference",
    "V1alpha1ResourceClaimSchedulingStatus",
    "V1alpha1ResourceClaimSpec",
    "V1alpha1ResourceClaimStatus",
    "V1alpha1ResourceClaimTemplate",
    "V1alpha1ResourceClaimTemplateList",
    "V1alpha1ResourceClaimTemplateSpec",
    "V1alpha1ResourceClass",
    "V1alpha1ResourceClassList",
    "V1alpha1ResourceClassParametersReference",
    "V1alpha1SelfSubjectReview",
    "V1alpha1SelfSubjectReviewStatus",
    "V1alpha1ServerStorageVersion",
    "V1alpha1StorageVersion",
    "V1alpha1StorageVersionCondition",
    "V1alpha1StorageVersionList",
    "V1alpha1StorageVersionStatus",
    "V1alpha1ValidatingAdmissionPolicy",
    "V1alpha1ValidatingAdmissionPolicyBinding",
    "V1alpha1ValidatingAdmissionPolicyBindingList",
    "V1alpha1ValidatingAdmissionPolicyBindingSpec",
    "V1alpha1ValidatingAdmissionPolicyList",
    "V1alpha1ValidatingAdmissionPolicySpec",
    "V1alpha1Validation",
    "V1beta1CSIStorageCapacity",
    "V1beta1CSIStorageCapacityList",
    "V1beta2FlowDistinguisherMethod",
    "V1beta2FlowSchema",
    "V1beta2FlowSchemaCondition",
    "V1beta2FlowSchemaList",
    "V1beta2FlowSchemaSpec",
    "V1beta2FlowSchemaStatus",
    "V1beta2GroupSubject",
    "V1beta2LimitResponse",
    "V1beta2LimitedPriorityLevelConfiguration",
    "V1beta2NonResourcePolicyRule",
    "V1beta2PolicyRulesWithSubjects",
    "V1beta2PriorityLevelConfiguration",
    "V1beta2PriorityLevelConfigurationCondition",
    "V1beta2PriorityLevelConfigurationList",
    "V1beta2PriorityLevelConfigurationReference",
    "V1beta2PriorityLevelConfigurationSpec",
    "V1beta2PriorityLevelConfigurationStatus",
    "V1beta2QueuingConfiguration",
    "V1beta2ResourcePolicyRule",
    "V1beta2ServiceAccountSubject",
    "V1beta2Subject",
    "V1beta2UserSubject",
    "V1beta3FlowDistinguisherMethod",
    "V1beta3FlowSchema",
    "V1beta3FlowSchemaCondition",
    "V1beta3FlowSchemaList",
    "V1beta3FlowSchemaSpec",
    "V1beta3FlowSchemaStatus",
    "V1beta3GroupSubject",
    "V1beta3LimitResponse",
    "V1beta3LimitedPriorityLevelConfiguration",
    "V1beta3NonResourcePolicyRule",
    "V1beta3PolicyRulesWithSubjects",
    "V1beta3PriorityLevelConfiguration",
    "V1beta3PriorityLevelConfigurationCondition",
    "V1beta3PriorityLevelConfigurationList",
    "V1beta3PriorityLevelConfigurationReference",
    "V1beta3PriorityLevelConfigurationSpec",
    "V1beta3PriorityLevelConfigurationStatus",
    "V1beta3QueuingConfiguration",
    "V1beta3ResourcePolicyRule",
    "V1beta3ServiceAccountSubject",
    "V1beta3Subject",
    "V1beta3UserSubject",
    "V2ContainerResourceMetricSource",
    "V2ContainerResourceMetricStatus",
    "V2CrossVersionObjectReference",
    "V2ExternalMetricSource",
    "V2ExternalMetricStatus",
    "V2HPAScalingPolicy",
    "V2HPAScalingRules",
    "V2HorizontalPodAutoscaler",
    "V2HorizontalPodAutoscalerBehavior",
    "V2HorizontalPodAutoscalerCondition",
    "V2HorizontalPodAutoscalerList",
    "V2HorizontalPodAutoscalerSpec",
    "V2HorizontalPodAutoscalerStatus",
    "V2MetricIdentifier",
    "V2MetricSpec",
    "V2MetricStatus",
    "V2MetricTarget",
    "V2MetricValueStatus",
    "V2ObjectMetricSource",
    "V2ObjectMetricStatus",
    "V2PodsMetricSource",
    "V2PodsMetricStatus",
    "V2ResourceMetricSource",
    "V2ResourceMetricStatus",
]

from kubernetes_dynamic.models.all import (
    AdmissionregistrationV1ServiceReference,
    AdmissionregistrationV1WebhookClientConfig,
    ApiextensionsV1ServiceReference,
    ApiextensionsV1WebhookClientConfig,
    ApiregistrationV1ServiceReference,
    AuthenticationV1TokenRequest,
    CoreV1EndpointPort,
    CoreV1Event,
    CoreV1EventList,
    CoreV1EventSeries,
    DiscoveryV1EndpointPort,
    EventsV1Event,
    EventsV1EventList,
    EventsV1EventSeries,
    StorageV1TokenRequest,
    V1Affinity,
    V1AggregationRule,
    V1alpha1AllocationResult,
    V1alpha1ClusterCIDR,
    V1alpha1ClusterCIDRList,
    V1alpha1ClusterCIDRSpec,
    V1alpha1MatchResources,
    V1alpha1NamedRuleWithOperations,
    V1alpha1ParamKind,
    V1alpha1ParamRef,
    V1alpha1PodScheduling,
    V1alpha1PodSchedulingList,
    V1alpha1PodSchedulingSpec,
    V1alpha1PodSchedulingStatus,
    V1alpha1ResourceClaim,
    V1alpha1ResourceClaimConsumerReference,
    V1alpha1ResourceClaimList,
    V1alpha1ResourceClaimParametersReference,
    V1alpha1ResourceClaimSchedulingStatus,
    V1alpha1ResourceClaimSpec,
    V1alpha1ResourceClaimStatus,
    V1alpha1ResourceClaimTemplate,
    V1alpha1ResourceClaimTemplateList,
    V1alpha1ResourceClaimTemplateSpec,
    V1alpha1ResourceClass,
    V1alpha1ResourceClassList,
    V1alpha1ResourceClassParametersReference,
    V1alpha1SelfSubjectReview,
    V1alpha1SelfSubjectReviewStatus,
    V1alpha1ServerStorageVersion,
    V1alpha1StorageVersion,
    V1alpha1StorageVersionCondition,
    V1alpha1StorageVersionList,
    V1alpha1StorageVersionStatus,
    V1alpha1ValidatingAdmissionPolicy,
    V1alpha1ValidatingAdmissionPolicyBinding,
    V1alpha1ValidatingAdmissionPolicyBindingList,
    V1alpha1ValidatingAdmissionPolicyBindingSpec,
    V1alpha1ValidatingAdmissionPolicyList,
    V1alpha1ValidatingAdmissionPolicySpec,
    V1alpha1Validation,
    V1APIGroup,
    V1APIGroupList,
    V1APIResource,
    V1APIResourceList,
    V1APIService,
    V1APIServiceCondition,
    V1APIServiceList,
    V1APIServiceSpec,
    V1APIServiceStatus,
    V1APIVersions,
    V1AttachedVolume,
    V1AWSElasticBlockStoreVolumeSource,
    V1AzureDiskVolumeSource,
    V1AzureFilePersistentVolumeSource,
    V1AzureFileVolumeSource,
    V1beta1CSIStorageCapacity,
    V1beta1CSIStorageCapacityList,
    V1beta2FlowDistinguisherMethod,
    V1beta2FlowSchema,
    V1beta2FlowSchemaCondition,
    V1beta2FlowSchemaList,
    V1beta2FlowSchemaSpec,
    V1beta2FlowSchemaStatus,
    V1beta2GroupSubject,
    V1beta2LimitedPriorityLevelConfiguration,
    V1beta2LimitResponse,
    V1beta2NonResourcePolicyRule,
    V1beta2PolicyRulesWithSubjects,
    V1beta2PriorityLevelConfiguration,
    V1beta2PriorityLevelConfigurationCondition,
    V1beta2PriorityLevelConfigurationList,
    V1beta2PriorityLevelConfigurationReference,
    V1beta2PriorityLevelConfigurationSpec,
    V1beta2PriorityLevelConfigurationStatus,
    V1beta2QueuingConfiguration,
    V1beta2ResourcePolicyRule,
    V1beta2ServiceAccountSubject,
    V1beta2Subject,
    V1beta2UserSubject,
    V1beta3FlowDistinguisherMethod,
    V1beta3FlowSchema,
    V1beta3FlowSchemaCondition,
    V1beta3FlowSchemaList,
    V1beta3FlowSchemaSpec,
    V1beta3FlowSchemaStatus,
    V1beta3GroupSubject,
    V1beta3LimitedPriorityLevelConfiguration,
    V1beta3LimitResponse,
    V1beta3NonResourcePolicyRule,
    V1beta3PolicyRulesWithSubjects,
    V1beta3PriorityLevelConfiguration,
    V1beta3PriorityLevelConfigurationCondition,
    V1beta3PriorityLevelConfigurationList,
    V1beta3PriorityLevelConfigurationReference,
    V1beta3PriorityLevelConfigurationSpec,
    V1beta3PriorityLevelConfigurationStatus,
    V1beta3QueuingConfiguration,
    V1beta3ResourcePolicyRule,
    V1beta3ServiceAccountSubject,
    V1beta3Subject,
    V1beta3UserSubject,
    V1Binding,
    V1BoundObjectReference,
    V1Capabilities,
    V1CephFSPersistentVolumeSource,
    V1CephFSVolumeSource,
    V1CertificateSigningRequest,
    V1CertificateSigningRequestCondition,
    V1CertificateSigningRequestList,
    V1CertificateSigningRequestSpec,
    V1CertificateSigningRequestStatus,
    V1CinderPersistentVolumeSource,
    V1CinderVolumeSource,
    V1ClaimSource,
    V1ClientIPConfig,
    V1ClusterRole,
    V1ClusterRoleBinding,
    V1ClusterRoleBindingList,
    V1ClusterRoleList,
    V1ComponentCondition,
    V1ComponentStatus,
    V1ComponentStatusList,
    V1Condition,
    V1ConfigMap,
    V1ConfigMapEnvSource,
    V1ConfigMapKeySelector,
    V1ConfigMapList,
    V1ConfigMapNodeConfigSource,
    V1ConfigMapProjection,
    V1ConfigMapVolumeSource,
    V1Container,
    V1ContainerImage,
    V1ContainerPort,
    V1ContainerState,
    V1ContainerStateRunning,
    V1ContainerStateTerminated,
    V1ContainerStateWaiting,
    V1ContainerStatus,
    V1ControllerRevision,
    V1ControllerRevisionList,
    V1CronJob,
    V1CronJobList,
    V1CronJobSpec,
    V1CronJobStatus,
    V1CrossVersionObjectReference,
    V1CSIDriver,
    V1CSIDriverList,
    V1CSIDriverSpec,
    V1CSINode,
    V1CSINodeDriver,
    V1CSINodeList,
    V1CSINodeSpec,
    V1CSIPersistentVolumeSource,
    V1CSIStorageCapacity,
    V1CSIStorageCapacityList,
    V1CSIVolumeSource,
    V1CustomResourceColumnDefinition,
    V1CustomResourceConversion,
    V1CustomResourceDefinition,
    V1CustomResourceDefinitionCondition,
    V1CustomResourceDefinitionList,
    V1CustomResourceDefinitionNames,
    V1CustomResourceDefinitionSpec,
    V1CustomResourceDefinitionStatus,
    V1CustomResourceDefinitionVersion,
    V1CustomResourceSubresources,
    V1CustomResourceSubresourceScale,
    V1CustomResourceValidation,
    V1DaemonEndpoint,
    V1DaemonSet,
    V1DaemonSetCondition,
    V1DaemonSetList,
    V1DaemonSetSpec,
    V1DaemonSetStatus,
    V1DaemonSetUpdateStrategy,
    V1DeleteOptions,
    V1Deployment,
    V1DeploymentCondition,
    V1DeploymentList,
    V1DeploymentSpec,
    V1DeploymentStatus,
    V1DeploymentStrategy,
    V1DownwardAPIProjection,
    V1DownwardAPIVolumeFile,
    V1DownwardAPIVolumeSource,
    V1EmptyDirVolumeSource,
    V1Endpoint,
    V1EndpointAddress,
    V1EndpointConditions,
    V1EndpointHints,
    V1Endpoints,
    V1EndpointSlice,
    V1EndpointSliceList,
    V1EndpointsList,
    V1EndpointSubset,
    V1EnvFromSource,
    V1EnvVar,
    V1EnvVarSource,
    V1EphemeralContainer,
    V1EphemeralVolumeSource,
    V1EventSource,
    V1Eviction,
    V1ExecAction,
    V1ExternalDocumentation,
    V1FCVolumeSource,
    V1FlexPersistentVolumeSource,
    V1FlexVolumeSource,
    V1FlockerVolumeSource,
    V1ForZone,
    V1GCEPersistentDiskVolumeSource,
    V1GitRepoVolumeSource,
    V1GlusterfsPersistentVolumeSource,
    V1GlusterfsVolumeSource,
    V1GroupVersionForDiscovery,
    V1GRPCAction,
    V1HorizontalPodAutoscaler,
    V1HorizontalPodAutoscalerList,
    V1HorizontalPodAutoscalerSpec,
    V1HorizontalPodAutoscalerStatus,
    V1HostAlias,
    V1HostPathVolumeSource,
    V1HTTPGetAction,
    V1HTTPHeader,
    V1HTTPIngressPath,
    V1HTTPIngressRuleValue,
    V1Ingress,
    V1IngressBackend,
    V1IngressClass,
    V1IngressClassList,
    V1IngressClassParametersReference,
    V1IngressClassSpec,
    V1IngressList,
    V1IngressLoadBalancerIngress,
    V1IngressLoadBalancerStatus,
    V1IngressPortStatus,
    V1IngressRule,
    V1IngressServiceBackend,
    V1IngressSpec,
    V1IngressStatus,
    V1IngressTLS,
    V1IPBlock,
    V1ISCSIPersistentVolumeSource,
    V1ISCSIVolumeSource,
    V1Job,
    V1JobCondition,
    V1JobList,
    V1JobSpec,
    V1JobStatus,
    V1JobTemplateSpec,
    V1JSONSchemaProps,
    V1KeyToPath,
    V1LabelSelector,
    V1LabelSelectorRequirement,
    V1Lease,
    V1LeaseList,
    V1LeaseSpec,
    V1Lifecycle,
    V1LifecycleHandler,
    V1LimitRange,
    V1LimitRangeItem,
    V1LimitRangeList,
    V1LimitRangeSpec,
    V1ListMeta,
    V1LoadBalancerIngress,
    V1LoadBalancerStatus,
    V1LocalObjectReference,
    V1LocalSubjectAccessReview,
    V1LocalVolumeSource,
    V1ManagedFieldsEntry,
    V1MutatingWebhook,
    V1MutatingWebhookConfiguration,
    V1MutatingWebhookConfigurationList,
    V1Namespace,
    V1NamespaceCondition,
    V1NamespaceList,
    V1NamespaceSpec,
    V1NamespaceStatus,
    V1NetworkPolicy,
    V1NetworkPolicyEgressRule,
    V1NetworkPolicyIngressRule,
    V1NetworkPolicyList,
    V1NetworkPolicyPeer,
    V1NetworkPolicyPort,
    V1NetworkPolicySpec,
    V1NetworkPolicyStatus,
    V1NFSVolumeSource,
    V1Node,
    V1NodeAddress,
    V1NodeAffinity,
    V1NodeCondition,
    V1NodeConfigSource,
    V1NodeConfigStatus,
    V1NodeDaemonEndpoints,
    V1NodeList,
    V1NodeSelector,
    V1NodeSelectorRequirement,
    V1NodeSelectorTerm,
    V1NodeSpec,
    V1NodeStatus,
    V1NodeSystemInfo,
    V1NonResourceAttributes,
    V1NonResourceRule,
    V1ObjectFieldSelector,
    V1ObjectMeta,
    V1ObjectReference,
    V1Overhead,
    V1OwnerReference,
    V1PersistentVolume,
    V1PersistentVolumeClaim,
    V1PersistentVolumeClaimCondition,
    V1PersistentVolumeClaimList,
    V1PersistentVolumeClaimSpec,
    V1PersistentVolumeClaimStatus,
    V1PersistentVolumeClaimTemplate,
    V1PersistentVolumeClaimVolumeSource,
    V1PersistentVolumeList,
    V1PersistentVolumeSpec,
    V1PersistentVolumeStatus,
    V1PhotonPersistentDiskVolumeSource,
    V1Pod,
    V1PodAffinity,
    V1PodAffinityTerm,
    V1PodAntiAffinity,
    V1PodCondition,
    V1PodDisruptionBudget,
    V1PodDisruptionBudgetList,
    V1PodDisruptionBudgetSpec,
    V1PodDisruptionBudgetStatus,
    V1PodDNSConfig,
    V1PodDNSConfigOption,
    V1PodFailurePolicy,
    V1PodFailurePolicyOnExitCodesRequirement,
    V1PodFailurePolicyOnPodConditionsPattern,
    V1PodFailurePolicyRule,
    V1PodIP,
    V1PodList,
    V1PodOS,
    V1PodReadinessGate,
    V1PodResourceClaim,
    V1PodSchedulingGate,
    V1PodSecurityContext,
    V1PodSpec,
    V1PodStatus,
    V1PodTemplate,
    V1PodTemplateList,
    V1PodTemplateSpec,
    V1PolicyRule,
    V1PortStatus,
    V1PortworxVolumeSource,
    V1Preconditions,
    V1PreferredSchedulingTerm,
    V1PriorityClass,
    V1PriorityClassList,
    V1Probe,
    V1ProjectedVolumeSource,
    V1QuobyteVolumeSource,
    V1RBDPersistentVolumeSource,
    V1RBDVolumeSource,
    V1ReplicaSet,
    V1ReplicaSetCondition,
    V1ReplicaSetList,
    V1ReplicaSetSpec,
    V1ReplicaSetStatus,
    V1ReplicationController,
    V1ReplicationControllerCondition,
    V1ReplicationControllerList,
    V1ReplicationControllerSpec,
    V1ReplicationControllerStatus,
    V1ResourceAttributes,
    V1ResourceClaim,
    V1ResourceFieldSelector,
    V1ResourceQuota,
    V1ResourceQuotaList,
    V1ResourceQuotaSpec,
    V1ResourceQuotaStatus,
    V1ResourceRequirements,
    V1ResourceRule,
    V1Role,
    V1RoleBinding,
    V1RoleBindingList,
    V1RoleList,
    V1RoleRef,
    V1RollingUpdateDaemonSet,
    V1RollingUpdateDeployment,
    V1RollingUpdateStatefulSetStrategy,
    V1RuleWithOperations,
    V1RuntimeClass,
    V1RuntimeClassList,
    V1Scale,
    V1ScaleIOPersistentVolumeSource,
    V1ScaleIOVolumeSource,
    V1ScaleSpec,
    V1ScaleStatus,
    V1Scheduling,
    V1ScopedResourceSelectorRequirement,
    V1ScopeSelector,
    V1SeccompProfile,
    V1Secret,
    V1SecretEnvSource,
    V1SecretKeySelector,
    V1SecretList,
    V1SecretProjection,
    V1SecretReference,
    V1SecretVolumeSource,
    V1SecurityContext,
    V1SelfSubjectAccessReview,
    V1SelfSubjectAccessReviewSpec,
    V1SelfSubjectRulesReview,
    V1SelfSubjectRulesReviewSpec,
    V1SELinuxOptions,
    V1ServerAddressByClientCIDR,
    V1Service,
    V1ServiceAccount,
    V1ServiceAccountList,
    V1ServiceAccountTokenProjection,
    V1ServiceBackendPort,
    V1ServiceList,
    V1ServicePort,
    V1ServiceSpec,
    V1ServiceStatus,
    V1SessionAffinityConfig,
    V1StatefulSet,
    V1StatefulSetCondition,
    V1StatefulSetList,
    V1StatefulSetOrdinals,
    V1StatefulSetPersistentVolumeClaimRetentionPolicy,
    V1StatefulSetSpec,
    V1StatefulSetStatus,
    V1StatefulSetUpdateStrategy,
    V1Status,
    V1StatusCause,
    V1StatusDetails,
    V1StorageClass,
    V1StorageClassList,
    V1StorageOSPersistentVolumeSource,
    V1StorageOSVolumeSource,
    V1Subject,
    V1SubjectAccessReview,
    V1SubjectAccessReviewSpec,
    V1SubjectAccessReviewStatus,
    V1SubjectRulesReviewStatus,
    V1Sysctl,
    V1Taint,
    V1TCPSocketAction,
    V1TokenRequestSpec,
    V1TokenRequestStatus,
    V1TokenReview,
    V1TokenReviewSpec,
    V1TokenReviewStatus,
    V1Toleration,
    V1TopologySelectorLabelRequirement,
    V1TopologySelectorTerm,
    V1TopologySpreadConstraint,
    V1TypedLocalObjectReference,
    V1TypedObjectReference,
    V1UncountedTerminatedPods,
    V1UserInfo,
    V1ValidatingWebhook,
    V1ValidatingWebhookConfiguration,
    V1ValidatingWebhookConfigurationList,
    V1Volume,
    V1VolumeAttachment,
    V1VolumeAttachmentList,
    V1VolumeAttachmentSource,
    V1VolumeAttachmentSpec,
    V1VolumeAttachmentStatus,
    V1VolumeDevice,
    V1VolumeError,
    V1VolumeMount,
    V1VolumeNodeAffinity,
    V1VolumeNodeResources,
    V1VolumeProjection,
    V1VsphereVirtualDiskVolumeSource,
    V1WebhookConversion,
    V1WeightedPodAffinityTerm,
    V1WindowsSecurityContextOptions,
    V2ContainerResourceMetricSource,
    V2ContainerResourceMetricStatus,
    V2CrossVersionObjectReference,
    V2ExternalMetricSource,
    V2ExternalMetricStatus,
    V2HorizontalPodAutoscaler,
    V2HorizontalPodAutoscalerBehavior,
    V2HorizontalPodAutoscalerCondition,
    V2HorizontalPodAutoscalerList,
    V2HorizontalPodAutoscalerSpec,
    V2HorizontalPodAutoscalerStatus,
    V2HPAScalingPolicy,
    V2HPAScalingRules,
    V2MetricIdentifier,
    V2MetricSpec,
    V2MetricStatus,
    V2MetricTarget,
    V2MetricValueStatus,
    V2ObjectMetricSource,
    V2ObjectMetricStatus,
    V2PodsMetricSource,
    V2PodsMetricStatus,
    V2ResourceMetricSource,
    V2ResourceMetricStatus,
)
