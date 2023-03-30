from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

import pydantic
from pydantic import Field

from ..resource import ResourceItem
from ..resource_value import ResourceValue
from .common import V1ListMeta as V1ListMeta
from .common import V1ManagedFieldsEntry as V1ManagedFieldsEntry
from .common import V1ObjectMeta, V1OwnerReference
from .configmap import V1ConfigMap
from .ingress import V1Ingress as V1Ingress
from .namespace import V1Namespace as V1Namespace
from .pod import V1Pod as V1Pod
from .secret import V1Secret as V1Secret
from .stateful_set import V1StatefulSet as V1StatefulSet


class V2HorizontalPodAutoscalerList(ResourceItem):
    items: List[V2HorizontalPodAutoscaler]
    metadata: V1ListMeta


class V2ResourceMetricStatus(ResourceValue):
    current: V2MetricValueStatus
    name: str


class V2PodsMetricStatus(ResourceValue):
    current: V2MetricValueStatus
    metric: V2MetricIdentifier


class V2ObjectMetricStatus(ResourceValue):
    current: V2MetricValueStatus
    describedObject: V2CrossVersionObjectReference
    metric: V2MetricIdentifier


class V2ExternalMetricStatus(ResourceValue):
    current: V2MetricValueStatus
    metric: V2MetricIdentifier


class V2MetricValueStatus(ResourceValue):
    averageUtilization: int
    averageValue: str
    value: str


class V2ContainerResourceMetricStatus(ResourceValue):
    container: str
    current: V2MetricValueStatus
    name: str


class V2MetricStatus(ResourceValue):
    containerResource: V2ContainerResourceMetricStatus
    external: V2ExternalMetricStatus
    object: V2ObjectMetricStatus
    pods: V2PodsMetricStatus
    resource: V2ResourceMetricStatus
    type: str


class V2HorizontalPodAutoscalerCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V2HorizontalPodAutoscalerStatus(ResourceValue):
    conditions: List[V2HorizontalPodAutoscalerCondition]
    currentMetrics: List[V2MetricStatus]
    currentReplicas: int
    desiredReplicas: int
    lastScaleTime: datetime
    observedGeneration: int


class V2ResourceMetricSource(ResourceValue):
    name: str
    target: V2MetricTarget


class V2PodsMetricSource(ResourceValue):
    metric: V2MetricIdentifier
    target: V2MetricTarget


class V2ObjectMetricSource(ResourceValue):
    describedObject: V2CrossVersionObjectReference
    metric: V2MetricIdentifier
    target: V2MetricTarget


class V2MetricIdentifier(ResourceValue):
    name: str
    selector: V1LabelSelector


class V2ExternalMetricSource(ResourceValue):
    metric: V2MetricIdentifier
    target: V2MetricTarget


class V2MetricTarget(ResourceValue):
    averageUtilization: int
    averageValue: str
    type: str
    value: str


class V2ContainerResourceMetricSource(ResourceValue):
    container: str
    name: str
    target: V2MetricTarget


class V2MetricSpec(ResourceValue):
    containerResource: V2ContainerResourceMetricSource
    external: V2ExternalMetricSource
    object: V2ObjectMetricSource
    pods: V2PodsMetricSource
    resource: V2ResourceMetricSource
    type: str


class V2HPAScalingPolicy(ResourceValue):
    periodSeconds: int
    type: str
    value: int


class V2HPAScalingRules(ResourceValue):
    policies: List[V2HPAScalingPolicy]
    selectPolicy: str
    stabilizationWindowSeconds: int


class V2HorizontalPodAutoscalerBehavior(ResourceValue):
    scaleDown: V2HPAScalingRules
    scaleUp: V2HPAScalingRules


class V2HorizontalPodAutoscalerSpec(ResourceValue):
    behavior: V2HorizontalPodAutoscalerBehavior
    maxReplicas: int
    metrics: List[V2MetricSpec]
    minReplicas: int
    scaleTargetRef: V2CrossVersionObjectReference


class V2HorizontalPodAutoscaler(ResourceItem):
    metadata: V1ObjectMeta
    spec: V2HorizontalPodAutoscalerSpec
    status: V2HorizontalPodAutoscalerStatus


class V2CrossVersionObjectReference(ResourceItem):
    name: str


class V1beta3PriorityLevelConfigurationList(ResourceItem):
    items: List[V1beta3PriorityLevelConfiguration]
    metadata: V1ListMeta


class V1beta3PriorityLevelConfigurationCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1beta3PriorityLevelConfigurationStatus(ResourceValue):
    conditions: List[V1beta3PriorityLevelConfigurationCondition]


class V1beta3QueuingConfiguration(ResourceValue):
    handSize: int
    queueLengthLimit: int
    queues: int


class V1beta3LimitResponse(ResourceValue):
    queuing: V1beta3QueuingConfiguration
    type: str


class V1beta3LimitedPriorityLevelConfiguration(ResourceValue):
    borrowingLimitPercent: int
    lendablePercent: int
    limitResponse: V1beta3LimitResponse
    nominalConcurrencyShares: int


class V1beta3PriorityLevelConfigurationSpec(ResourceValue):
    limited: V1beta3LimitedPriorityLevelConfiguration
    type: str


class V1beta3PriorityLevelConfiguration(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1beta3PriorityLevelConfigurationSpec
    status: V1beta3PriorityLevelConfigurationStatus


class V1beta3FlowSchemaList(ResourceItem):
    items: List[V1beta3FlowSchema]
    metadata: V1ListMeta


class V1beta3FlowSchemaCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1beta3FlowSchemaStatus(ResourceValue):
    conditions: List[V1beta3FlowSchemaCondition]


class V1beta3UserSubject(ResourceValue):
    name: str


class V1beta3ServiceAccountSubject(ResourceValue):
    name: str
    namespace: str


class V1beta3GroupSubject(ResourceValue):
    name: str


class V1beta3Subject(ResourceValue):
    group: V1beta3GroupSubject
    kind: str
    serviceAccount: V1beta3ServiceAccountSubject
    user: V1beta3UserSubject


class V1beta3ResourcePolicyRule(ResourceValue):
    apiGroups: List[str]
    clusterScope: bool
    namespaces: List[str]
    resources: List[str]
    verbs: List[str]


class V1beta3NonResourcePolicyRule(ResourceValue):
    nonResourceURLs: List[str]
    verbs: List[str]


class V1beta3PolicyRulesWithSubjects(ResourceValue):
    nonResourceRules: List[V1beta3NonResourcePolicyRule]
    resourceRules: List[V1beta3ResourcePolicyRule]
    subjects: List[V1beta3Subject]


class V1beta3PriorityLevelConfigurationReference(ResourceValue):
    name: str


class V1beta3FlowDistinguisherMethod(ResourceValue):
    type: str


class V1beta3FlowSchemaSpec(ResourceValue):
    distinguisherMethod: V1beta3FlowDistinguisherMethod
    matchingPrecedence: int
    priorityLevelConfiguration: V1beta3PriorityLevelConfigurationReference
    rules: List[V1beta3PolicyRulesWithSubjects]


class V1beta3FlowSchema(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1beta3FlowSchemaSpec
    status: V1beta3FlowSchemaStatus


class V1beta2PriorityLevelConfigurationList(ResourceItem):
    items: List[V1beta2PriorityLevelConfiguration]
    metadata: V1ListMeta


class V1beta2PriorityLevelConfigurationCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1beta2PriorityLevelConfigurationStatus(ResourceValue):
    conditions: List[V1beta2PriorityLevelConfigurationCondition]


class V1beta2QueuingConfiguration(ResourceValue):
    handSize: int
    queueLengthLimit: int
    queues: int


class V1beta2LimitResponse(ResourceValue):
    queuing: V1beta2QueuingConfiguration
    type: str


class V1beta2LimitedPriorityLevelConfiguration(ResourceValue):
    assuredConcurrencyShares: int
    borrowingLimitPercent: int
    lendablePercent: int
    limitResponse: V1beta2LimitResponse


class V1beta2PriorityLevelConfigurationSpec(ResourceValue):
    limited: V1beta2LimitedPriorityLevelConfiguration
    type: str


class V1beta2PriorityLevelConfiguration(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1beta2PriorityLevelConfigurationSpec
    status: V1beta2PriorityLevelConfigurationStatus


class V1beta2FlowSchemaList(ResourceItem):
    items: List[V1beta2FlowSchema]
    metadata: V1ListMeta


class V1beta2FlowSchemaCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1beta2FlowSchemaStatus(ResourceValue):
    conditions: List[V1beta2FlowSchemaCondition]


class V1beta2UserSubject(ResourceValue):
    name: str


class V1beta2ServiceAccountSubject(ResourceValue):
    name: str
    namespace: str


class V1beta2GroupSubject(ResourceValue):
    name: str


class V1beta2Subject(ResourceValue):
    group: V1beta2GroupSubject
    kind: str
    serviceAccount: V1beta2ServiceAccountSubject
    user: V1beta2UserSubject


class V1beta2ResourcePolicyRule(ResourceValue):
    apiGroups: List[str]
    clusterScope: bool
    namespaces: List[str]
    resources: List[str]
    verbs: List[str]


class V1beta2NonResourcePolicyRule(ResourceValue):
    nonResourceURLs: List[str]
    verbs: List[str]


class V1beta2PolicyRulesWithSubjects(ResourceValue):
    nonResourceRules: List[V1beta2NonResourcePolicyRule]
    resourceRules: List[V1beta2ResourcePolicyRule]
    subjects: List[V1beta2Subject]


class V1beta2PriorityLevelConfigurationReference(ResourceValue):
    name: str


class V1beta2FlowDistinguisherMethod(ResourceValue):
    type: str


class V1beta2FlowSchemaSpec(ResourceValue):
    distinguisherMethod: V1beta2FlowDistinguisherMethod
    matchingPrecedence: int
    priorityLevelConfiguration: V1beta2PriorityLevelConfigurationReference
    rules: List[V1beta2PolicyRulesWithSubjects]


class V1beta2FlowSchema(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1beta2FlowSchemaSpec
    status: V1beta2FlowSchemaStatus


class V1beta1CSIStorageCapacityList(ResourceItem):
    items: List[V1beta1CSIStorageCapacity]
    metadata: V1ListMeta


class V1beta1CSIStorageCapacity(ResourceItem):
    capacity: str
    maximumVolumeSize: str
    metadata: V1ObjectMeta
    nodeTopology: V1LabelSelector
    storageClassName: str


class V1alpha1ValidatingAdmissionPolicyList(ResourceItem):
    items: List[V1alpha1ValidatingAdmissionPolicy]
    metadata: V1ListMeta


class V1alpha1ValidatingAdmissionPolicyBindingList(ResourceItem):
    items: List[V1alpha1ValidatingAdmissionPolicyBinding]
    metadata: V1ListMeta


class V1alpha1ParamRef(ResourceValue):
    name: str
    namespace: str


class V1alpha1ValidatingAdmissionPolicyBindingSpec(ResourceValue):
    matchResources: V1alpha1MatchResources
    paramRef: V1alpha1ParamRef
    policyName: str


class V1alpha1ValidatingAdmissionPolicyBinding(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1alpha1ValidatingAdmissionPolicyBindingSpec


class V1alpha1Validation(ResourceValue):
    expression: str
    message: str
    reason: str


class V1alpha1NamedRuleWithOperations(ResourceValue):
    apiGroups: List[str]
    apiVersions: List[str]
    operations: List[str]
    resourceNames: List[str]
    resources: List[str]
    scope: str


class V1alpha1MatchResources(ResourceValue):
    excludeResourceRules: List[V1alpha1NamedRuleWithOperations]
    matchPolicy: str
    namespaceSelector: V1LabelSelector
    objectSelector: V1LabelSelector
    resourceRules: List[V1alpha1NamedRuleWithOperations]


class V1alpha1ValidatingAdmissionPolicySpec(ResourceValue):
    failurePolicy: str
    matchConstraints: V1alpha1MatchResources
    paramKind: V1alpha1ParamKind
    validations: List[V1alpha1Validation]


class V1alpha1ValidatingAdmissionPolicy(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1alpha1ValidatingAdmissionPolicySpec


class V1alpha1StorageVersionList(ResourceItem):
    items: List[V1alpha1StorageVersion]
    metadata: V1ListMeta


class V1alpha1ServerStorageVersion(ResourceValue):
    apiServerID: str
    decodableVersions: List[str]
    encodingVersion: str


class V1alpha1StorageVersionCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    observedGeneration: int
    reason: str
    status: str
    type: str


class V1alpha1StorageVersionStatus(ResourceValue):
    commonEncodingVersion: str
    conditions: List[V1alpha1StorageVersionCondition]
    storageVersions: List[V1alpha1ServerStorageVersion]


class V1alpha1StorageVersion(ResourceItem):
    metadata: V1ObjectMeta
    spec: object
    status: V1alpha1StorageVersionStatus


class V1alpha1SelfSubjectReviewStatus(ResourceValue):
    userInfo: V1UserInfo


class V1alpha1SelfSubjectReview(ResourceItem):
    metadata: V1ObjectMeta
    status: V1alpha1SelfSubjectReviewStatus


class V1alpha1ResourceClassList(ResourceItem):
    items: List[V1alpha1ResourceClass]
    metadata: V1ListMeta


class V1alpha1ResourceClassParametersReference(ResourceValue):
    apiGroup: str
    kind: str
    name: str
    namespace: str


class V1alpha1ResourceClass(ResourceItem):
    driverName: str
    metadata: V1ObjectMeta
    parametersRef: V1alpha1ResourceClassParametersReference
    suitableNodes: V1NodeSelector


class V1alpha1ResourceClaimTemplateList(ResourceItem):
    items: List[V1alpha1ResourceClaimTemplate]
    metadata: V1ListMeta


class V1alpha1ResourceClaimTemplateSpec(ResourceValue):
    metadata: V1ObjectMeta
    spec: V1alpha1ResourceClaimSpec


class V1alpha1ResourceClaimTemplate(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1alpha1ResourceClaimTemplateSpec


class V1alpha1ResourceClaimList(ResourceItem):
    items: List[V1alpha1ResourceClaim]
    metadata: V1ListMeta


class V1alpha1ResourceClaimConsumerReference(ResourceValue):
    apiGroup: str
    name: str
    resource: str
    uid: str


class V1alpha1AllocationResult(ResourceValue):
    availableOnNodes: V1NodeSelector
    resourceHandle: str
    shareable: bool


class V1alpha1ResourceClaimStatus(ResourceValue):
    allocation: V1alpha1AllocationResult
    deallocationRequested: bool
    driverName: str
    reservedFor: List[V1alpha1ResourceClaimConsumerReference]


class V1alpha1ResourceClaimParametersReference(ResourceValue):
    apiGroup: str
    kind: str
    name: str


class V1alpha1ResourceClaimSpec(ResourceValue):
    allocationMode: str
    parametersRef: V1alpha1ResourceClaimParametersReference
    resourceClassName: str


class V1alpha1ResourceClaim(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1alpha1ResourceClaimSpec
    status: V1alpha1ResourceClaimStatus


class V1alpha1PodSchedulingList(ResourceItem):
    items: List[V1alpha1PodScheduling]
    metadata: V1ListMeta


class V1alpha1ResourceClaimSchedulingStatus(ResourceValue):
    name: str
    unsuitableNodes: List[str]


class V1alpha1PodSchedulingStatus(ResourceValue):
    resourceClaims: List[V1alpha1ResourceClaimSchedulingStatus]


class V1alpha1PodSchedulingSpec(ResourceValue):
    potentialNodes: List[str]
    selectedNode: str


class V1alpha1PodScheduling(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1alpha1PodSchedulingSpec
    status: V1alpha1PodSchedulingStatus


class V1alpha1ParamKind(ResourceItem):
    pass


class V1alpha1ClusterCIDRList(ResourceItem):
    items: List[V1alpha1ClusterCIDR]
    metadata: V1ListMeta


class V1alpha1ClusterCIDRSpec(ResourceValue):
    ipv4: str
    ipv6: str
    nodeSelector: V1NodeSelector
    perNodeHostBits: int


class V1alpha1ClusterCIDR(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1alpha1ClusterCIDRSpec


class V1VolumeAttachmentList(ResourceItem):
    items: List[V1VolumeAttachment]
    metadata: V1ListMeta


class V1VolumeError(ResourceValue):
    message: str
    time: datetime


class V1VolumeAttachmentStatus(ResourceValue):
    attachError: V1VolumeError
    attached: bool
    attachmentMetadata: Dict[str, str]
    detachError: V1VolumeError


class V1VolumeAttachmentSource(ResourceValue):
    inlineVolumeSpec: V1PersistentVolumeSpec
    persistentVolumeName: str


class V1VolumeAttachmentSpec(ResourceValue):
    attacher: str
    nodeName: str
    source: V1VolumeAttachmentSource


class V1VolumeAttachment(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1VolumeAttachmentSpec
    status: V1VolumeAttachmentStatus


class V1ValidatingWebhookConfigurationList(ResourceItem):
    items: List[V1ValidatingWebhookConfiguration]
    metadata: V1ListMeta


class V1ValidatingWebhook(ResourceValue):
    admissionReviewVersions: List[str]
    clientConfig: AdmissionregistrationV1WebhookClientConfig
    failurePolicy: str
    matchPolicy: str
    name: str
    namespaceSelector: V1LabelSelector
    objectSelector: V1LabelSelector
    rules: List[V1RuleWithOperations]
    sideEffects: str
    timeoutSeconds: int


class V1ValidatingWebhookConfiguration(ResourceItem):
    metadata: V1ObjectMeta
    webhooks: List[V1ValidatingWebhook]


class V1UserInfo(ResourceValue):
    extra: Dict[str, List[str]]
    groups: List[str]
    uid: str
    username: str


class V1TokenReviewStatus(ResourceValue):
    audiences: List[str]
    authenticated: bool
    error: str
    user: V1UserInfo


class V1TokenReviewSpec(ResourceValue):
    audiences: List[str]
    token: str


class V1TokenReview(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1TokenReviewSpec
    status: V1TokenReviewStatus


class V1SubjectAccessReview(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1SubjectAccessReviewSpec
    status: V1SubjectAccessReviewStatus


class V1StorageClassList(ResourceItem):
    items: List[V1StorageClass]
    metadata: V1ListMeta


class V1TopologySelectorLabelRequirement(ResourceValue):
    key: str
    values: List[str]


class V1TopologySelectorTerm(ResourceValue):
    matchLabelExpressions: List[V1TopologySelectorLabelRequirement]


class V1StorageClass(ResourceItem):
    allowVolumeExpansion: bool
    allowedTopologies: List[V1TopologySelectorTerm]
    metadata: V1ObjectMeta
    mountOptions: List[str]
    parameters: Dict[str, str]
    provisioner: str
    reclaimPolicy: str
    volumeBindingMode: str


class V1StatusCause(ResourceValue):
    field: str
    message: str
    reason: str


class V1StatusDetails(ResourceValue):
    causes: List[V1StatusCause]
    group: str
    kind: str
    name: str
    retryAfterSeconds: int
    uid: str


class V1Status(ResourceItem):
    code: int
    details: V1StatusDetails
    message: str
    metadata: V1ListMeta
    reason: str
    status: str


class V1StatefulSetList(ResourceItem):
    items: List[V1StatefulSet]
    metadata: V1ListMeta


class V1StatefulSetCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1StatefulSetStatus(ResourceValue):
    availableReplicas: int
    collisionCount: int
    conditions: List[V1StatefulSetCondition]
    currentReplicas: int
    currentRevision: str
    observedGeneration: int
    readyReplicas: int
    replicas: int
    updateRevision: str
    updatedReplicas: int


class V1RollingUpdateStatefulSetStrategy(ResourceValue):
    maxUnavailable: object
    partition: int


class V1StatefulSetUpdateStrategy(ResourceValue):
    rollingUpdate: V1RollingUpdateStatefulSetStrategy
    type: str


class V1StatefulSetPersistentVolumeClaimRetentionPolicy(ResourceValue):
    whenDeleted: str
    whenScaled: str


class V1StatefulSetOrdinals(ResourceValue):
    start: int


class V1StatefulSetSpec(ResourceValue):
    minReadySeconds: int
    ordinals: V1StatefulSetOrdinals
    persistentVolumeClaimRetentionPolicy: V1StatefulSetPersistentVolumeClaimRetentionPolicy
    podManagementPolicy: str
    replicas: int
    revisionHistoryLimit: int
    selector: V1LabelSelector
    serviceName: str
    template: V1PodTemplateSpec
    updateStrategy: V1StatefulSetUpdateStrategy
    volumeClaimTemplates: List[V1PersistentVolumeClaim]


class V1ServiceList(ResourceItem):
    items: List[V1Service]
    metadata: V1ListMeta


class V1ServiceAccountList(ResourceItem):
    items: List[V1ServiceAccount]
    metadata: V1ListMeta


class V1ServiceAccount(ResourceItem):
    automountServiceAccountToken: bool
    imagePullSecrets: List[V1LocalObjectReference]
    metadata: V1ObjectMeta
    secrets: List[V1ObjectReference]


class V1PortStatus(ResourceValue):
    error: str
    port: int
    protocol: str


class V1LoadBalancerIngress(ResourceValue):
    hostname: str
    ip: str
    ports: List[V1PortStatus]


class V1LoadBalancerStatus(ResourceValue):
    ingress: List[V1LoadBalancerIngress]


class V1ServiceStatus(ResourceValue):
    conditions: List[V1Condition]
    loadBalancer: V1LoadBalancerStatus


class V1ClientIPConfig(ResourceValue):
    timeoutSeconds: int


class V1SessionAffinityConfig(ResourceValue):
    clientIP: V1ClientIPConfig


class V1ServicePort(ResourceValue):
    appProtocol: str
    name: str
    nodePort: int
    port: int
    protocol: str
    targetPort: object


class V1ServiceSpec(ResourceValue):
    allocateLoadBalancerNodePorts: bool
    clusterIP: str
    clusterIPs: List[str]
    externalIPs: List[str]
    externalName: str
    externalTrafficPolicy: str
    healthCheckNodePort: int
    internalTrafficPolicy: str
    ipFamilies: List[str]
    ipFamilyPolicy: str
    loadBalancerClass: str
    loadBalancerIP: str
    loadBalancerSourceRanges: List[str]
    ports: List[V1ServicePort]
    publishNotReadyAddresses: bool
    selector: Dict[str, str]
    sessionAffinity: str
    sessionAffinityConfig: V1SessionAffinityConfig
    type: str


class V1Service(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1ServiceSpec
    status: V1ServiceStatus


class V1ResourceRule(ResourceValue):
    apiGroups: List[str]
    resourceNames: List[str]
    resources: List[str]
    verbs: List[str]


class V1NonResourceRule(ResourceValue):
    nonResourceURLs: List[str]
    verbs: List[str]


class V1SubjectRulesReviewStatus(ResourceValue):
    evaluationError: str
    incomplete: bool
    nonResourceRules: List[V1NonResourceRule]
    resourceRules: List[V1ResourceRule]


class V1SelfSubjectRulesReviewSpec(ResourceValue):
    namespace: str


class V1SelfSubjectRulesReview(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1SelfSubjectRulesReviewSpec
    status: V1SubjectRulesReviewStatus


class V1SelfSubjectAccessReviewSpec(ResourceValue):
    nonResourceAttributes: V1NonResourceAttributes
    resourceAttributes: V1ResourceAttributes


class V1SelfSubjectAccessReview(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1SelfSubjectAccessReviewSpec
    status: V1SubjectAccessReviewStatus


class V1SecretList(ResourceItem):
    items: List[V1Secret]
    metadata: V1ListMeta


class V1ScaleStatus(ResourceValue):
    replicas: int
    selector: str


class V1ScaleSpec(ResourceValue):
    replicas: int


class V1Scale(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1ScaleSpec
    status: V1ScaleStatus


class V1RuntimeClassList(ResourceItem):
    items: List[V1RuntimeClass]
    metadata: V1ListMeta


class V1Scheduling(ResourceValue):
    nodeSelector: Dict[str, str]
    tolerations: List[V1Toleration]


class V1Overhead(ResourceValue):
    podFixed: Dict[str, str]


class V1RuntimeClass(ResourceItem):
    handler: str
    metadata: V1ObjectMeta
    overhead: V1Overhead
    scheduling: V1Scheduling


class V1RoleList(ResourceItem):
    items: List[V1Role]
    metadata: V1ListMeta


class V1RoleBindingList(ResourceItem):
    items: List[V1RoleBinding]
    metadata: V1ListMeta


class V1RoleBinding(ResourceItem):
    metadata: V1ObjectMeta
    roleRef: V1RoleRef
    subjects: List[V1Subject]


class V1Role(ResourceItem):
    metadata: V1ObjectMeta
    rules: List[V1PolicyRule]


class V1ResourceQuotaList(ResourceItem):
    items: List[V1ResourceQuota]
    metadata: V1ListMeta


class V1ResourceQuotaStatus(ResourceValue):
    hard: Dict[str, str]
    used: Dict[str, str]


class V1ScopedResourceSelectorRequirement(ResourceValue):
    operator: str
    scopeName: str
    values: List[str]


class V1ScopeSelector(ResourceValue):
    matchExpressions: List[V1ScopedResourceSelectorRequirement]


class V1ResourceQuotaSpec(ResourceValue):
    hard: Dict[str, str]
    scopeSelector: V1ScopeSelector
    scopes: List[str]


class V1ResourceQuota(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1ResourceQuotaSpec
    status: V1ResourceQuotaStatus


class V1ReplicationControllerList(ResourceItem):
    items: List[V1ReplicationController]
    metadata: V1ListMeta


class V1ReplicationControllerCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1ReplicationControllerStatus(ResourceValue):
    availableReplicas: int
    conditions: List[V1ReplicationControllerCondition]
    fullyLabeledReplicas: int
    observedGeneration: int
    readyReplicas: int
    replicas: int


class V1ReplicationControllerSpec(ResourceValue):
    minReadySeconds: int
    replicas: int
    selector: Dict[str, str]
    template: V1PodTemplateSpec


class V1ReplicationController(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1ReplicationControllerSpec
    status: V1ReplicationControllerStatus


class V1ReplicaSetList(ResourceItem):
    items: List[V1ReplicaSet]
    metadata: V1ListMeta


class V1ReplicaSetCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1ReplicaSetStatus(ResourceValue):
    availableReplicas: int
    conditions: List[V1ReplicaSetCondition]
    fullyLabeledReplicas: int
    observedGeneration: int
    readyReplicas: int
    replicas: int


class V1ReplicaSetSpec(ResourceValue):
    minReadySeconds: int
    replicas: int
    selector: V1LabelSelector
    template: V1PodTemplateSpec


class V1ReplicaSet(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1ReplicaSetSpec
    status: V1ReplicaSetStatus


class V1PriorityClassList(ResourceItem):
    items: List[V1PriorityClass]
    metadata: V1ListMeta


class V1PriorityClass(ResourceItem):
    description: str
    globalDefault: bool
    metadata: V1ObjectMeta
    preemptionPolicy: str
    value: int


class V1PodTemplateList(ResourceItem):
    items: List[V1PodTemplate]
    metadata: V1ListMeta


class V1PodTemplate(ResourceItem):
    metadata: V1ObjectMeta
    template: V1PodTemplateSpec


class V1PodList(ResourceItem):
    items: List[V1Pod]
    metadata: V1ListMeta


class V1PodDisruptionBudgetList(ResourceItem):
    items: List[V1PodDisruptionBudget]
    metadata: V1ListMeta


class V1PodDisruptionBudgetStatus(ResourceValue):
    conditions: List[V1Condition]
    currentHealthy: int
    desiredHealthy: int
    disruptedPods: Dict[str, datetime]
    disruptionsAllowed: int
    expectedPods: int
    observedGeneration: int


class V1PodDisruptionBudgetSpec(ResourceValue):
    maxUnavailable: object
    minAvailable: object
    selector: V1LabelSelector
    unhealthyPodEvictionPolicy: str


class V1PodDisruptionBudget(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1PodDisruptionBudgetSpec
    status: V1PodDisruptionBudgetStatus


class V1PodIP(ResourceValue):
    ip: str


class V1ContainerStateWaiting(ResourceValue):
    message: str
    reason: str


class V1ContainerStateTerminated(ResourceValue):
    containerID: str
    exitCode: int
    finishedAt: datetime
    message: str
    reason: str
    signal: int
    startedAt: datetime


class V1ContainerStateRunning(ResourceValue):
    startedAt: datetime


class V1ContainerState(ResourceValue):
    running: V1ContainerStateRunning
    terminated: V1ContainerStateTerminated
    waiting: V1ContainerStateWaiting


class V1ContainerStatus(ResourceValue):
    containerID: str
    image: str
    imageID: str
    lastState: V1ContainerState
    name: str
    ready: bool
    restartCount: int
    started: bool
    state: V1ContainerState


class V1PodCondition(ResourceValue):
    lastProbeTime: datetime
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1PodStatus(ResourceValue):
    conditions: List[V1PodCondition]
    containerStatuses: List[V1ContainerStatus]
    ephemeralContainerStatuses: List[V1ContainerStatus]
    hostIP: str
    initContainerStatuses: List[V1ContainerStatus]
    message: str
    nominatedNodeName: str
    phase: str
    podIP: str
    podIPs: List[V1PodIP]
    qosClass: str
    reason: str
    startTime: datetime


class V1PersistentVolumeList(ResourceItem):
    items: List[V1PersistentVolume]
    metadata: V1ListMeta


class V1PersistentVolumeClaimList(ResourceItem):
    items: List[V1PersistentVolumeClaim]
    metadata: V1ListMeta


class V1PersistentVolumeClaimCondition(ResourceValue):
    lastProbeTime: datetime
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1PersistentVolumeClaimStatus(ResourceValue):
    accessModes: List[str]
    allocatedResources: Dict[str, str]
    capacity: Dict[str, str]
    conditions: List[V1PersistentVolumeClaimCondition]
    phase: str
    resizeStatus: str


class V1PersistentVolumeClaim(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1PersistentVolumeClaimSpec
    status: V1PersistentVolumeClaimStatus


class V1PersistentVolumeStatus(ResourceValue):
    message: str
    phase: str
    reason: str


class V1StorageOSPersistentVolumeSource(ResourceValue):
    fsType: str
    readOnly: bool
    secretRef: V1ObjectReference
    volumeName: str
    volumeNamespace: str


class V1ScaleIOPersistentVolumeSource(ResourceValue):
    fsType: str
    gateway: str
    protectionDomain: str
    readOnly: bool
    secretRef: V1SecretReference
    sslEnabled: bool
    storageMode: str
    storagePool: str
    system: str
    volumeName: str


class V1RBDPersistentVolumeSource(ResourceValue):
    fsType: str
    image: str
    keyring: str
    monitors: List[str]
    pool: str
    readOnly: bool
    secretRef: V1SecretReference
    user: str


class V1VolumeNodeAffinity(ResourceValue):
    required: V1NodeSelector


class V1LocalVolumeSource(ResourceValue):
    fsType: str
    path: str


class V1ISCSIPersistentVolumeSource(ResourceValue):
    chapAuthDiscovery: bool
    chapAuthSession: bool
    fsType: str
    initiatorName: str
    iqn: str
    iscsiInterface: str
    lun: int
    portals: List[str]
    readOnly: bool
    secretRef: V1SecretReference
    targetPortal: str


class V1GlusterfsPersistentVolumeSource(ResourceValue):
    endpoints: str
    endpointsNamespace: str
    path: str
    readOnly: bool


class V1FlexPersistentVolumeSource(ResourceValue):
    driver: str
    fsType: str
    options: Dict[str, str]
    readOnly: bool
    secretRef: V1SecretReference


class V1CSIPersistentVolumeSource(ResourceValue):
    controllerExpandSecretRef: V1SecretReference
    controllerPublishSecretRef: V1SecretReference
    driver: str
    fsType: str
    nodeExpandSecretRef: V1SecretReference
    nodePublishSecretRef: V1SecretReference
    nodeStageSecretRef: V1SecretReference
    readOnly: bool
    volumeAttributes: Dict[str, str]
    volumeHandle: str


class V1CinderPersistentVolumeSource(ResourceValue):
    fsType: str
    readOnly: bool
    secretRef: V1SecretReference
    volumeID: str


class V1SecretReference(ResourceValue):
    name: str
    namespace: str


class V1CephFSPersistentVolumeSource(ResourceValue):
    monitors: List[str]
    path: str
    readOnly: bool
    secretFile: str
    secretRef: V1SecretReference
    user: str


class V1AzureFilePersistentVolumeSource(ResourceValue):
    readOnly: bool
    secretName: str
    secretNamespace: str
    shareName: str


class V1PersistentVolumeSpec(ResourceValue):
    accessModes: List[str]
    awsElasticBlockStore: V1AWSElasticBlockStoreVolumeSource
    azureDisk: V1AzureDiskVolumeSource
    azureFile: V1AzureFilePersistentVolumeSource
    capacity: Dict[str, str]
    cephfs: V1CephFSPersistentVolumeSource
    cinder: V1CinderPersistentVolumeSource
    claimRef: V1ObjectReference
    csi: V1CSIPersistentVolumeSource
    fc: V1FCVolumeSource
    flexVolume: V1FlexPersistentVolumeSource
    flocker: V1FlockerVolumeSource
    gcePersistentDisk: V1GCEPersistentDiskVolumeSource
    glusterfs: V1GlusterfsPersistentVolumeSource
    hostPath: V1HostPathVolumeSource
    iscsi: V1ISCSIPersistentVolumeSource
    local: V1LocalVolumeSource
    mountOptions: List[str]
    nfs: V1NFSVolumeSource
    nodeAffinity: V1VolumeNodeAffinity
    persistentVolumeReclaimPolicy: str
    photonPersistentDisk: V1PhotonPersistentDiskVolumeSource
    portworxVolume: V1PortworxVolumeSource
    quobyte: V1QuobyteVolumeSource
    rbd: V1RBDPersistentVolumeSource
    scaleIO: V1ScaleIOPersistentVolumeSource
    storageClassName: str
    storageos: V1StorageOSPersistentVolumeSource
    volumeMode: str
    vsphereVolume: V1VsphereVirtualDiskVolumeSource


class V1PersistentVolume(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1PersistentVolumeSpec
    status: V1PersistentVolumeStatus


class V1NodeList(ResourceItem):
    items: List[V1Node]
    metadata: V1ListMeta


class V1AttachedVolume(ResourceValue):
    devicePath: str
    name: str


class V1NodeSystemInfo(ResourceValue):
    architecture: str
    bootID: str
    containerRuntimeVersion: str
    kernelVersion: str
    kubeProxyVersion: str
    kubeletVersion: str
    machineID: str
    operatingSystem: str
    osImage: str
    systemUUID: str


class V1ContainerImage(ResourceValue):
    names: List[str]
    sizeBytes: int


class V1DaemonEndpoint(ResourceValue):
    Port: int


class V1NodeDaemonEndpoints(ResourceValue):
    kubeletEndpoint: V1DaemonEndpoint


class V1NodeConfigStatus(ResourceValue):
    active: V1NodeConfigSource
    assigned: V1NodeConfigSource
    error: str
    lastKnownGood: V1NodeConfigSource


class V1NodeCondition(ResourceValue):
    lastHeartbeatTime: datetime
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1NodeAddress(ResourceValue):
    address: str
    type: str


class V1NodeStatus(ResourceValue):
    addresses: List[V1NodeAddress]
    allocatable: Dict[str, str]
    capacity: Dict[str, str]
    conditions: List[V1NodeCondition]
    config: V1NodeConfigStatus
    daemonEndpoints: V1NodeDaemonEndpoints
    images: List[V1ContainerImage]
    nodeInfo: V1NodeSystemInfo
    phase: str
    volumesAttached: List[V1AttachedVolume]
    volumesInUse: List[str]


class V1Taint(ResourceValue):
    effect: str
    key: str
    timeAdded: datetime
    value: str


class V1ConfigMapNodeConfigSource(ResourceValue):
    kubeletConfigKey: str
    name: str
    namespace: str
    resourceVersion: str
    uid: str


class V1NodeConfigSource(ResourceValue):
    configMap: V1ConfigMapNodeConfigSource


class V1NodeSpec(ResourceValue):
    configSource: V1NodeConfigSource
    externalID: str
    podCIDR: str
    podCIDRs: List[str]
    providerID: str
    taints: List[V1Taint]
    unschedulable: bool


class V1Node(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1NodeSpec
    status: V1NodeStatus


class V1NetworkPolicyList(ResourceItem):
    items: List[V1NetworkPolicy]
    metadata: V1ListMeta


class V1Condition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    observedGeneration: int
    reason: str
    status: str
    type: str


class V1NetworkPolicyStatus(ResourceValue):
    conditions: List[V1Condition]


class V1NetworkPolicyIngressRule(ResourceValue):
    ports: List[V1NetworkPolicyPort]


class V1IPBlock(ResourceValue):
    cidr: str


class V1NetworkPolicyPeer(ResourceValue):
    ipBlock: V1IPBlock
    namespaceSelector: V1LabelSelector
    podSelector: V1LabelSelector


class V1NetworkPolicyPort(ResourceValue):
    endPort: int
    port: object
    protocol: str


class V1NetworkPolicyEgressRule(ResourceValue):
    ports: List[V1NetworkPolicyPort]
    to: List[V1NetworkPolicyPeer]


class V1NetworkPolicySpec(ResourceValue):
    egress: List[V1NetworkPolicyEgressRule]
    ingress: List[V1NetworkPolicyIngressRule]
    podSelector: V1LabelSelector
    policyTypes: List[str]


class V1NetworkPolicy(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1NetworkPolicySpec
    status: V1NetworkPolicyStatus


class V1NamespaceList(ResourceItem):
    items: List[V1Namespace]
    metadata: V1ListMeta


class V1NamespaceCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1NamespaceStatus(ResourceValue):
    conditions: List[V1NamespaceCondition]
    phase: str


class V1NamespaceSpec(ResourceValue):
    finalizers: List[str]


class V1MutatingWebhookConfigurationList(ResourceItem):
    items: List[V1MutatingWebhookConfiguration]
    metadata: V1ListMeta


class V1RuleWithOperations(ResourceValue):
    apiGroups: List[str]
    apiVersions: List[str]
    operations: List[str]
    resources: List[str]
    scope: str


class AdmissionregistrationV1ServiceReference(ResourceValue):
    name: str
    namespace: str
    path: str
    port: int


class AdmissionregistrationV1WebhookClientConfig(ResourceValue):
    caBundle: str
    service: AdmissionregistrationV1ServiceReference
    url: str


class V1MutatingWebhook(ResourceValue):
    admissionReviewVersions: List[str]
    clientConfig: AdmissionregistrationV1WebhookClientConfig
    failurePolicy: str
    matchPolicy: str
    name: str
    namespaceSelector: V1LabelSelector
    objectSelector: V1LabelSelector
    reinvocationPolicy: str
    rules: List[V1RuleWithOperations]
    sideEffects: str
    timeoutSeconds: int


class V1MutatingWebhookConfiguration(ResourceItem):
    metadata: V1ObjectMeta
    webhooks: List[V1MutatingWebhook]


class V1SubjectAccessReviewStatus(ResourceValue):
    allowed: bool
    denied: bool
    evaluationError: str
    reason: str


class V1ResourceAttributes(ResourceValue):
    group: str
    name: str
    namespace: str
    resource: str
    subresource: str
    verb: str
    version: str


class V1NonResourceAttributes(ResourceValue):
    path: str
    verb: str


class V1SubjectAccessReviewSpec(ResourceValue):
    extra: Dict[str, List[str]]
    groups: List[str]
    nonResourceAttributes: V1NonResourceAttributes
    resourceAttributes: V1ResourceAttributes
    uid: str
    user: str


class V1LocalSubjectAccessReview(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1SubjectAccessReviewSpec
    status: V1SubjectAccessReviewStatus


class V1LimitRangeList(ResourceItem):
    items: List[V1LimitRange]
    metadata: V1ListMeta


class V1LimitRangeItem(ResourceValue):
    default: Dict[str, str]
    defaultRequest: Dict[str, str]
    max: Dict[str, str]
    maxLimitRequestRatio: Dict[str, str]
    min: Dict[str, str]
    type: str


class V1LimitRangeSpec(ResourceValue):
    limits: List[V1LimitRangeItem]


class V1LimitRange(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1LimitRangeSpec


class V1LeaseList(ResourceItem):
    items: List[V1Lease]
    metadata: V1ListMeta


class V1LeaseSpec(ResourceValue):
    acquireTime: datetime
    holderIdentity: str
    leaseDurationSeconds: int
    leaseTransitions: int
    renewTime: datetime


class V1Lease(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1LeaseSpec


class V1JobList(ResourceItem):
    items: List[V1Job]
    metadata: V1ListMeta


class V1UncountedTerminatedPods(ResourceValue):
    failed: List[str]
    succeeded: List[str]


class V1JobCondition(ResourceValue):
    lastProbeTime: datetime
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1JobStatus(ResourceValue):
    active: int
    completedIndexes: str
    completionTime: datetime
    conditions: List[V1JobCondition]
    failed: int
    ready: int
    startTime: datetime
    succeeded: int
    uncountedTerminatedPods: V1UncountedTerminatedPods


class V1Job(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1JobSpec
    status: V1JobStatus


class V1IngressList(ResourceItem):
    items: List[V1Ingress]
    metadata: V1ListMeta


class V1IngressClassList(ResourceItem):
    items: List[V1IngressClass]
    metadata: V1ListMeta


class V1IngressClassParametersReference(ResourceValue):
    apiGroup: str
    kind: str
    name: str
    namespace: str
    scope: str


class V1IngressClassSpec(ResourceValue):
    controller: str
    parameters: V1IngressClassParametersReference


class V1IngressClass(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1IngressClassSpec


class V1IngressPortStatus(ResourceValue):
    error: str
    port: int
    protocol: str


class V1IngressLoadBalancerIngress(ResourceValue):
    hostname: str
    ip: str
    ports: List[V1IngressPortStatus]


class V1IngressLoadBalancerStatus(ResourceValue):
    ingress: List[V1IngressLoadBalancerIngress]


class V1IngressStatus(ResourceValue):
    loadBalancer: V1IngressLoadBalancerStatus


class V1IngressTLS(ResourceValue):
    hosts: List[str]
    secretName: str


class V1HTTPIngressPath(ResourceValue):
    backend: V1IngressBackend
    path: str
    pathType: str


class V1HTTPIngressRuleValue(ResourceValue):
    paths: List[V1HTTPIngressPath]


class V1IngressRule(ResourceValue):
    host: str
    http: V1HTTPIngressRuleValue


class V1ServiceBackendPort(ResourceValue):
    name: str
    number: int


class V1IngressServiceBackend(ResourceValue):
    name: str
    port: V1ServiceBackendPort


class V1IngressBackend(ResourceValue):
    resource: V1TypedLocalObjectReference
    service: V1IngressServiceBackend


class V1IngressSpec(ResourceValue):
    defaultBackend: V1IngressBackend
    ingressClassName: str
    rules: List[V1IngressRule]
    tls: List[V1IngressTLS]


class V1HorizontalPodAutoscalerList(ResourceItem):
    items: List[V1HorizontalPodAutoscaler]
    metadata: V1ListMeta


class V1HorizontalPodAutoscalerStatus(ResourceValue):
    currentCPUUtilizationPercentage: int
    currentReplicas: int
    desiredReplicas: int
    lastScaleTime: datetime
    observedGeneration: int


class V1HorizontalPodAutoscalerSpec(ResourceValue):
    maxReplicas: int
    minReplicas: int
    scaleTargetRef: V1CrossVersionObjectReference
    targetCPUUtilizationPercentage: int


class V1HorizontalPodAutoscaler(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1HorizontalPodAutoscalerSpec
    status: V1HorizontalPodAutoscalerStatus


class V1Eviction(ResourceItem):
    deleteOptions: V1DeleteOptions
    metadata: V1ObjectMeta


class V1EndpointsList(ResourceItem):
    items: List[V1Endpoints]
    metadata: V1ListMeta


class CoreV1EndpointPort(ResourceValue):
    appProtocol: str
    name: str
    port: int
    protocol: str


class V1EndpointAddress(ResourceValue):
    hostname: str
    ip: str
    nodeName: str
    targetRef: V1ObjectReference


class V1EndpointSubset(ResourceValue):
    addresses: List[V1EndpointAddress]
    notReadyAddresses: List[V1EndpointAddress]
    ports: List[CoreV1EndpointPort]


class V1Endpoints(ResourceItem):
    metadata: V1ObjectMeta
    subsets: List[V1EndpointSubset]


class V1EndpointSliceList(ResourceItem):
    items: List[V1EndpointSlice]
    metadata: V1ListMeta


class DiscoveryV1EndpointPort(ResourceValue):
    appProtocol: str
    name: str
    port: int
    protocol: str


class V1ForZone(ResourceValue):
    name: str


class V1EndpointHints(ResourceValue):
    forZones: List[V1ForZone]


class V1EndpointConditions(ResourceValue):
    ready: bool
    serving: bool
    terminating: bool


class V1Endpoint(ResourceValue):
    addresses: List[str]
    conditions: V1EndpointConditions
    deprecatedTopology: Dict[str, str]
    hints: V1EndpointHints
    hostname: str
    nodeName: str
    targetRef: V1ObjectReference
    zone: str


class V1EndpointSlice(ResourceItem):
    addressType: str
    endpoints: List[V1Endpoint]
    metadata: V1ObjectMeta
    ports: List[DiscoveryV1EndpointPort]


class V1DeploymentList(ResourceItem):
    items: List[V1Deployment]
    metadata: V1ListMeta


class V1DeploymentCondition(ResourceValue):
    lastTransitionTime: datetime
    lastUpdateTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1DeploymentStatus(ResourceValue):
    availableReplicas: int
    collisionCount: int
    conditions: List[V1DeploymentCondition]
    observedGeneration: int
    readyReplicas: int
    replicas: int
    unavailableReplicas: int
    updatedReplicas: int


class V1RollingUpdateDeployment(ResourceValue):
    maxSurge: object
    maxUnavailable: object


class V1DeploymentStrategy(ResourceValue):
    rollingUpdate: V1RollingUpdateDeployment
    type: str


class V1DeploymentSpec(ResourceValue):
    minReadySeconds: int
    paused: bool
    progressDeadlineSeconds: int
    replicas: int
    revisionHistoryLimit: int
    selector: V1LabelSelector
    strategy: V1DeploymentStrategy
    template: V1PodTemplateSpec


class V1Deployment(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1DeploymentSpec
    status: V1DeploymentStatus


class V1Preconditions(ResourceValue):
    resourceVersion: str
    uid: str


class V1DeleteOptions(ResourceItem):
    dryRun: List[str]
    gracePeriodSeconds: int
    orphanDependents: bool
    preconditions: V1Preconditions
    propagationPolicy: str


class V1DaemonSetList(ResourceItem):
    items: List[V1DaemonSet]
    metadata: V1ListMeta


class V1DaemonSetCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1DaemonSetStatus(ResourceValue):
    collisionCount: int
    conditions: List[V1DaemonSetCondition]
    currentNumberScheduled: int
    desiredNumberScheduled: int
    numberAvailable: int
    numberMisscheduled: int
    numberReady: int
    numberUnavailable: int
    observedGeneration: int
    updatedNumberScheduled: int


class V1RollingUpdateDaemonSet(ResourceValue):
    maxSurge: object
    maxUnavailable: object


class V1DaemonSetUpdateStrategy(ResourceValue):
    rollingUpdate: V1RollingUpdateDaemonSet
    type: str


class V1DaemonSetSpec(ResourceValue):
    minReadySeconds: int
    revisionHistoryLimit: int
    selector: V1LabelSelector
    template: V1PodTemplateSpec
    updateStrategy: V1DaemonSetUpdateStrategy


class V1DaemonSet(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1DaemonSetSpec
    status: V1DaemonSetStatus


class V1CustomResourceDefinitionList(ResourceItem):
    items: List[V1CustomResourceDefinition]
    metadata: V1ListMeta


class V1CustomResourceDefinitionCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1CustomResourceDefinitionStatus(ResourceValue):
    acceptedNames: V1CustomResourceDefinitionNames
    conditions: List[V1CustomResourceDefinitionCondition]
    storedVersions: List[str]


class V1CustomResourceSubresourceScale(ResourceValue):
    labelSelectorPath: str
    specReplicasPath: str
    statusReplicasPath: str


class V1CustomResourceSubresources(ResourceValue):
    scale: V1CustomResourceSubresourceScale
    status: object


class V1ExternalDocumentation(ResourceValue):
    description: str
    url: str


class V1JSONSchemaProps(ResourceValue):
    additionalItems: object
    additionalProperties: object
    allOf: List[V1JSONSchemaProps]
    anyOf: List[V1JSONSchemaProps]
    default: object
    definitions: Dict[str, V1JSONSchemaProps]
    dependencies: Dict[str, object]
    description: str
    enum: List[object]
    example: object
    exclusiveMaximum: bool
    exclusiveMinimum: bool
    externalDocs: V1ExternalDocumentation
    format: str
    id: str
    items: object
    maxItems: int
    maxLength: int
    maxProperties: int
    maximum: float
    minItems: int
    minLength: int
    minProperties: int
    minimum: float
    multipleOf: float
    nullable: bool
    oneOf: List[V1JSONSchemaProps]
    pattern: str
    patternProperties: Dict[str, V1JSONSchemaProps]
    properties: Dict[str, V1JSONSchemaProps]
    required: List[str]
    title: str
    type: str
    uniqueItems: bool


class V1CustomResourceValidation(ResourceValue):
    openAPIV3Schema: V1JSONSchemaProps


class V1CustomResourceColumnDefinition(ResourceValue):
    description: str
    format: str
    jsonPath: str
    name: str
    priority: int
    type: str


class V1CustomResourceDefinitionVersion(ResourceValue):
    additionalPrinterColumns: List[V1CustomResourceColumnDefinition]
    deprecated: bool
    deprecationWarning: str
    name: str
    v1schema: V1CustomResourceValidation = Field(alias="schema")
    served: bool
    storage: bool
    subresources: V1CustomResourceSubresources


class V1CustomResourceDefinitionNames(ResourceValue):
    categories: List[str]
    kind: str
    listKind: str
    plural: str
    shortNames: List[str]
    singular: str


class ApiextensionsV1ServiceReference(ResourceValue):
    name: str
    namespace: str
    path: str
    port: int


class ApiextensionsV1WebhookClientConfig(ResourceValue):
    caBundle: str
    service: ApiextensionsV1ServiceReference
    url: str


class V1WebhookConversion(ResourceValue):
    clientConfig: ApiextensionsV1WebhookClientConfig
    conversionReviewVersions: List[str]


class V1CustomResourceConversion(ResourceValue):
    strategy: str
    webhook: V1WebhookConversion


class V1CustomResourceDefinitionSpec(ResourceValue):
    conversion: V1CustomResourceConversion
    group: str
    names: V1CustomResourceDefinitionNames
    preserveUnknownFields: bool
    scope: str
    versions: List[V1CustomResourceDefinitionVersion]


class V1CustomResourceDefinition(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1CustomResourceDefinitionSpec
    status: V1CustomResourceDefinitionStatus


class V1CrossVersionObjectReference(ResourceItem):
    name: str


class V1CronJobList(ResourceItem):
    items: List[V1CronJob]
    metadata: V1ListMeta


class V1CronJobStatus(ResourceValue):
    active: List[V1ObjectReference]
    lastScheduleTime: datetime
    lastSuccessfulTime: datetime


class V1VsphereVirtualDiskVolumeSource(ResourceValue):
    fsType: str
    storagePolicyID: str
    storagePolicyName: str
    volumePath: str


class V1StorageOSVolumeSource(ResourceValue):
    fsType: str
    readOnly: bool
    secretRef: V1LocalObjectReference
    volumeName: str
    volumeNamespace: str


class V1SecretVolumeSource(ResourceValue):
    defaultMode: int
    items: List[V1KeyToPath]
    optional: bool
    secretName: str


class V1ScaleIOVolumeSource(ResourceValue):
    fsType: str
    gateway: str
    protectionDomain: str
    readOnly: bool
    secretRef: V1LocalObjectReference
    sslEnabled: bool
    storageMode: str
    storagePool: str
    system: str
    volumeName: str


class V1RBDVolumeSource(ResourceValue):
    fsType: str
    image: str
    keyring: str
    monitors: List[str]
    pool: str
    readOnly: bool
    secretRef: V1LocalObjectReference
    user: str


class V1QuobyteVolumeSource(ResourceValue):
    group: str
    readOnly: bool
    registry: str
    tenant: str
    user: str
    volume: str


class V1ServiceAccountTokenProjection(ResourceValue):
    audience: str
    expirationSeconds: int
    path: str


class V1SecretProjection(ResourceValue):
    items: List[V1KeyToPath]
    name: str
    optional: bool


class V1DownwardAPIProjection(ResourceValue):
    items: List[V1DownwardAPIVolumeFile]


class V1ConfigMapProjection(ResourceValue):
    items: List[V1KeyToPath]
    name: str
    optional: bool


class V1VolumeProjection(ResourceValue):
    configMap: V1ConfigMapProjection
    downwardAPI: V1DownwardAPIProjection
    secret: V1SecretProjection
    serviceAccountToken: V1ServiceAccountTokenProjection


class V1ProjectedVolumeSource(ResourceValue):
    defaultMode: int
    sources: List[V1VolumeProjection]


class V1PortworxVolumeSource(ResourceValue):
    fsType: str
    readOnly: bool
    volumeID: str


class V1PhotonPersistentDiskVolumeSource(ResourceValue):
    fsType: str
    pdID: str


class V1PersistentVolumeClaimVolumeSource(ResourceValue):
    claimName: str
    readOnly: bool


class V1NFSVolumeSource(ResourceValue):
    path: str
    readOnly: bool
    server: str


class V1ISCSIVolumeSource(ResourceValue):
    chapAuthDiscovery: bool
    chapAuthSession: bool
    fsType: str
    initiatorName: str
    iqn: str
    iscsiInterface: str
    lun: int
    portals: List[str]
    readOnly: bool
    secretRef: V1LocalObjectReference
    targetPortal: str


class V1HostPathVolumeSource(ResourceValue):
    path: str
    type: str


class V1GlusterfsVolumeSource(ResourceValue):
    endpoints: str
    path: str
    readOnly: bool


class V1GitRepoVolumeSource(ResourceValue):
    directory: str
    repository: str
    revision: str


class V1GCEPersistentDiskVolumeSource(ResourceValue):
    fsType: str
    partition: int
    pdName: str
    readOnly: bool


class V1FlockerVolumeSource(ResourceValue):
    datasetName: str
    datasetUUID: str


class V1FlexVolumeSource(ResourceValue):
    driver: str
    fsType: str
    options: Dict[str, str]
    readOnly: bool
    secretRef: V1LocalObjectReference


class V1FCVolumeSource(ResourceValue):
    fsType: str
    lun: int
    readOnly: bool
    targetWWNs: List[str]
    wwids: List[str]


class V1TypedObjectReference(ResourceValue):
    apiGroup: str
    kind: str
    name: str
    namespace: str


class V1TypedLocalObjectReference(ResourceValue):
    apiGroup: str
    kind: str
    name: str


class V1PersistentVolumeClaimSpec(ResourceValue):
    accessModes: List[str]
    dataSource: V1TypedLocalObjectReference
    dataSourceRef: V1TypedObjectReference
    resources: V1ResourceRequirements
    selector: V1LabelSelector
    storageClassName: str
    volumeMode: str
    volumeName: str


class V1PersistentVolumeClaimTemplate(ResourceValue):
    metadata: V1ObjectMeta
    spec: V1PersistentVolumeClaimSpec


class V1EphemeralVolumeSource(ResourceValue):
    volumeClaimTemplate: V1PersistentVolumeClaimTemplate


class V1EmptyDirVolumeSource(ResourceValue):
    medium: str
    sizeLimit: str


class V1DownwardAPIVolumeFile(ResourceValue):
    fieldRef: V1ObjectFieldSelector
    mode: int
    path: str
    resourceFieldRef: V1ResourceFieldSelector


class V1DownwardAPIVolumeSource(ResourceValue):
    defaultMode: int
    items: List[V1DownwardAPIVolumeFile]


class V1CSIVolumeSource(ResourceValue):
    driver: str
    fsType: str
    nodePublishSecretRef: V1LocalObjectReference
    readOnly: bool
    volumeAttributes: Dict[str, str]


class V1KeyToPath(ResourceValue):
    key: str
    mode: int
    path: str


class V1ConfigMapVolumeSource(ResourceValue):
    defaultMode: int
    items: List[V1KeyToPath]
    name: str
    optional: bool


class V1CinderVolumeSource(ResourceValue):
    fsType: str
    readOnly: bool
    secretRef: V1LocalObjectReference
    volumeID: str


class V1CephFSVolumeSource(ResourceValue):
    monitors: List[str]
    path: str
    readOnly: bool
    secretFile: str
    secretRef: V1LocalObjectReference
    user: str


class V1AzureFileVolumeSource(ResourceValue):
    readOnly: bool
    secretName: str
    shareName: str


class V1AzureDiskVolumeSource(ResourceValue):
    cachingMode: str
    diskName: str
    diskURI: str
    fsType: str
    kind: str
    readOnly: bool


class V1AWSElasticBlockStoreVolumeSource(ResourceValue):
    fsType: str
    partition: int
    readOnly: bool
    volumeID: str


class V1Volume(ResourceValue):
    awsElasticBlockStore: V1AWSElasticBlockStoreVolumeSource
    azureDisk: V1AzureDiskVolumeSource
    azureFile: V1AzureFileVolumeSource
    cephfs: V1CephFSVolumeSource
    cinder: V1CinderVolumeSource
    configMap: V1ConfigMapVolumeSource
    csi: V1CSIVolumeSource
    downwardAPI: V1DownwardAPIVolumeSource
    emptyDir: V1EmptyDirVolumeSource
    ephemeral: V1EphemeralVolumeSource
    fc: V1FCVolumeSource
    flexVolume: V1FlexVolumeSource
    flocker: V1FlockerVolumeSource
    gcePersistentDisk: V1GCEPersistentDiskVolumeSource
    gitRepo: V1GitRepoVolumeSource
    glusterfs: V1GlusterfsVolumeSource
    hostPath: V1HostPathVolumeSource
    iscsi: V1ISCSIVolumeSource
    name: str
    nfs: V1NFSVolumeSource
    persistentVolumeClaim: V1PersistentVolumeClaimVolumeSource
    photonPersistentDisk: V1PhotonPersistentDiskVolumeSource
    portworxVolume: V1PortworxVolumeSource
    projected: V1ProjectedVolumeSource
    quobyte: V1QuobyteVolumeSource
    rbd: V1RBDVolumeSource
    scaleIO: V1ScaleIOVolumeSource
    secret: V1SecretVolumeSource
    storageos: V1StorageOSVolumeSource
    vsphereVolume: V1VsphereVirtualDiskVolumeSource


class V1TopologySpreadConstraint(ResourceValue):
    labelSelector: V1LabelSelector
    matchLabelKeys: List[str]
    maxSkew: int
    minDomains: int
    nodeAffinityPolicy: str
    nodeTaintsPolicy: str
    topologyKey: str
    whenUnsatisfiable: str


class V1Toleration(ResourceValue):
    effect: str
    key: str
    operator: str
    tolerationSeconds: int
    value: str


class V1Sysctl(ResourceValue):
    name: str
    value: str


class V1PodSecurityContext(ResourceValue):
    fsGroup: int
    fsGroupChangePolicy: str
    runAsGroup: int
    runAsNonRoot: bool
    runAsUser: int
    seLinuxOptions: V1SELinuxOptions
    seccompProfile: V1SeccompProfile
    supplementalGroups: List[int]
    sysctls: List[V1Sysctl]
    windowsOptions: V1WindowsSecurityContextOptions


class V1PodSchedulingGate(ResourceValue):
    name: str


class V1ClaimSource(ResourceValue):
    resourceClaimName: str
    resourceClaimTemplateName: str


class V1PodResourceClaim(ResourceValue):
    name: str
    source: V1ClaimSource


class V1PodReadinessGate(ResourceValue):
    conditionType: str


class V1PodOS(ResourceValue):
    name: str


class V1LocalObjectReference(ResourceValue):
    name: str


class V1HostAlias(ResourceValue):
    hostnames: List[str]
    ip: str


class V1EphemeralContainer(ResourceValue):
    args: List[str]
    command: List[str]
    env: List[V1EnvVar]
    envFrom: List[V1EnvFromSource]
    image: str
    imagePullPolicy: str
    lifecycle: V1Lifecycle
    livenessProbe: V1Probe
    name: str
    ports: List[V1ContainerPort]
    readinessProbe: V1Probe
    resources: V1ResourceRequirements
    securityContext: V1SecurityContext
    startupProbe: V1Probe
    stdin: bool
    stdinOnce: bool
    targetContainerName: str
    terminationMessagePath: str
    terminationMessagePolicy: str
    tty: bool
    volumeDevices: List[V1VolumeDevice]
    volumeMounts: List[V1VolumeMount]
    workingDir: str


class V1PodDNSConfigOption(ResourceValue):
    name: str
    value: str


class V1PodDNSConfig(ResourceValue):
    nameservers: List[str]
    options: List[V1PodDNSConfigOption]
    searches: List[str]


class V1VolumeMount(ResourceValue):
    mountPath: str
    mountPropagation: str
    name: str
    readOnly: bool
    subPath: str
    subPathExpr: str


class V1VolumeDevice(ResourceValue):
    devicePath: str
    name: str


class V1WindowsSecurityContextOptions(ResourceValue):
    gmsaCredentialSpec: str
    gmsaCredentialSpecName: str
    hostProcess: bool
    runAsUserName: str


class V1SeccompProfile(ResourceValue):
    localhostProfile: str
    type: str


class V1SELinuxOptions(ResourceValue):
    level: str
    role: str
    type: str
    user: str


class V1Capabilities(ResourceValue):
    add: List[str]
    drop: List[str]


class V1SecurityContext(ResourceValue):
    allowPrivilegeEscalation: bool
    capabilities: V1Capabilities
    privileged: bool
    procMount: str
    readOnlyRootFilesystem: bool
    runAsGroup: int
    runAsNonRoot: bool
    runAsUser: int
    seLinuxOptions: V1SELinuxOptions
    seccompProfile: V1SeccompProfile
    windowsOptions: V1WindowsSecurityContextOptions


class V1ResourceClaim(ResourceValue):
    name: str


class V1ResourceRequirements(ResourceValue):
    claims: List[V1ResourceClaim]
    limits: Dict[str, str]
    requests: Dict[str, str]


class V1ContainerPort(ResourceValue):
    containerPort: int
    hostIP: str
    hostPort: int
    name: str
    protocol: str


class V1GRPCAction(ResourceValue):
    port: int
    service: str


class V1Probe(ResourceValue):
    exec: V1ExecAction
    failureThreshold: int
    grpc: V1GRPCAction
    httpGet: V1HTTPGetAction
    initialDelaySeconds: int
    periodSeconds: int
    successThreshold: int
    tcpSocket: V1TCPSocketAction
    terminationGracePeriodSeconds: int
    timeoutSeconds: int


class V1TCPSocketAction(ResourceValue):
    host: str
    port: object


class V1HTTPHeader(ResourceValue):
    name: str
    value: str


class V1HTTPGetAction(ResourceValue):
    host: str
    httpHeaders: List[V1HTTPHeader]
    path: str
    port: object
    scheme: str


class V1ExecAction(ResourceValue):
    command: List[str]


class V1LifecycleHandler(ResourceValue):
    exec: V1ExecAction
    httpGet: V1HTTPGetAction
    tcpSocket: V1TCPSocketAction


class V1Lifecycle(ResourceValue):
    postStart: V1LifecycleHandler
    preStop: V1LifecycleHandler


class V1SecretEnvSource(ResourceValue):
    name: str
    optional: bool


class V1ConfigMapEnvSource(ResourceValue):
    name: str
    optional: bool


class V1EnvFromSource(ResourceValue):
    configMapRef: V1ConfigMapEnvSource
    prefix: str
    secretRef: V1SecretEnvSource


class V1SecretKeySelector(ResourceValue):
    key: str
    name: str
    optional: bool


class V1ResourceFieldSelector(ResourceValue):
    containerName: str
    divisor: str
    resource: str


class V1ObjectFieldSelector(ResourceValue):
    apiVersion: str
    fieldPath: str


class V1ConfigMapKeySelector(ResourceValue):
    key: str
    name: str
    optional: bool


class V1EnvVarSource(ResourceValue):
    configMapKeyRef: V1ConfigMapKeySelector
    fieldRef: V1ObjectFieldSelector
    resourceFieldRef: V1ResourceFieldSelector
    secretKeyRef: V1SecretKeySelector


class V1EnvVar(ResourceValue):
    name: str
    value: str
    valueFrom: V1EnvVarSource


class V1Container(ResourceValue):
    args: List[str]
    command: List[str]
    env: List[V1EnvVar]
    envFrom: List[V1EnvFromSource]
    image: str
    imagePullPolicy: str
    lifecycle: V1Lifecycle
    livenessProbe: V1Probe
    name: str
    ports: List[V1ContainerPort]
    readinessProbe: V1Probe
    resources: V1ResourceRequirements
    securityContext: V1SecurityContext
    startupProbe: V1Probe
    stdin: bool
    stdinOnce: bool
    terminationMessagePath: str
    terminationMessagePolicy: str
    tty: bool
    volumeDevices: List[V1VolumeDevice]
    volumeMounts: List[V1VolumeMount]
    workingDir: str


class V1PodAntiAffinity(ResourceValue):
    preferredDuringSchedulingIgnoredDuringExecution: List[V1WeightedPodAffinityTerm]
    requiredDuringSchedulingIgnoredDuringExecution: List[V1PodAffinityTerm]


class V1PodAffinityTerm(ResourceValue):
    labelSelector: V1LabelSelector
    namespaceSelector: V1LabelSelector
    namespaces: List[str]
    topologyKey: str


class V1WeightedPodAffinityTerm(ResourceValue):
    podAffinityTerm: V1PodAffinityTerm
    weight: int


class V1PodAffinity(ResourceValue):
    preferredDuringSchedulingIgnoredDuringExecution: List[V1WeightedPodAffinityTerm]
    requiredDuringSchedulingIgnoredDuringExecution: List[V1PodAffinityTerm]


class V1NodeSelector(ResourceValue):
    nodeSelectorTerms: List[V1NodeSelectorTerm]


class V1NodeSelectorRequirement(ResourceValue):
    key: str
    operator: str
    values: List[str]


class V1NodeSelectorTerm(ResourceValue):
    matchExpressions: List[V1NodeSelectorRequirement]
    matchFields: List[V1NodeSelectorRequirement]


class V1PreferredSchedulingTerm(ResourceValue):
    preference: V1NodeSelectorTerm
    weight: int


class V1NodeAffinity(ResourceValue):
    preferredDuringSchedulingIgnoredDuringExecution: List[V1PreferredSchedulingTerm]
    requiredDuringSchedulingIgnoredDuringExecution: V1NodeSelector


class V1Affinity(ResourceValue):
    nodeAffinity: V1NodeAffinity
    podAffinity: V1PodAffinity
    podAntiAffinity: V1PodAntiAffinity


class V1PodSpec(ResourceValue):
    activeDeadlineSeconds: int
    affinity: V1Affinity
    automountServiceAccountToken: bool
    containers: List[V1Container]
    dnsConfig: V1PodDNSConfig
    dnsPolicy: str
    enableServiceLinks: bool
    ephemeralContainers: List[V1EphemeralContainer]
    hostAliases: List[V1HostAlias]
    hostIPC: bool
    hostNetwork: bool
    hostPID: bool
    hostUsers: bool
    hostname: str
    imagePullSecrets: List[V1LocalObjectReference]
    initContainers: List[V1Container]
    nodeName: str
    nodeSelector: Dict[str, str]
    os: V1PodOS
    overhead: Dict[str, str]
    preemptionPolicy: str
    priority: int
    priorityClassName: str
    readinessGates: List[V1PodReadinessGate]
    resourceClaims: List[V1PodResourceClaim]
    restartPolicy: str
    runtimeClassName: str
    schedulerName: str
    schedulingGates: List[V1PodSchedulingGate]
    securityContext: V1PodSecurityContext
    serviceAccount: str
    serviceAccountName: str
    setHostnameAsFQDN: bool
    shareProcessNamespace: bool
    subdomain: str
    terminationGracePeriodSeconds: int
    tolerations: List[V1Toleration]
    topologySpreadConstraints: List[V1TopologySpreadConstraint]
    volumes: List[V1Volume]


class V1PodTemplateSpec(ResourceValue):
    metadata: V1ObjectMeta
    spec: V1PodSpec


class V1PodFailurePolicyOnPodConditionsPattern(ResourceValue):
    status: str
    type: str


class V1PodFailurePolicyOnExitCodesRequirement(ResourceValue):
    containerName: str
    operator: str
    values: List[int]


class V1PodFailurePolicyRule(ResourceValue):
    action: str
    onExitCodes: V1PodFailurePolicyOnExitCodesRequirement
    onPodConditions: List[V1PodFailurePolicyOnPodConditionsPattern]


class V1PodFailurePolicy(ResourceValue):
    rules: List[V1PodFailurePolicyRule]


class V1JobSpec(ResourceValue):
    activeDeadlineSeconds: int
    backoffLimit: int
    completionMode: str
    completions: int
    manualSelector: bool
    parallelism: int
    podFailurePolicy: V1PodFailurePolicy
    selector: V1LabelSelector
    suspend: bool
    template: V1PodTemplateSpec
    ttlSecondsAfterFinished: int


class V1JobTemplateSpec(ResourceValue):
    metadata: V1ObjectMeta
    spec: V1JobSpec


class V1CronJobSpec(ResourceValue):
    concurrencyPolicy: str
    failedJobsHistoryLimit: int
    jobTemplate: V1JobTemplateSpec
    schedule: str
    startingDeadlineSeconds: int
    successfulJobsHistoryLimit: int
    suspend: bool
    timeZone: str


class V1CronJob(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1CronJobSpec
    status: V1CronJobStatus


class V1ControllerRevisionList(ResourceItem):
    items: List[V1ControllerRevision]
    metadata: V1ListMeta


class V1ControllerRevision(ResourceItem):
    data: object
    metadata: V1ObjectMeta
    revision: int


class V1ConfigMapList(ResourceItem):
    items: List[V1ConfigMap]
    metadata: V1ListMeta


class V1ComponentStatusList(ResourceItem):
    items: List[V1ComponentStatus]
    metadata: V1ListMeta


class V1ComponentCondition(ResourceValue):
    error: str
    message: str
    status: str
    type: str


class V1ComponentStatus(ResourceItem):
    conditions: List[V1ComponentCondition]
    metadata: V1ObjectMeta


class V1ClusterRoleList(ResourceItem):
    items: List[V1ClusterRole]
    metadata: V1ListMeta


class V1ClusterRoleBindingList(ResourceItem):
    items: List[V1ClusterRoleBinding]
    metadata: V1ListMeta


class V1Subject(ResourceValue):
    apiGroup: str
    kind: str
    name: str
    namespace: str


class V1RoleRef(ResourceValue):
    apiGroup: str
    kind: str
    name: str


class V1ClusterRoleBinding(ResourceItem):
    metadata: V1ObjectMeta
    roleRef: V1RoleRef
    subjects: List[V1Subject]


class V1PolicyRule(ResourceValue):
    apiGroups: List[str]
    nonResourceURLs: List[str]
    resourceNames: List[str]
    resources: List[str]
    verbs: List[str]


class V1AggregationRule(ResourceValue):
    clusterRoleSelectors: List[V1LabelSelector]


class V1ClusterRole(ResourceItem):
    aggregationRule: V1AggregationRule
    metadata: V1ObjectMeta
    rules: List[V1PolicyRule]


class V1CertificateSigningRequestList(ResourceItem):
    items: List[V1CertificateSigningRequest]
    metadata: V1ListMeta


class V1CertificateSigningRequestCondition(ResourceValue):
    lastTransitionTime: datetime
    lastUpdateTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1CertificateSigningRequestStatus(ResourceValue):
    certificate: str
    conditions: List[V1CertificateSigningRequestCondition]


class V1CertificateSigningRequestSpec(ResourceValue):
    expirationSeconds: int
    extra: Dict[str, List[str]]
    groups: List[str]
    request: str
    signerName: str
    uid: str
    usages: List[str]
    username: str


class V1CertificateSigningRequest(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1CertificateSigningRequestSpec
    status: V1CertificateSigningRequestStatus


class V1CSIStorageCapacityList(ResourceItem):
    items: List[V1CSIStorageCapacity]
    metadata: V1ListMeta


class V1LabelSelectorRequirement(ResourceValue):
    key: str
    operator: str
    values: List[str]


class V1LabelSelector(ResourceValue):
    matchExpressions: List[V1LabelSelectorRequirement]
    matchLabels: Dict[str, str]


class V1CSIStorageCapacity(ResourceItem):
    capacity: str
    maximumVolumeSize: str
    metadata: V1ObjectMeta
    nodeTopology: V1LabelSelector
    storageClassName: str


class V1CSINodeList(ResourceItem):
    items: List[V1CSINode]
    metadata: V1ListMeta


class V1VolumeNodeResources(ResourceValue):
    count: int


class V1CSINodeDriver(ResourceValue):
    allocatable: V1VolumeNodeResources
    name: str
    nodeID: str
    topologyKeys: List[str]


class V1CSINodeSpec(ResourceValue):
    drivers: List[V1CSINodeDriver]


class V1CSINode(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1CSINodeSpec


class V1CSIDriverList(ResourceItem):
    items: List[V1CSIDriver]
    metadata: V1ListMeta


class StorageV1TokenRequest(ResourceValue):
    audience: str
    expirationSeconds: int


class V1CSIDriverSpec(ResourceValue):
    attachRequired: bool
    fsGroupPolicy: str
    podInfoOnMount: bool
    requiresRepublish: bool
    seLinuxMount: bool
    storageCapacity: bool
    tokenRequests: List[StorageV1TokenRequest]
    volumeLifecycleModes: List[str]


class V1CSIDriver(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1CSIDriverSpec


class V1Binding(ResourceItem):
    metadata: V1ObjectMeta
    target: V1ObjectReference


class V1APIVersions(ResourceItem):
    serverAddressByClientCIDRs: List[V1ServerAddressByClientCIDR]
    versions: List[str]


class V1APIServiceList(ResourceItem):
    items: List[V1APIService]
    metadata: V1ListMeta


class V1APIServiceCondition(ResourceValue):
    lastTransitionTime: datetime
    message: str
    reason: str
    status: str
    type: str


class V1APIServiceStatus(ResourceValue):
    conditions: List[V1APIServiceCondition]


class ApiregistrationV1ServiceReference(ResourceValue):
    name: str
    namespace: str
    port: int


class V1APIServiceSpec(ResourceValue):
    caBundle: str
    group: str
    groupPriorityMinimum: int
    insecureSkipTLSVerify: bool
    service: ApiregistrationV1ServiceReference
    version: str
    versionPriority: int


class V1APIService(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1APIServiceSpec
    status: V1APIServiceStatus


class V1APIResource(ResourceValue):
    categories: List[str]
    group: str
    kind: str
    name: str
    namespaced: bool
    shortNames: List[str]
    singularName: str
    storageVersionHash: str
    verbs: List[str]
    version: str


class V1APIResourceList(ResourceItem):
    groupVersion: str
    resources: List[V1APIResource]


class V1APIGroupList(ResourceItem):
    groups: List[V1APIGroup]


class V1ServerAddressByClientCIDR(ResourceValue):
    clientCIDR: str
    serverAddress: str


class V1GroupVersionForDiscovery(ResourceValue):
    groupVersion: str
    version: str


class V1APIGroup(ResourceItem):
    name: str
    preferredVersion: V1GroupVersionForDiscovery
    serverAddressByClientCIDRs: List[V1ServerAddressByClientCIDR]
    versions: List[V1GroupVersionForDiscovery]


class EventsV1EventList(ResourceItem):
    items: List[EventsV1Event]
    metadata: V1ListMeta


class EventsV1EventSeries(ResourceValue):
    count: int
    lastObservedTime: datetime


class EventsV1Event(ResourceItem):
    action: str
    deprecatedCount: int
    deprecatedFirstTimestamp: datetime
    deprecatedLastTimestamp: datetime
    deprecatedSource: V1EventSource
    eventTime: datetime
    metadata: V1ObjectMeta
    note: str
    reason: str
    regarding: V1ObjectReference
    related: V1ObjectReference
    reportingController: str
    reportingInstance: str
    series: EventsV1EventSeries
    type: str


class CoreV1EventList(ResourceItem):
    items: List[CoreV1Event]
    metadata: V1ListMeta


class V1EventSource(ResourceValue):
    component: str
    host: str


class CoreV1EventSeries(ResourceValue):
    count: int
    lastObservedTime: datetime


class V1ObjectReference(ResourceItem):
    fieldPath: str
    name: str
    namespace: str
    resourceVersion: str
    uid: str


class CoreV1Event(ResourceItem):
    action: str
    count: int
    eventTime: datetime
    firstTimestamp: datetime
    involvedObject: V1ObjectReference
    lastTimestamp: datetime
    message: str
    metadata: V1ObjectMeta
    reason: str
    related: V1ObjectReference
    reportingComponent: str
    reportingInstance: str
    series: CoreV1EventSeries
    source: V1EventSource
    type: str


class V1TokenRequestStatus(ResourceValue):
    expirationTimestamp: datetime
    token: str


class V1BoundObjectReference(ResourceItem):
    name: str
    uid: str


class V1TokenRequestSpec(ResourceValue):
    audiences: List[str]
    boundObjectRef: V1BoundObjectReference
    expirationSeconds: int


class AuthenticationV1TokenRequest(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1TokenRequestSpec
    status: V1TokenRequestStatus


mapping = {
    "TokenRequest": {
        "v1": AuthenticationV1TokenRequest,
    },
    "OwnerReference": {
        "v1": V1OwnerReference,
    },
    "BoundObjectReference": {
        "v1": V1BoundObjectReference,
    },
    "Event": {
        "v1": EventsV1Event,
    },
    "ObjectReference": {
        "v1": V1ObjectReference,
    },
    "EventList": {
        "v1": EventsV1EventList,
    },
    "APIGroup": {
        "v1": V1APIGroup,
    },
    "APIGroupList": {
        "v1": V1APIGroupList,
    },
    "APIResourceList": {
        "v1": V1APIResourceList,
    },
    "APIResource": {
        "v1": V1APIResource,
    },
    "APIService": {
        "v1": V1APIService,
    },
    "APIServiceList": {
        "v1": V1APIServiceList,
    },
    "APIVersions": {
        "v1": V1APIVersions,
    },
    "Binding": {
        "v1": V1Binding,
    },
    "CSIDriver": {
        "v1": V1CSIDriver,
    },
    "CSIDriverList": {
        "v1": V1CSIDriverList,
    },
    "CSINode": {
        "v1": V1CSINode,
    },
    "CSINodeList": {
        "v1": V1CSINodeList,
    },
    "CSIStorageCapacity": {
        "v1": V1CSIStorageCapacity,
        "v1beta1": V1beta1CSIStorageCapacity,
    },
    "CSIStorageCapacityList": {
        "v1": V1CSIStorageCapacityList,
        "v1beta1": V1beta1CSIStorageCapacityList,
    },
    "CertificateSigningRequest": {
        "v1": V1CertificateSigningRequest,
    },
    "CertificateSigningRequestList": {
        "v1": V1CertificateSigningRequestList,
    },
    "ClusterRole": {
        "v1": V1ClusterRole,
    },
    "ClusterRoleBinding": {
        "v1": V1ClusterRoleBinding,
    },
    "RoleRef": {
        "v1": V1RoleRef,
    },
    "Subject": {
        "v1": V1Subject,
        "v1beta2": V1beta2Subject,
        "v1beta3": V1beta3Subject,
    },
    "ClusterRoleBindingList": {
        "v1": V1ClusterRoleBindingList,
    },
    "ClusterRoleList": {
        "v1": V1ClusterRoleList,
    },
    "ComponentStatus": {
        "v1": V1ComponentStatus,
    },
    "ComponentStatusList": {
        "v1": V1ComponentStatusList,
    },
    "ConfigMap": {
        "v1": V1ConfigMap,
    },
    "ConfigMapList": {
        "v1": V1ConfigMapList,
    },
    "ControllerRevision": {
        "v1": V1ControllerRevision,
    },
    "ControllerRevisionList": {
        "v1": V1ControllerRevisionList,
    },
    "CronJob": {
        "v1": V1CronJob,
    },
    "AzureDiskVolumeSource": {
        "v1": V1AzureDiskVolumeSource,
    },
    "TypedLocalObjectReference": {
        "v1": V1TypedLocalObjectReference,
    },
    "TypedObjectReference": {
        "v1": V1TypedObjectReference,
    },
    "CronJobList": {
        "v1": V1CronJobList,
    },
    "CrossVersionObjectReference": {
        "v1": V1CrossVersionObjectReference,
        "v2": V2CrossVersionObjectReference,
    },
    "CustomResourceDefinition": {
        "v1": V1CustomResourceDefinition,
    },
    "CustomResourceDefinitionNames": {
        "v1": V1CustomResourceDefinitionNames,
    },
    "CustomResourceDefinitionList": {
        "v1": V1CustomResourceDefinitionList,
    },
    "DaemonSet": {
        "v1": V1DaemonSet,
    },
    "DaemonSetList": {
        "v1": V1DaemonSetList,
    },
    "DeleteOptions": {
        "v1": V1DeleteOptions,
    },
    "Deployment": {
        "v1": V1Deployment,
    },
    "DeploymentList": {
        "v1": V1DeploymentList,
    },
    "EndpointSlice": {
        "v1": V1EndpointSlice,
    },
    "EndpointSliceList": {
        "v1": V1EndpointSliceList,
    },
    "Endpoints": {
        "v1": V1Endpoints,
    },
    "EndpointsList": {
        "v1": V1EndpointsList,
    },
    "Eviction": {
        "v1": V1Eviction,
    },
    "HorizontalPodAutoscaler": {
        "v1": V1HorizontalPodAutoscaler,
        "v2": V2HorizontalPodAutoscaler,
    },
    "HorizontalPodAutoscalerList": {
        "v1": V1HorizontalPodAutoscalerList,
        "v2": V2HorizontalPodAutoscalerList,
    },
    "Ingress": {
        "v1": V1Ingress,
    },
    "IngressClass": {
        "v1": V1IngressClass,
    },
    "IngressClassParametersReference": {
        "v1": V1IngressClassParametersReference,
    },
    "IngressClassList": {
        "v1": V1IngressClassList,
    },
    "IngressList": {
        "v1": V1IngressList,
    },
    "Job": {
        "v1": V1Job,
    },
    "JobList": {
        "v1": V1JobList,
    },
    "Lease": {
        "v1": V1Lease,
    },
    "LeaseList": {
        "v1": V1LeaseList,
    },
    "LimitRange": {
        "v1": V1LimitRange,
    },
    "LimitRangeList": {
        "v1": V1LimitRangeList,
    },
    "LocalSubjectAccessReview": {
        "v1": V1LocalSubjectAccessReview,
    },
    "MutatingWebhookConfiguration": {
        "v1": V1MutatingWebhookConfiguration,
    },
    "MutatingWebhookConfigurationList": {
        "v1": V1MutatingWebhookConfigurationList,
    },
    "Namespace": {
        "v1": V1Namespace,
    },
    "NamespaceList": {
        "v1": V1NamespaceList,
    },
    "NetworkPolicy": {
        "v1": V1NetworkPolicy,
    },
    "NetworkPolicyList": {
        "v1": V1NetworkPolicyList,
    },
    "Node": {
        "v1": V1Node,
    },
    "NodeList": {
        "v1": V1NodeList,
    },
    "PersistentVolume": {
        "v1": V1PersistentVolume,
    },
    "PersistentVolumeClaim": {
        "v1": V1PersistentVolumeClaim,
    },
    "PersistentVolumeClaimList": {
        "v1": V1PersistentVolumeClaimList,
    },
    "PersistentVolumeList": {
        "v1": V1PersistentVolumeList,
    },
    "Pod": {
        "v1": V1Pod,
    },
    "PodDisruptionBudget": {
        "v1": V1PodDisruptionBudget,
    },
    "PodDisruptionBudgetList": {
        "v1": V1PodDisruptionBudgetList,
    },
    "PodList": {
        "v1": V1PodList,
    },
    "PodTemplate": {
        "v1": V1PodTemplate,
    },
    "PodTemplateList": {
        "v1": V1PodTemplateList,
    },
    "PriorityClass": {
        "v1": V1PriorityClass,
    },
    "PriorityClassList": {
        "v1": V1PriorityClassList,
    },
    "ReplicaSet": {
        "v1": V1ReplicaSet,
    },
    "ReplicaSetList": {
        "v1": V1ReplicaSetList,
    },
    "ReplicationController": {
        "v1": V1ReplicationController,
    },
    "ReplicationControllerList": {
        "v1": V1ReplicationControllerList,
    },
    "ResourceQuota": {
        "v1": V1ResourceQuota,
    },
    "ResourceQuotaList": {
        "v1": V1ResourceQuotaList,
    },
    "Role": {
        "v1": V1Role,
    },
    "RoleBinding": {
        "v1": V1RoleBinding,
    },
    "RoleBindingList": {
        "v1": V1RoleBindingList,
    },
    "RoleList": {
        "v1": V1RoleList,
    },
    "RuntimeClass": {
        "v1": V1RuntimeClass,
    },
    "RuntimeClassList": {
        "v1": V1RuntimeClassList,
    },
    "Scale": {
        "v1": V1Scale,
    },
    "Secret": {
        "v1": V1Secret,
    },
    "SecretList": {
        "v1": V1SecretList,
    },
    "SelfSubjectAccessReview": {
        "v1": V1SelfSubjectAccessReview,
    },
    "SelfSubjectRulesReview": {
        "v1": V1SelfSubjectRulesReview,
    },
    "Service": {
        "v1": V1Service,
    },
    "ServiceAccount": {
        "v1": V1ServiceAccount,
    },
    "ServiceAccountList": {
        "v1": V1ServiceAccountList,
    },
    "ServiceList": {
        "v1": V1ServiceList,
    },
    "StatefulSet": {
        "v1": V1StatefulSet,
    },
    "StatefulSetList": {
        "v1": V1StatefulSetList,
    },
    "Status": {
        "v1": V1Status,
    },
    "StatusDetails": {
        "v1": V1StatusDetails,
    },
    "StorageClass": {
        "v1": V1StorageClass,
    },
    "StorageClassList": {
        "v1": V1StorageClassList,
    },
    "SubjectAccessReview": {
        "v1": V1SubjectAccessReview,
    },
    "TokenReview": {
        "v1": V1TokenReview,
    },
    "ValidatingWebhookConfiguration": {
        "v1": V1ValidatingWebhookConfiguration,
    },
    "ValidatingWebhookConfigurationList": {
        "v1": V1ValidatingWebhookConfigurationList,
    },
    "VolumeAttachment": {
        "v1": V1VolumeAttachment,
    },
    "VolumeAttachmentList": {
        "v1": V1VolumeAttachmentList,
    },
    "ClusterCIDR": {
        "v1alpha1": V1alpha1ClusterCIDR,
    },
    "ClusterCIDRList": {
        "v1alpha1": V1alpha1ClusterCIDRList,
    },
    "ParamKind": {
        "v1alpha1": V1alpha1ParamKind,
    },
    "PodScheduling": {
        "v1alpha1": V1alpha1PodScheduling,
    },
    "PodSchedulingList": {
        "v1alpha1": V1alpha1PodSchedulingList,
    },
    "ResourceClaim": {
        "v1alpha1": V1alpha1ResourceClaim,
    },
    "ResourceClaimParametersReference": {
        "v1alpha1": V1alpha1ResourceClaimParametersReference,
    },
    "ResourceClaimList": {
        "v1alpha1": V1alpha1ResourceClaimList,
    },
    "ResourceClaimTemplate": {
        "v1alpha1": V1alpha1ResourceClaimTemplate,
    },
    "ResourceClaimTemplateList": {
        "v1alpha1": V1alpha1ResourceClaimTemplateList,
    },
    "ResourceClass": {
        "v1alpha1": V1alpha1ResourceClass,
    },
    "ResourceClassParametersReference": {
        "v1alpha1": V1alpha1ResourceClassParametersReference,
    },
    "ResourceClassList": {
        "v1alpha1": V1alpha1ResourceClassList,
    },
    "SelfSubjectReview": {
        "v1alpha1": V1alpha1SelfSubjectReview,
    },
    "StorageVersion": {
        "v1alpha1": V1alpha1StorageVersion,
    },
    "StorageVersionList": {
        "v1alpha1": V1alpha1StorageVersionList,
    },
    "ValidatingAdmissionPolicy": {
        "v1alpha1": V1alpha1ValidatingAdmissionPolicy,
    },
    "ValidatingAdmissionPolicyBinding": {
        "v1alpha1": V1alpha1ValidatingAdmissionPolicyBinding,
    },
    "ValidatingAdmissionPolicyBindingList": {
        "v1alpha1": V1alpha1ValidatingAdmissionPolicyBindingList,
    },
    "ValidatingAdmissionPolicyList": {
        "v1alpha1": V1alpha1ValidatingAdmissionPolicyList,
    },
    "FlowSchema": {
        "v1beta2": V1beta2FlowSchema,
        "v1beta3": V1beta3FlowSchema,
    },
    "FlowSchemaList": {
        "v1beta2": V1beta2FlowSchemaList,
        "v1beta3": V1beta3FlowSchemaList,
    },
    "PriorityLevelConfiguration": {
        "v1beta2": V1beta2PriorityLevelConfiguration,
        "v1beta3": V1beta3PriorityLevelConfiguration,
    },
    "PriorityLevelConfigurationList": {
        "v1beta2": V1beta2PriorityLevelConfigurationList,
        "v1beta3": V1beta3PriorityLevelConfigurationList,
    },
}


def update_models(locals: dict[str, Any]):
    models = [model for _, model in locals.items() if isinstance(model, type) and issubclass(model, pydantic.BaseModel)]
    for model in models:
        model.update_forward_refs(**locals)


update_models(locals())


def get_type(kind: str, version: str, default: Any = None):
    return mapping.get(kind, {}).get(version, default)
