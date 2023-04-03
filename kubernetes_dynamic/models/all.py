from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pydantic
from pydantic import Field

from .common import V1ListMeta as V1ListMeta
from .common import V1ManagedFieldsEntry as V1ManagedFieldsEntry
from .common import V1ObjectMeta, V1OwnerReference
from .configmap import V1ConfigMap
from .ingress import V1Ingress as V1Ingress
from .namespace import V1Namespace as V1Namespace
from .pod import V1Pod as V1Pod
from .resource_item import ResourceItem
from .resource_value import ResourceValue
from .secret import V1Secret as V1Secret
from .stateful_set import V1StatefulSet as V1StatefulSet


class V2HorizontalPodAutoscalerList(ResourceItem):
    items: List[V2HorizontalPodAutoscaler] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V2ResourceMetricStatus(ResourceValue):
    current: V2MetricValueStatus = Field(default_factory=lambda: V2MetricValueStatus())
    name: Optional[str] = None


class V2PodsMetricStatus(ResourceValue):
    current: V2MetricValueStatus = Field(default_factory=lambda: V2MetricValueStatus())
    metric: V2MetricIdentifier = Field(default_factory=lambda: V2MetricIdentifier())


class V2ObjectMetricStatus(ResourceValue):
    current: V2MetricValueStatus = Field(default_factory=lambda: V2MetricValueStatus())
    describedObject: V2CrossVersionObjectReference = Field(default_factory=lambda: V2CrossVersionObjectReference())
    metric: V2MetricIdentifier = Field(default_factory=lambda: V2MetricIdentifier())


class V2ExternalMetricStatus(ResourceValue):
    current: V2MetricValueStatus = Field(default_factory=lambda: V2MetricValueStatus())
    metric: V2MetricIdentifier = Field(default_factory=lambda: V2MetricIdentifier())


class V2MetricValueStatus(ResourceValue):
    averageUtilization: Optional[int] = None
    averageValue: Optional[str] = None
    value: Optional[str] = None


class V2ContainerResourceMetricStatus(ResourceValue):
    container: Optional[str] = None
    current: V2MetricValueStatus = Field(default_factory=lambda: V2MetricValueStatus())
    name: Optional[str] = None


class V2MetricStatus(ResourceValue):
    containerResource: V2ContainerResourceMetricStatus = Field(
        default_factory=lambda: V2ContainerResourceMetricStatus()
    )
    external: V2ExternalMetricStatus = Field(default_factory=lambda: V2ExternalMetricStatus())
    object: V2ObjectMetricStatus = Field(default_factory=lambda: V2ObjectMetricStatus())
    pods: V2PodsMetricStatus = Field(default_factory=lambda: V2PodsMetricStatus())
    resource: V2ResourceMetricStatus = Field(default_factory=lambda: V2ResourceMetricStatus())
    type: Optional[str] = None


class V2HorizontalPodAutoscalerCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V2HorizontalPodAutoscalerStatus(ResourceValue):
    conditions: List[V2HorizontalPodAutoscalerCondition] = Field(default_factory=list)
    currentMetrics: List[V2MetricStatus] = Field(default_factory=list)
    currentReplicas: Optional[int] = None
    desiredReplicas: Optional[int] = None
    lastScaleTime: Optional[datetime] = None
    observedGeneration: Optional[int] = None


class V2ResourceMetricSource(ResourceValue):
    name: Optional[str] = None
    target: V2MetricTarget = Field(default_factory=lambda: V2MetricTarget())


class V2PodsMetricSource(ResourceValue):
    metric: V2MetricIdentifier = Field(default_factory=lambda: V2MetricIdentifier())
    target: V2MetricTarget = Field(default_factory=lambda: V2MetricTarget())


class V2ObjectMetricSource(ResourceValue):
    describedObject: V2CrossVersionObjectReference = Field(default_factory=lambda: V2CrossVersionObjectReference())
    metric: V2MetricIdentifier = Field(default_factory=lambda: V2MetricIdentifier())
    target: V2MetricTarget = Field(default_factory=lambda: V2MetricTarget())


class V2MetricIdentifier(ResourceValue):
    name: Optional[str] = None
    selector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())


class V2ExternalMetricSource(ResourceValue):
    metric: V2MetricIdentifier = Field(default_factory=lambda: V2MetricIdentifier())
    target: V2MetricTarget = Field(default_factory=lambda: V2MetricTarget())


class V2MetricTarget(ResourceValue):
    averageUtilization: Optional[int] = None
    averageValue: Optional[str] = None
    type: Optional[str] = None
    value: Optional[str] = None


class V2ContainerResourceMetricSource(ResourceValue):
    container: Optional[str] = None
    name: Optional[str] = None
    target: V2MetricTarget = Field(default_factory=lambda: V2MetricTarget())


class V2MetricSpec(ResourceValue):
    containerResource: V2ContainerResourceMetricSource = Field(
        default_factory=lambda: V2ContainerResourceMetricSource()
    )
    external: V2ExternalMetricSource = Field(default_factory=lambda: V2ExternalMetricSource())
    object: V2ObjectMetricSource = Field(default_factory=lambda: V2ObjectMetricSource())
    pods: V2PodsMetricSource = Field(default_factory=lambda: V2PodsMetricSource())
    resource: V2ResourceMetricSource = Field(default_factory=lambda: V2ResourceMetricSource())
    type: Optional[str] = None


class V2HPAScalingPolicy(ResourceValue):
    periodSeconds: Optional[int] = None
    type: Optional[str] = None
    value: Optional[int] = None


class V2HPAScalingRules(ResourceValue):
    policies: List[V2HPAScalingPolicy] = Field(default_factory=list)
    selectPolicy: Optional[str] = None
    stabilizationWindowSeconds: Optional[int] = None


class V2HorizontalPodAutoscalerBehavior(ResourceValue):
    scaleDown: V2HPAScalingRules = Field(default_factory=lambda: V2HPAScalingRules())
    scaleUp: V2HPAScalingRules = Field(default_factory=lambda: V2HPAScalingRules())


class V2HorizontalPodAutoscalerSpec(ResourceValue):
    behavior: V2HorizontalPodAutoscalerBehavior = Field(default_factory=lambda: V2HorizontalPodAutoscalerBehavior())
    maxReplicas: Optional[int] = None
    metrics: List[V2MetricSpec] = Field(default_factory=list)
    minReplicas: Optional[int] = None
    scaleTargetRef: V2CrossVersionObjectReference = Field(default_factory=lambda: V2CrossVersionObjectReference())


class V2HorizontalPodAutoscaler(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V2HorizontalPodAutoscalerSpec = Field(default_factory=lambda: V2HorizontalPodAutoscalerSpec())
    status: V2HorizontalPodAutoscalerStatus = Field(default_factory=lambda: V2HorizontalPodAutoscalerStatus())


class V2CrossVersionObjectReference(ResourceItem):
    name: Optional[str] = None


class V1beta3PriorityLevelConfigurationList(ResourceItem):
    items: List[V1beta3PriorityLevelConfiguration] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1beta3PriorityLevelConfigurationCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1beta3PriorityLevelConfigurationStatus(ResourceValue):
    conditions: List[V1beta3PriorityLevelConfigurationCondition] = Field(default_factory=list)


class V1beta3QueuingConfiguration(ResourceValue):
    handSize: Optional[int] = None
    queueLengthLimit: Optional[int] = None
    queues: Optional[int] = None


class V1beta3LimitResponse(ResourceValue):
    queuing: V1beta3QueuingConfiguration = Field(default_factory=lambda: V1beta3QueuingConfiguration())
    type: Optional[str] = None


class V1beta3LimitedPriorityLevelConfiguration(ResourceValue):
    borrowingLimitPercent: Optional[int] = None
    lendablePercent: Optional[int] = None
    limitResponse: V1beta3LimitResponse = Field(default_factory=lambda: V1beta3LimitResponse())
    nominalConcurrencyShares: Optional[int] = None


class V1beta3PriorityLevelConfigurationSpec(ResourceValue):
    limited: V1beta3LimitedPriorityLevelConfiguration = Field(
        default_factory=lambda: V1beta3LimitedPriorityLevelConfiguration()
    )
    type: Optional[str] = None


class V1beta3PriorityLevelConfiguration(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1beta3PriorityLevelConfigurationSpec = Field(default_factory=lambda: V1beta3PriorityLevelConfigurationSpec())
    status: V1beta3PriorityLevelConfigurationStatus = Field(
        default_factory=lambda: V1beta3PriorityLevelConfigurationStatus()
    )


class V1beta3FlowSchemaList(ResourceItem):
    items: List[V1beta3FlowSchema] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1beta3FlowSchemaCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1beta3FlowSchemaStatus(ResourceValue):
    conditions: List[V1beta3FlowSchemaCondition] = Field(default_factory=list)


class V1beta3UserSubject(ResourceValue):
    name: Optional[str] = None


class V1beta3ServiceAccountSubject(ResourceValue):
    name: Optional[str] = None
    namespace: Optional[str] = None


class V1beta3GroupSubject(ResourceValue):
    name: Optional[str] = None


class V1beta3Subject(ResourceValue):
    group: V1beta3GroupSubject = Field(default_factory=lambda: V1beta3GroupSubject())
    kind: Optional[str] = None
    serviceAccount: V1beta3ServiceAccountSubject = Field(default_factory=lambda: V1beta3ServiceAccountSubject())
    user: V1beta3UserSubject = Field(default_factory=lambda: V1beta3UserSubject())


class V1beta3ResourcePolicyRule(ResourceValue):
    apiGroups: List[str] = Field(default_factory=list)
    clusterScope: Optional[bool] = None
    namespaces: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    verbs: List[str] = Field(default_factory=list)


class V1beta3NonResourcePolicyRule(ResourceValue):
    nonResourceURLs: List[str] = Field(default_factory=list)
    verbs: List[str] = Field(default_factory=list)


class V1beta3PolicyRulesWithSubjects(ResourceValue):
    nonResourceRules: List[V1beta3NonResourcePolicyRule] = Field(default_factory=list)
    resourceRules: List[V1beta3ResourcePolicyRule] = Field(default_factory=list)
    subjects: List[V1beta3Subject] = Field(default_factory=list)


class V1beta3PriorityLevelConfigurationReference(ResourceValue):
    name: Optional[str] = None


class V1beta3FlowDistinguisherMethod(ResourceValue):
    type: Optional[str] = None


class V1beta3FlowSchemaSpec(ResourceValue):
    distinguisherMethod: V1beta3FlowDistinguisherMethod = Field(
        default_factory=lambda: V1beta3FlowDistinguisherMethod()
    )
    matchingPrecedence: Optional[int] = None
    priorityLevelConfiguration: V1beta3PriorityLevelConfigurationReference = Field(
        default_factory=lambda: V1beta3PriorityLevelConfigurationReference()
    )
    rules: List[V1beta3PolicyRulesWithSubjects] = Field(default_factory=list)


class V1beta3FlowSchema(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1beta3FlowSchemaSpec = Field(default_factory=lambda: V1beta3FlowSchemaSpec())
    status: V1beta3FlowSchemaStatus = Field(default_factory=lambda: V1beta3FlowSchemaStatus())


class V1beta2PriorityLevelConfigurationList(ResourceItem):
    items: List[V1beta2PriorityLevelConfiguration] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1beta2PriorityLevelConfigurationCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1beta2PriorityLevelConfigurationStatus(ResourceValue):
    conditions: List[V1beta2PriorityLevelConfigurationCondition] = Field(default_factory=list)


class V1beta2QueuingConfiguration(ResourceValue):
    handSize: Optional[int] = None
    queueLengthLimit: Optional[int] = None
    queues: Optional[int] = None


class V1beta2LimitResponse(ResourceValue):
    queuing: V1beta2QueuingConfiguration = Field(default_factory=lambda: V1beta2QueuingConfiguration())
    type: Optional[str] = None


class V1beta2LimitedPriorityLevelConfiguration(ResourceValue):
    assuredConcurrencyShares: Optional[int] = None
    borrowingLimitPercent: Optional[int] = None
    lendablePercent: Optional[int] = None
    limitResponse: V1beta2LimitResponse = Field(default_factory=lambda: V1beta2LimitResponse())


class V1beta2PriorityLevelConfigurationSpec(ResourceValue):
    limited: V1beta2LimitedPriorityLevelConfiguration = Field(
        default_factory=lambda: V1beta2LimitedPriorityLevelConfiguration()
    )
    type: Optional[str] = None


class V1beta2PriorityLevelConfiguration(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1beta2PriorityLevelConfigurationSpec = Field(default_factory=lambda: V1beta2PriorityLevelConfigurationSpec())
    status: V1beta2PriorityLevelConfigurationStatus = Field(
        default_factory=lambda: V1beta2PriorityLevelConfigurationStatus()
    )


class V1beta2FlowSchemaList(ResourceItem):
    items: List[V1beta2FlowSchema] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1beta2FlowSchemaCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1beta2FlowSchemaStatus(ResourceValue):
    conditions: List[V1beta2FlowSchemaCondition] = Field(default_factory=list)


class V1beta2UserSubject(ResourceValue):
    name: Optional[str] = None


class V1beta2ServiceAccountSubject(ResourceValue):
    name: Optional[str] = None
    namespace: Optional[str] = None


class V1beta2GroupSubject(ResourceValue):
    name: Optional[str] = None


class V1beta2Subject(ResourceValue):
    group: V1beta2GroupSubject = Field(default_factory=lambda: V1beta2GroupSubject())
    kind: Optional[str] = None
    serviceAccount: V1beta2ServiceAccountSubject = Field(default_factory=lambda: V1beta2ServiceAccountSubject())
    user: V1beta2UserSubject = Field(default_factory=lambda: V1beta2UserSubject())


class V1beta2ResourcePolicyRule(ResourceValue):
    apiGroups: List[str] = Field(default_factory=list)
    clusterScope: Optional[bool] = None
    namespaces: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    verbs: List[str] = Field(default_factory=list)


class V1beta2NonResourcePolicyRule(ResourceValue):
    nonResourceURLs: List[str] = Field(default_factory=list)
    verbs: List[str] = Field(default_factory=list)


class V1beta2PolicyRulesWithSubjects(ResourceValue):
    nonResourceRules: List[V1beta2NonResourcePolicyRule] = Field(default_factory=list)
    resourceRules: List[V1beta2ResourcePolicyRule] = Field(default_factory=list)
    subjects: List[V1beta2Subject] = Field(default_factory=list)


class V1beta2PriorityLevelConfigurationReference(ResourceValue):
    name: Optional[str] = None


class V1beta2FlowDistinguisherMethod(ResourceValue):
    type: Optional[str] = None


class V1beta2FlowSchemaSpec(ResourceValue):
    distinguisherMethod: V1beta2FlowDistinguisherMethod = Field(
        default_factory=lambda: V1beta2FlowDistinguisherMethod()
    )
    matchingPrecedence: Optional[int] = None
    priorityLevelConfiguration: V1beta2PriorityLevelConfigurationReference = Field(
        default_factory=lambda: V1beta2PriorityLevelConfigurationReference()
    )
    rules: List[V1beta2PolicyRulesWithSubjects] = Field(default_factory=list)


class V1beta2FlowSchema(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1beta2FlowSchemaSpec = Field(default_factory=lambda: V1beta2FlowSchemaSpec())
    status: V1beta2FlowSchemaStatus = Field(default_factory=lambda: V1beta2FlowSchemaStatus())


class V1beta1CSIStorageCapacityList(ResourceItem):
    items: List[V1beta1CSIStorageCapacity] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1beta1CSIStorageCapacity(ResourceItem):
    capacity: Optional[str] = None
    maximumVolumeSize: Optional[str] = None
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    nodeTopology: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    storageClassName: Optional[str] = None


class V1alpha1ValidatingAdmissionPolicyList(ResourceItem):
    items: List[V1alpha1ValidatingAdmissionPolicy] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1alpha1ValidatingAdmissionPolicyBindingList(ResourceItem):
    items: List[V1alpha1ValidatingAdmissionPolicyBinding] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1alpha1ParamRef(ResourceValue):
    name: Optional[str] = None
    namespace: Optional[str] = None


class V1alpha1ValidatingAdmissionPolicyBindingSpec(ResourceValue):
    matchResources: V1alpha1MatchResources = Field(default_factory=lambda: V1alpha1MatchResources())
    paramRef: V1alpha1ParamRef = Field(default_factory=lambda: V1alpha1ParamRef())
    policyName: Optional[str] = None


class V1alpha1ValidatingAdmissionPolicyBinding(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1alpha1ValidatingAdmissionPolicyBindingSpec = Field(
        default_factory=lambda: V1alpha1ValidatingAdmissionPolicyBindingSpec()
    )


class V1alpha1Validation(ResourceValue):
    expression: Optional[str] = None
    message: Optional[str] = None
    reason: Optional[str] = None


class V1alpha1NamedRuleWithOperations(ResourceValue):
    apiGroups: List[str] = Field(default_factory=list)
    apiVersions: List[str] = Field(default_factory=list)
    operations: List[str] = Field(default_factory=list)
    resourceNames: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    scope: Optional[str] = None


class V1alpha1MatchResources(ResourceValue):
    excludeResourceRules: List[V1alpha1NamedRuleWithOperations] = Field(default_factory=list)
    matchPolicy: Optional[str] = None
    namespaceSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    objectSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    resourceRules: List[V1alpha1NamedRuleWithOperations] = Field(default_factory=list)


class V1alpha1ValidatingAdmissionPolicySpec(ResourceValue):
    failurePolicy: Optional[str] = None
    matchConstraints: V1alpha1MatchResources = Field(default_factory=lambda: V1alpha1MatchResources())
    paramKind: V1alpha1ParamKind = Field(default_factory=lambda: V1alpha1ParamKind())
    validations: List[V1alpha1Validation] = Field(default_factory=list)


class V1alpha1ValidatingAdmissionPolicy(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1alpha1ValidatingAdmissionPolicySpec = Field(default_factory=lambda: V1alpha1ValidatingAdmissionPolicySpec())


class V1alpha1StorageVersionList(ResourceItem):
    items: List[V1alpha1StorageVersion] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1alpha1ServerStorageVersion(ResourceValue):
    apiServerID: Optional[str] = None
    decodableVersions: List[str] = Field(default_factory=list)
    encodingVersion: Optional[str] = None


class V1alpha1StorageVersionCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    observedGeneration: Optional[int] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1alpha1StorageVersionStatus(ResourceValue):
    commonEncodingVersion: Optional[str] = None
    conditions: List[V1alpha1StorageVersionCondition] = Field(default_factory=list)
    storageVersions: List[V1alpha1ServerStorageVersion] = Field(default_factory=list)


class V1alpha1StorageVersion(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: Optional[object] = None
    status: V1alpha1StorageVersionStatus = Field(default_factory=lambda: V1alpha1StorageVersionStatus())


class V1alpha1SelfSubjectReviewStatus(ResourceValue):
    userInfo: V1UserInfo = Field(default_factory=lambda: V1UserInfo())


class V1alpha1SelfSubjectReview(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    status: V1alpha1SelfSubjectReviewStatus = Field(default_factory=lambda: V1alpha1SelfSubjectReviewStatus())


class V1alpha1ResourceClassList(ResourceItem):
    items: List[V1alpha1ResourceClass] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1alpha1ResourceClassParametersReference(ResourceValue):
    apiGroup: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None


class V1alpha1ResourceClass(ResourceItem):
    driverName: Optional[str] = None
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    parametersRef: V1alpha1ResourceClassParametersReference = Field(
        default_factory=lambda: V1alpha1ResourceClassParametersReference()
    )
    suitableNodes: V1NodeSelector = Field(default_factory=lambda: V1NodeSelector())


class V1alpha1ResourceClaimTemplateList(ResourceItem):
    items: List[V1alpha1ResourceClaimTemplate] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1alpha1ResourceClaimTemplateSpec(ResourceValue):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1alpha1ResourceClaimSpec = Field(default_factory=lambda: V1alpha1ResourceClaimSpec())


class V1alpha1ResourceClaimTemplate(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1alpha1ResourceClaimTemplateSpec = Field(default_factory=lambda: V1alpha1ResourceClaimTemplateSpec())


class V1alpha1ResourceClaimList(ResourceItem):
    items: List[V1alpha1ResourceClaim] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1alpha1ResourceClaimConsumerReference(ResourceValue):
    apiGroup: Optional[str] = None
    name: Optional[str] = None
    resource: Optional[str] = None
    uid: Optional[str] = None


class V1alpha1AllocationResult(ResourceValue):
    availableOnNodes: V1NodeSelector = Field(default_factory=lambda: V1NodeSelector())
    resourceHandle: Optional[str] = None
    shareable: Optional[bool] = None


class V1alpha1ResourceClaimStatus(ResourceValue):
    allocation: V1alpha1AllocationResult = Field(default_factory=lambda: V1alpha1AllocationResult())
    deallocationRequested: Optional[bool] = None
    driverName: Optional[str] = None
    reservedFor: List[V1alpha1ResourceClaimConsumerReference] = Field(default_factory=list)


class V1alpha1ResourceClaimParametersReference(ResourceValue):
    apiGroup: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None


class V1alpha1ResourceClaimSpec(ResourceValue):
    allocationMode: Optional[str] = None
    parametersRef: V1alpha1ResourceClaimParametersReference = Field(
        default_factory=lambda: V1alpha1ResourceClaimParametersReference()
    )
    resourceClassName: Optional[str] = None


class V1alpha1ResourceClaim(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1alpha1ResourceClaimSpec = Field(default_factory=lambda: V1alpha1ResourceClaimSpec())
    status: V1alpha1ResourceClaimStatus = Field(default_factory=lambda: V1alpha1ResourceClaimStatus())


class V1alpha1PodSchedulingList(ResourceItem):
    items: List[V1alpha1PodScheduling] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1alpha1ResourceClaimSchedulingStatus(ResourceValue):
    name: Optional[str] = None
    unsuitableNodes: List[str] = Field(default_factory=list)


class V1alpha1PodSchedulingStatus(ResourceValue):
    resourceClaims: List[V1alpha1ResourceClaimSchedulingStatus] = Field(default_factory=list)


class V1alpha1PodSchedulingSpec(ResourceValue):
    potentialNodes: List[str] = Field(default_factory=list)
    selectedNode: Optional[str] = None


class V1alpha1PodScheduling(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1alpha1PodSchedulingSpec = Field(default_factory=lambda: V1alpha1PodSchedulingSpec())
    status: V1alpha1PodSchedulingStatus = Field(default_factory=lambda: V1alpha1PodSchedulingStatus())


class V1alpha1ParamKind(ResourceItem):
    pass


class V1alpha1ClusterCIDRList(ResourceItem):
    items: List[V1alpha1ClusterCIDR] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1alpha1ClusterCIDRSpec(ResourceValue):
    ipv4: Optional[str] = None
    ipv6: Optional[str] = None
    nodeSelector: V1NodeSelector = Field(default_factory=lambda: V1NodeSelector())
    perNodeHostBits: Optional[int] = None


class V1alpha1ClusterCIDR(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1alpha1ClusterCIDRSpec = Field(default_factory=lambda: V1alpha1ClusterCIDRSpec())


class V1VolumeAttachmentList(ResourceItem):
    items: List[V1VolumeAttachment] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1VolumeError(ResourceValue):
    message: Optional[str] = None
    time: Optional[datetime] = None


class V1VolumeAttachmentStatus(ResourceValue):
    attachError: V1VolumeError = Field(default_factory=lambda: V1VolumeError())
    attached: Optional[bool] = None
    attachmentMetadata: Dict[str, str] = Field(default_factory=dict)
    detachError: V1VolumeError = Field(default_factory=lambda: V1VolumeError())


class V1VolumeAttachmentSource(ResourceValue):
    inlineVolumeSpec: V1PersistentVolumeSpec = Field(default_factory=lambda: V1PersistentVolumeSpec())
    persistentVolumeName: Optional[str] = None


class V1VolumeAttachmentSpec(ResourceValue):
    attacher: Optional[str] = None
    nodeName: Optional[str] = None
    source: V1VolumeAttachmentSource = Field(default_factory=lambda: V1VolumeAttachmentSource())


class V1VolumeAttachment(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1VolumeAttachmentSpec = Field(default_factory=lambda: V1VolumeAttachmentSpec())
    status: V1VolumeAttachmentStatus = Field(default_factory=lambda: V1VolumeAttachmentStatus())


class V1ValidatingWebhookConfigurationList(ResourceItem):
    items: List[V1ValidatingWebhookConfiguration] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ValidatingWebhook(ResourceValue):
    admissionReviewVersions: List[str] = Field(default_factory=list)
    clientConfig: AdmissionregistrationV1WebhookClientConfig = Field(
        default_factory=lambda: AdmissionregistrationV1WebhookClientConfig()
    )
    failurePolicy: Optional[str] = None
    matchPolicy: Optional[str] = None
    name: Optional[str] = None
    namespaceSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    objectSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    rules: List[V1RuleWithOperations] = Field(default_factory=list)
    sideEffects: Optional[str] = None
    timeoutSeconds: Optional[int] = None


class V1ValidatingWebhookConfiguration(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    webhooks: List[V1ValidatingWebhook] = Field(default_factory=list)


class V1UserInfo(ResourceValue):
    extra: Dict[str, List[str]] = Field(default_factory=dict)
    groups: List[str] = Field(default_factory=list)
    uid: Optional[str] = None
    username: Optional[str] = None


class V1TokenReviewStatus(ResourceValue):
    audiences: List[str] = Field(default_factory=list)
    authenticated: Optional[bool] = None
    error: Optional[str] = None
    user: V1UserInfo = Field(default_factory=lambda: V1UserInfo())


class V1TokenReviewSpec(ResourceValue):
    audiences: List[str] = Field(default_factory=list)
    token: Optional[str] = None


class V1TokenReview(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1TokenReviewSpec = Field(default_factory=lambda: V1TokenReviewSpec())
    status: V1TokenReviewStatus = Field(default_factory=lambda: V1TokenReviewStatus())


class V1SubjectAccessReview(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1SubjectAccessReviewSpec = Field(default_factory=lambda: V1SubjectAccessReviewSpec())
    status: V1SubjectAccessReviewStatus = Field(default_factory=lambda: V1SubjectAccessReviewStatus())


class V1StorageClassList(ResourceItem):
    items: List[V1StorageClass] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1TopologySelectorLabelRequirement(ResourceValue):
    key: Optional[str] = None
    values: List[str] = Field(default_factory=list)


class V1TopologySelectorTerm(ResourceValue):
    matchLabelExpressions: List[V1TopologySelectorLabelRequirement] = Field(default_factory=list)


class V1StorageClass(ResourceItem):
    allowVolumeExpansion: Optional[bool] = None
    allowedTopologies: List[V1TopologySelectorTerm] = Field(default_factory=list)
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    mountOptions: List[str] = Field(default_factory=list)
    parameters: Dict[str, str] = Field(default_factory=dict)
    provisioner: Optional[str] = None
    reclaimPolicy: Optional[str] = None
    volumeBindingMode: Optional[str] = None


class V1StatusCause(ResourceValue):
    field: Optional[str] = None
    message: Optional[str] = None
    reason: Optional[str] = None


class V1StatusDetails(ResourceValue):
    causes: List[V1StatusCause] = Field(default_factory=list)
    group: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    retryAfterSeconds: Optional[int] = None
    uid: Optional[str] = None


class V1Status(ResourceItem):
    code: Optional[int] = None
    details: V1StatusDetails = Field(default_factory=lambda: V1StatusDetails())
    message: Optional[str] = None
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())
    reason: Optional[str] = None
    status: Optional[str] = None


class V1StatefulSetList(ResourceItem):
    items: List[V1StatefulSet] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1StatefulSetCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1StatefulSetStatus(ResourceValue):
    availableReplicas: Optional[int] = None
    collisionCount: Optional[int] = None
    conditions: List[V1StatefulSetCondition] = Field(default_factory=list)
    currentReplicas: Optional[int] = None
    currentRevision: Optional[str] = None
    observedGeneration: Optional[int] = None
    readyReplicas: Optional[int] = None
    replicas: Optional[int] = None
    updateRevision: Optional[str] = None
    updatedReplicas: Optional[int] = None


class V1RollingUpdateStatefulSetStrategy(ResourceValue):
    maxUnavailable: Optional[Union[str, int]] = None
    partition: Optional[int] = None


class V1StatefulSetUpdateStrategy(ResourceValue):
    rollingUpdate: V1RollingUpdateStatefulSetStrategy = Field(
        default_factory=lambda: V1RollingUpdateStatefulSetStrategy()
    )
    type: Optional[str] = None


class V1StatefulSetPersistentVolumeClaimRetentionPolicy(ResourceValue):
    whenDeleted: Optional[str] = None
    whenScaled: Optional[str] = None


class V1StatefulSetOrdinals(ResourceValue):
    start: Optional[int] = None


class V1StatefulSetSpec(ResourceValue):
    minReadySeconds: Optional[int] = None
    ordinals: V1StatefulSetOrdinals = Field(default_factory=lambda: V1StatefulSetOrdinals())
    persistentVolumeClaimRetentionPolicy: V1StatefulSetPersistentVolumeClaimRetentionPolicy = Field(
        default_factory=lambda: V1StatefulSetPersistentVolumeClaimRetentionPolicy()
    )
    podManagementPolicy: Optional[str] = None
    replicas: Optional[int] = None
    revisionHistoryLimit: Optional[int] = None
    selector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    serviceName: Optional[str] = None
    template: V1PodTemplateSpec = Field(default_factory=lambda: V1PodTemplateSpec())
    updateStrategy: V1StatefulSetUpdateStrategy = Field(default_factory=lambda: V1StatefulSetUpdateStrategy())
    volumeClaimTemplates: List[V1PersistentVolumeClaim] = Field(default_factory=list)


class V1ServiceList(ResourceItem):
    items: List[V1Service] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ServiceAccountList(ResourceItem):
    items: List[V1ServiceAccount] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ServiceAccount(ResourceItem):
    automountServiceAccountToken: Optional[bool] = None
    imagePullSecrets: List[V1LocalObjectReference] = Field(default_factory=list)
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    secrets: List[V1ObjectReference] = Field(default_factory=list)


class V1PortStatus(ResourceValue):
    error: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[str] = None


class V1LoadBalancerIngress(ResourceValue):
    hostname: Optional[str] = None
    ip: Optional[str] = None
    ports: List[V1PortStatus] = Field(default_factory=list)


class V1LoadBalancerStatus(ResourceValue):
    ingress: List[V1LoadBalancerIngress] = Field(default_factory=list)


class V1ServiceStatus(ResourceValue):
    conditions: List[V1Condition] = Field(default_factory=list)
    loadBalancer: V1LoadBalancerStatus = Field(default_factory=lambda: V1LoadBalancerStatus())


class V1ClientIPConfig(ResourceValue):
    timeoutSeconds: Optional[int] = None


class V1SessionAffinityConfig(ResourceValue):
    clientIP: V1ClientIPConfig = Field(default_factory=lambda: V1ClientIPConfig())


class V1ServicePort(ResourceValue):
    appProtocol: Optional[str] = None
    name: Optional[str] = None
    nodePort: Optional[int] = None
    port: Optional[int] = None
    protocol: Optional[str] = None
    targetPort: Optional[object] = None


class V1ServiceSpec(ResourceValue):
    allocateLoadBalancerNodePorts: Optional[bool] = None
    clusterIP: Optional[str] = None
    clusterIPs: List[str] = Field(default_factory=list)
    externalIPs: List[str] = Field(default_factory=list)
    externalName: Optional[str] = None
    externalTrafficPolicy: Optional[str] = None
    healthCheckNodePort: Optional[int] = None
    internalTrafficPolicy: Optional[str] = None
    ipFamilies: List[str] = Field(default_factory=list)
    ipFamilyPolicy: Optional[str] = None
    loadBalancerClass: Optional[str] = None
    loadBalancerIP: Optional[str] = None
    loadBalancerSourceRanges: List[str] = Field(default_factory=list)
    ports: List[V1ServicePort] = Field(default_factory=list)
    publishNotReadyAddresses: Optional[bool] = None
    selector: Dict[str, str] = Field(default_factory=dict)
    sessionAffinity: Optional[str] = None
    sessionAffinityConfig: V1SessionAffinityConfig = Field(default_factory=lambda: V1SessionAffinityConfig())
    type: Optional[str] = None


class V1Service(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1ServiceSpec = Field(default_factory=lambda: V1ServiceSpec())
    status: V1ServiceStatus = Field(default_factory=lambda: V1ServiceStatus())


class V1ResourceRule(ResourceValue):
    apiGroups: List[str] = Field(default_factory=list)
    resourceNames: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    verbs: List[str] = Field(default_factory=list)


class V1NonResourceRule(ResourceValue):
    nonResourceURLs: List[str] = Field(default_factory=list)
    verbs: List[str] = Field(default_factory=list)


class V1SubjectRulesReviewStatus(ResourceValue):
    evaluationError: Optional[str] = None
    incomplete: Optional[bool] = None
    nonResourceRules: List[V1NonResourceRule] = Field(default_factory=list)
    resourceRules: List[V1ResourceRule] = Field(default_factory=list)


class V1SelfSubjectRulesReviewSpec(ResourceValue):
    namespace: Optional[str] = None


class V1SelfSubjectRulesReview(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1SelfSubjectRulesReviewSpec = Field(default_factory=lambda: V1SelfSubjectRulesReviewSpec())
    status: V1SubjectRulesReviewStatus = Field(default_factory=lambda: V1SubjectRulesReviewStatus())


class V1SelfSubjectAccessReviewSpec(ResourceValue):
    nonResourceAttributes: V1NonResourceAttributes = Field(default_factory=lambda: V1NonResourceAttributes())
    resourceAttributes: V1ResourceAttributes = Field(default_factory=lambda: V1ResourceAttributes())


class V1SelfSubjectAccessReview(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1SelfSubjectAccessReviewSpec = Field(default_factory=lambda: V1SelfSubjectAccessReviewSpec())
    status: V1SubjectAccessReviewStatus = Field(default_factory=lambda: V1SubjectAccessReviewStatus())


class V1SecretList(ResourceItem):
    items: List[V1Secret] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ScaleStatus(ResourceValue):
    replicas: Optional[int] = None
    selector: Optional[str] = None


class V1ScaleSpec(ResourceValue):
    replicas: Optional[int] = None


class V1Scale(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1ScaleSpec = Field(default_factory=lambda: V1ScaleSpec())
    status: V1ScaleStatus = Field(default_factory=lambda: V1ScaleStatus())


class V1RuntimeClassList(ResourceItem):
    items: List[V1RuntimeClass] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1Scheduling(ResourceValue):
    nodeSelector: Dict[str, str] = Field(default_factory=dict)
    tolerations: List[V1Toleration] = Field(default_factory=list)


class V1Overhead(ResourceValue):
    podFixed: Dict[str, str] = Field(default_factory=dict)


class V1RuntimeClass(ResourceItem):
    handler: Optional[str] = None
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    overhead: V1Overhead = Field(default_factory=lambda: V1Overhead())
    scheduling: V1Scheduling = Field(default_factory=lambda: V1Scheduling())


class V1RoleList(ResourceItem):
    items: List[V1Role] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1RoleBindingList(ResourceItem):
    items: List[V1RoleBinding] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1RoleBinding(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    roleRef: V1RoleRef = Field(default_factory=lambda: V1RoleRef())
    subjects: List[V1Subject] = Field(default_factory=list)


class V1Role(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    rules: List[V1PolicyRule] = Field(default_factory=list)


class V1ResourceQuotaList(ResourceItem):
    items: List[V1ResourceQuota] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ResourceQuotaStatus(ResourceValue):
    hard: Dict[str, str] = Field(default_factory=dict)
    used: Dict[str, str] = Field(default_factory=dict)


class V1ScopedResourceSelectorRequirement(ResourceValue):
    operator: Optional[str] = None
    scopeName: Optional[str] = None
    values: List[str] = Field(default_factory=list)


class V1ScopeSelector(ResourceValue):
    matchExpressions: List[V1ScopedResourceSelectorRequirement] = Field(default_factory=list)


class V1ResourceQuotaSpec(ResourceValue):
    hard: Dict[str, str] = Field(default_factory=dict)
    scopeSelector: V1ScopeSelector = Field(default_factory=lambda: V1ScopeSelector())
    scopes: List[str] = Field(default_factory=list)


class V1ResourceQuota(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1ResourceQuotaSpec = Field(default_factory=lambda: V1ResourceQuotaSpec())
    status: V1ResourceQuotaStatus = Field(default_factory=lambda: V1ResourceQuotaStatus())


class V1ReplicationControllerList(ResourceItem):
    items: List[V1ReplicationController] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ReplicationControllerCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1ReplicationControllerStatus(ResourceValue):
    availableReplicas: Optional[int] = None
    conditions: List[V1ReplicationControllerCondition] = Field(default_factory=list)
    fullyLabeledReplicas: Optional[int] = None
    observedGeneration: Optional[int] = None
    readyReplicas: Optional[int] = None
    replicas: Optional[int] = None


class V1ReplicationControllerSpec(ResourceValue):
    minReadySeconds: Optional[int] = None
    replicas: Optional[int] = None
    selector: Dict[str, str] = Field(default_factory=dict)
    template: V1PodTemplateSpec = Field(default_factory=lambda: V1PodTemplateSpec())


class V1ReplicationController(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1ReplicationControllerSpec = Field(default_factory=lambda: V1ReplicationControllerSpec())
    status: V1ReplicationControllerStatus = Field(default_factory=lambda: V1ReplicationControllerStatus())


class V1ReplicaSetList(ResourceItem):
    items: List[V1ReplicaSet] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ReplicaSetCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1ReplicaSetStatus(ResourceValue):
    availableReplicas: Optional[int] = None
    conditions: List[V1ReplicaSetCondition] = Field(default_factory=list)
    fullyLabeledReplicas: Optional[int] = None
    observedGeneration: Optional[int] = None
    readyReplicas: Optional[int] = None
    replicas: Optional[int] = None


class V1ReplicaSetSpec(ResourceValue):
    minReadySeconds: Optional[int] = None
    replicas: Optional[int] = None
    selector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    template: V1PodTemplateSpec = Field(default_factory=lambda: V1PodTemplateSpec())


class V1ReplicaSet(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1ReplicaSetSpec = Field(default_factory=lambda: V1ReplicaSetSpec())
    status: V1ReplicaSetStatus = Field(default_factory=lambda: V1ReplicaSetStatus())


class V1PriorityClassList(ResourceItem):
    items: List[V1PriorityClass] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1PriorityClass(ResourceItem):
    description: Optional[str] = None
    globalDefault: Optional[bool] = None
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    preemptionPolicy: Optional[str] = None
    value: Optional[int] = None


class V1PodTemplateList(ResourceItem):
    items: List[V1PodTemplate] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1PodTemplate(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    template: V1PodTemplateSpec = Field(default_factory=lambda: V1PodTemplateSpec())


class V1PodList(ResourceItem):
    items: List[V1Pod] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1PodDisruptionBudgetList(ResourceItem):
    items: List[V1PodDisruptionBudget] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1PodDisruptionBudgetStatus(ResourceValue):
    conditions: List[V1Condition] = Field(default_factory=list)
    currentHealthy: Optional[int] = None
    desiredHealthy: Optional[int] = None
    disruptedPods: Dict[str, datetime] = Field(default_factory=dict)
    disruptionsAllowed: Optional[int] = None
    expectedPods: Optional[int] = None
    observedGeneration: Optional[int] = None


class V1PodDisruptionBudgetSpec(ResourceValue):
    maxUnavailable: Optional[object] = None
    minAvailable: Optional[object] = None
    selector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    unhealthyPodEvictionPolicy: Optional[str] = None


class V1PodDisruptionBudget(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1PodDisruptionBudgetSpec = Field(default_factory=lambda: V1PodDisruptionBudgetSpec())
    status: V1PodDisruptionBudgetStatus = Field(default_factory=lambda: V1PodDisruptionBudgetStatus())


class V1PodIP(ResourceValue):
    ip: Optional[str] = None


class V1ContainerStateWaiting(ResourceValue):
    message: Optional[str] = None
    reason: Optional[str] = None


class V1ContainerStateTerminated(ResourceValue):
    containerID: Optional[str] = None
    exitCode: Optional[int] = None
    finishedAt: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    signal: Optional[int] = None
    startedAt: Optional[datetime] = None


class V1ContainerStateRunning(ResourceValue):
    startedAt: Optional[datetime] = None


class V1ContainerState(ResourceValue):
    running: V1ContainerStateRunning = Field(default_factory=lambda: V1ContainerStateRunning())
    terminated: V1ContainerStateTerminated = Field(default_factory=lambda: V1ContainerStateTerminated())
    waiting: V1ContainerStateWaiting = Field(default_factory=lambda: V1ContainerStateWaiting())


class V1ContainerStatus(ResourceValue):
    containerID: Optional[str] = None
    image: Optional[str] = None
    imageID: Optional[str] = None
    lastState: V1ContainerState = Field(default_factory=lambda: V1ContainerState())
    name: Optional[str] = None
    ready: Optional[bool] = None
    restartCount: int = 0
    started: Optional[bool] = None
    state: V1ContainerState = Field(default_factory=lambda: V1ContainerState())


class V1PodCondition(ResourceValue):
    lastProbeTime: Optional[datetime] = None
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1PodStatus(ResourceValue):
    conditions: List[V1PodCondition] = Field(default_factory=list)
    containerStatuses: List[V1ContainerStatus] = Field(default_factory=list)
    ephemeralContainerStatuses: List[V1ContainerStatus] = Field(default_factory=list)
    hostIP: Optional[str] = None
    initContainerStatuses: List[V1ContainerStatus] = Field(default_factory=list)
    message: Optional[str] = None
    nominatedNodeName: Optional[str] = None
    phase: Optional[str] = None
    podIP: Optional[str] = None
    podIPs: List[V1PodIP] = Field(default_factory=list)
    qosClass: Optional[str] = None
    reason: Optional[str] = None
    startTime: Optional[datetime] = None


class V1PersistentVolumeList(ResourceItem):
    items: List[V1PersistentVolume] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1PersistentVolumeClaimList(ResourceItem):
    items: List[V1PersistentVolumeClaim] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1PersistentVolumeClaimCondition(ResourceValue):
    lastProbeTime: Optional[datetime] = None
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1PersistentVolumeClaimStatus(ResourceValue):
    accessModes: List[str] = Field(default_factory=list)
    allocatedResources: Dict[str, str] = Field(default_factory=dict)
    capacity: Dict[str, str] = Field(default_factory=dict)
    conditions: List[V1PersistentVolumeClaimCondition] = Field(default_factory=list)
    phase: Optional[str] = None
    resizeStatus: Optional[str] = None


class V1PersistentVolumeClaim(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1PersistentVolumeClaimSpec = Field(default_factory=lambda: V1PersistentVolumeClaimSpec())
    status: V1PersistentVolumeClaimStatus = Field(default_factory=lambda: V1PersistentVolumeClaimStatus())


class V1PersistentVolumeStatus(ResourceValue):
    message: Optional[str] = None
    phase: Optional[str] = None
    reason: Optional[str] = None


class V1StorageOSPersistentVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: V1ObjectReference = Field(default_factory=lambda: V1ObjectReference())
    volumeName: Optional[str] = None
    volumeNamespace: Optional[str] = None


class V1ScaleIOPersistentVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    gateway: Optional[str] = None
    protectionDomain: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    sslEnabled: Optional[bool] = None
    storageMode: Optional[str] = None
    storagePool: Optional[str] = None
    system: Optional[str] = None
    volumeName: Optional[str] = None


class V1RBDPersistentVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    image: Optional[str] = None
    keyring: Optional[str] = None
    monitors: List[str] = Field(default_factory=list)
    pool: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    user: Optional[str] = None


class V1VolumeNodeAffinity(ResourceValue):
    required: V1NodeSelector = Field(default_factory=lambda: V1NodeSelector())


class V1LocalVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    path: Optional[str] = None


class V1ISCSIPersistentVolumeSource(ResourceValue):
    chapAuthDiscovery: Optional[bool] = None
    chapAuthSession: Optional[bool] = None
    fsType: Optional[str] = None
    initiatorName: Optional[str] = None
    iqn: Optional[str] = None
    iscsiInterface: Optional[str] = None
    lun: Optional[int] = None
    portals: List[str] = Field(default_factory=list)
    readOnly: Optional[bool] = None
    secretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    targetPortal: Optional[str] = None


class V1GlusterfsPersistentVolumeSource(ResourceValue):
    endpoints: Optional[str] = None
    endpointsNamespace: Optional[str] = None
    path: Optional[str] = None
    readOnly: Optional[bool] = None


class V1FlexPersistentVolumeSource(ResourceValue):
    driver: Optional[str] = None
    fsType: Optional[str] = None
    options: Dict[str, str] = Field(default_factory=dict)
    readOnly: Optional[bool] = None
    secretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())


class V1CSIPersistentVolumeSource(ResourceValue):
    controllerExpandSecretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    controllerPublishSecretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    driver: Optional[str] = None
    fsType: Optional[str] = None
    nodeExpandSecretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    nodePublishSecretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    nodeStageSecretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    readOnly: Optional[bool] = None
    volumeAttributes: Dict[str, str] = Field(default_factory=dict)
    volumeHandle: Optional[str] = None


class V1CinderPersistentVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    volumeID: Optional[str] = None


class V1SecretReference(ResourceValue):
    name: Optional[str] = None
    namespace: Optional[str] = None


class V1CephFSPersistentVolumeSource(ResourceValue):
    monitors: List[str] = Field(default_factory=list)
    path: Optional[str] = None
    readOnly: Optional[bool] = None
    secretFile: Optional[str] = None
    secretRef: V1SecretReference = Field(default_factory=lambda: V1SecretReference())
    user: Optional[str] = None


class V1AzureFilePersistentVolumeSource(ResourceValue):
    readOnly: Optional[bool] = None
    secretName: Optional[str] = None
    secretNamespace: Optional[str] = None
    shareName: Optional[str] = None


class V1PersistentVolumeSpec(ResourceValue):
    accessModes: List[str] = Field(default_factory=list)
    awsElasticBlockStore: V1AWSElasticBlockStoreVolumeSource = Field(
        default_factory=lambda: V1AWSElasticBlockStoreVolumeSource()
    )
    azureDisk: V1AzureDiskVolumeSource = Field(default_factory=lambda: V1AzureDiskVolumeSource())
    azureFile: V1AzureFilePersistentVolumeSource = Field(default_factory=lambda: V1AzureFilePersistentVolumeSource())
    capacity: Dict[str, str] = Field(default_factory=dict)
    cephfs: V1CephFSPersistentVolumeSource = Field(default_factory=lambda: V1CephFSPersistentVolumeSource())
    cinder: V1CinderPersistentVolumeSource = Field(default_factory=lambda: V1CinderPersistentVolumeSource())
    claimRef: V1ObjectReference = Field(default_factory=lambda: V1ObjectReference())
    csi: V1CSIPersistentVolumeSource = Field(default_factory=lambda: V1CSIPersistentVolumeSource())
    fc: V1FCVolumeSource = Field(default_factory=lambda: V1FCVolumeSource())
    flexVolume: V1FlexPersistentVolumeSource = Field(default_factory=lambda: V1FlexPersistentVolumeSource())
    flocker: V1FlockerVolumeSource = Field(default_factory=lambda: V1FlockerVolumeSource())
    gcePersistentDisk: V1GCEPersistentDiskVolumeSource = Field(
        default_factory=lambda: V1GCEPersistentDiskVolumeSource()
    )
    glusterfs: V1GlusterfsPersistentVolumeSource = Field(default_factory=lambda: V1GlusterfsPersistentVolumeSource())
    hostPath: V1HostPathVolumeSource = Field(default_factory=lambda: V1HostPathVolumeSource())
    iscsi: V1ISCSIPersistentVolumeSource = Field(default_factory=lambda: V1ISCSIPersistentVolumeSource())
    local: V1LocalVolumeSource = Field(default_factory=lambda: V1LocalVolumeSource())
    mountOptions: List[str] = Field(default_factory=list)
    nfs: V1NFSVolumeSource = Field(default_factory=lambda: V1NFSVolumeSource())
    nodeAffinity: V1VolumeNodeAffinity = Field(default_factory=lambda: V1VolumeNodeAffinity())
    persistentVolumeReclaimPolicy: Optional[str] = None
    photonPersistentDisk: V1PhotonPersistentDiskVolumeSource = Field(
        default_factory=lambda: V1PhotonPersistentDiskVolumeSource()
    )
    portworxVolume: V1PortworxVolumeSource = Field(default_factory=lambda: V1PortworxVolumeSource())
    quobyte: V1QuobyteVolumeSource = Field(default_factory=lambda: V1QuobyteVolumeSource())
    rbd: V1RBDPersistentVolumeSource = Field(default_factory=lambda: V1RBDPersistentVolumeSource())
    scaleIO: V1ScaleIOPersistentVolumeSource = Field(default_factory=lambda: V1ScaleIOPersistentVolumeSource())
    storageClassName: Optional[str] = None
    storageos: V1StorageOSPersistentVolumeSource = Field(default_factory=lambda: V1StorageOSPersistentVolumeSource())
    volumeMode: Optional[str] = None
    vsphereVolume: V1VsphereVirtualDiskVolumeSource = Field(default_factory=lambda: V1VsphereVirtualDiskVolumeSource())


class V1PersistentVolume(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1PersistentVolumeSpec = Field(default_factory=lambda: V1PersistentVolumeSpec())
    status: V1PersistentVolumeStatus = Field(default_factory=lambda: V1PersistentVolumeStatus())


class V1NodeList(ResourceItem):
    items: List[V1Node] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1AttachedVolume(ResourceValue):
    devicePath: Optional[str] = None
    name: Optional[str] = None


class V1NodeSystemInfo(ResourceValue):
    architecture: Optional[str] = None
    bootID: Optional[str] = None
    containerRuntimeVersion: Optional[str] = None
    kernelVersion: Optional[str] = None
    kubeProxyVersion: Optional[str] = None
    kubeletVersion: Optional[str] = None
    machineID: Optional[str] = None
    operatingSystem: Optional[str] = None
    osImage: Optional[str] = None
    systemUUID: Optional[str] = None


class V1ContainerImage(ResourceValue):
    names: List[str] = Field(default_factory=list)
    sizeBytes: Optional[int] = None


class V1DaemonEndpoint(ResourceValue):
    Port: Optional[int] = None


class V1NodeDaemonEndpoints(ResourceValue):
    kubeletEndpoint: V1DaemonEndpoint = Field(default_factory=lambda: V1DaemonEndpoint())


class V1NodeConfigStatus(ResourceValue):
    active: V1NodeConfigSource = Field(default_factory=lambda: V1NodeConfigSource())
    assigned: V1NodeConfigSource = Field(default_factory=lambda: V1NodeConfigSource())
    error: Optional[str] = None
    lastKnownGood: V1NodeConfigSource = Field(default_factory=lambda: V1NodeConfigSource())


class V1NodeCondition(ResourceValue):
    lastHeartbeatTime: Optional[datetime] = None
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1NodeAddress(ResourceValue):
    address: Optional[str] = None
    type: Optional[str] = None


class V1NodeStatus(ResourceValue):
    addresses: List[V1NodeAddress] = Field(default_factory=list)
    allocatable: Dict[str, str] = Field(default_factory=dict)
    capacity: Dict[str, str] = Field(default_factory=dict)
    conditions: List[V1NodeCondition] = Field(default_factory=list)
    config: V1NodeConfigStatus = Field(default_factory=lambda: V1NodeConfigStatus())
    daemonEndpoints: V1NodeDaemonEndpoints = Field(default_factory=lambda: V1NodeDaemonEndpoints())
    images: List[V1ContainerImage] = Field(default_factory=list)
    nodeInfo: V1NodeSystemInfo = Field(default_factory=lambda: V1NodeSystemInfo())
    phase: Optional[str] = None
    volumesAttached: List[V1AttachedVolume] = Field(default_factory=list)
    volumesInUse: List[str] = Field(default_factory=list)


class V1Taint(ResourceValue):
    effect: Optional[str] = None
    key: Optional[str] = None
    timeAdded: Optional[datetime] = None
    value: Optional[str] = None


class V1ConfigMapNodeConfigSource(ResourceValue):
    kubeletConfigKey: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None
    resourceVersion: Optional[str] = None
    uid: Optional[str] = None


class V1NodeConfigSource(ResourceValue):
    configMap: V1ConfigMapNodeConfigSource = Field(default_factory=lambda: V1ConfigMapNodeConfigSource())


class V1NodeSpec(ResourceValue):
    configSource: V1NodeConfigSource = Field(default_factory=lambda: V1NodeConfigSource())
    externalID: Optional[str] = None
    podCIDR: Optional[str] = None
    podCIDRs: List[str] = Field(default_factory=list)
    providerID: Optional[str] = None
    taints: List[V1Taint] = Field(default_factory=list)
    unschedulable: Optional[bool] = None


class V1Node(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1NodeSpec = Field(default_factory=lambda: V1NodeSpec())
    status: V1NodeStatus = Field(default_factory=lambda: V1NodeStatus())


class V1NetworkPolicyList(ResourceItem):
    items: List[V1NetworkPolicy] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1Condition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    observedGeneration: Optional[int] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1NetworkPolicyStatus(ResourceValue):
    conditions: List[V1Condition] = Field(default_factory=list)


class V1NetworkPolicyIngressRule(ResourceValue):
    ports: List[V1NetworkPolicyPort] = Field(default_factory=list)


class V1IPBlock(ResourceValue):
    cidr: Optional[str] = None


class V1NetworkPolicyPeer(ResourceValue):
    ipBlock: V1IPBlock = Field(default_factory=lambda: V1IPBlock())
    namespaceSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    podSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())


class V1NetworkPolicyPort(ResourceValue):
    endPort: Optional[int] = None
    port: Optional[object] = None
    protocol: Optional[str] = None


class V1NetworkPolicyEgressRule(ResourceValue):
    ports: List[V1NetworkPolicyPort] = Field(default_factory=list)
    to: List[V1NetworkPolicyPeer] = Field(default_factory=list)


class V1NetworkPolicySpec(ResourceValue):
    egress: List[V1NetworkPolicyEgressRule] = Field(default_factory=list)
    ingress: List[V1NetworkPolicyIngressRule] = Field(default_factory=list)
    podSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    policyTypes: List[str] = Field(default_factory=list)


class V1NetworkPolicy(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1NetworkPolicySpec = Field(default_factory=lambda: V1NetworkPolicySpec())
    status: V1NetworkPolicyStatus = Field(default_factory=lambda: V1NetworkPolicyStatus())


class V1NamespaceList(ResourceItem):
    items: List[V1Namespace] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1NamespaceCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1NamespaceStatus(ResourceValue):
    conditions: List[V1NamespaceCondition] = Field(default_factory=list)
    phase: Optional[str] = None


class V1NamespaceSpec(ResourceValue):
    finalizers: List[str] = Field(default_factory=list)


class V1MutatingWebhookConfigurationList(ResourceItem):
    items: List[V1MutatingWebhookConfiguration] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1RuleWithOperations(ResourceValue):
    apiGroups: List[str] = Field(default_factory=list)
    apiVersions: List[str] = Field(default_factory=list)
    operations: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    scope: Optional[str] = None


class AdmissionregistrationV1ServiceReference(ResourceValue):
    name: Optional[str] = None
    namespace: Optional[str] = None
    path: Optional[str] = None
    port: Optional[int] = None


class AdmissionregistrationV1WebhookClientConfig(ResourceValue):
    caBundle: Optional[str] = None
    service: AdmissionregistrationV1ServiceReference = Field(
        default_factory=lambda: AdmissionregistrationV1ServiceReference()
    )
    url: Optional[str] = None


class V1MutatingWebhook(ResourceValue):
    admissionReviewVersions: List[str] = Field(default_factory=list)
    clientConfig: AdmissionregistrationV1WebhookClientConfig = Field(
        default_factory=lambda: AdmissionregistrationV1WebhookClientConfig()
    )
    failurePolicy: Optional[str] = None
    matchPolicy: Optional[str] = None
    name: Optional[str] = None
    namespaceSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    objectSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    reinvocationPolicy: Optional[str] = None
    rules: List[V1RuleWithOperations] = Field(default_factory=list)
    sideEffects: Optional[str] = None
    timeoutSeconds: Optional[int] = None


class V1MutatingWebhookConfiguration(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    webhooks: List[V1MutatingWebhook] = Field(default_factory=list)


class V1SubjectAccessReviewStatus(ResourceValue):
    allowed: Optional[bool] = None
    denied: Optional[bool] = None
    evaluationError: Optional[str] = None
    reason: Optional[str] = None


class V1ResourceAttributes(ResourceValue):
    group: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None
    resource: Optional[str] = None
    subresource: Optional[str] = None
    verb: Optional[str] = None
    version: Optional[str] = None


class V1NonResourceAttributes(ResourceValue):
    path: Optional[str] = None
    verb: Optional[str] = None


class V1SubjectAccessReviewSpec(ResourceValue):
    extra: Dict[str, List[str]] = Field(default_factory=dict)
    groups: List[str] = Field(default_factory=list)
    nonResourceAttributes: V1NonResourceAttributes = Field(default_factory=lambda: V1NonResourceAttributes())
    resourceAttributes: V1ResourceAttributes = Field(default_factory=lambda: V1ResourceAttributes())
    uid: Optional[str] = None
    user: Optional[str] = None


class V1LocalSubjectAccessReview(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1SubjectAccessReviewSpec = Field(default_factory=lambda: V1SubjectAccessReviewSpec())
    status: V1SubjectAccessReviewStatus = Field(default_factory=lambda: V1SubjectAccessReviewStatus())


class V1LimitRangeList(ResourceItem):
    items: List[V1LimitRange] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1LimitRangeItem(ResourceValue):
    default: Dict[str, str] = Field(default_factory=dict)
    defaultRequest: Dict[str, str] = Field(default_factory=dict)
    max: Dict[str, str] = Field(default_factory=dict)
    maxLimitRequestRatio: Dict[str, str] = Field(default_factory=dict)
    min: Dict[str, str] = Field(default_factory=dict)
    type: Optional[str] = None


class V1LimitRangeSpec(ResourceValue):
    limits: List[V1LimitRangeItem] = Field(default_factory=list)


class V1LimitRange(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1LimitRangeSpec = Field(default_factory=lambda: V1LimitRangeSpec())


class V1LeaseList(ResourceItem):
    items: List[V1Lease] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1LeaseSpec(ResourceValue):
    acquireTime: Optional[datetime] = None
    holderIdentity: Optional[str] = None
    leaseDurationSeconds: Optional[int] = None
    leaseTransitions: Optional[int] = None
    renewTime: Optional[datetime] = None


class V1Lease(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1LeaseSpec = Field(default_factory=lambda: V1LeaseSpec())


class V1JobList(ResourceItem):
    items: List[V1Job] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1UncountedTerminatedPods(ResourceValue):
    failed: List[str] = Field(default_factory=list)
    succeeded: List[str] = Field(default_factory=list)


class V1JobCondition(ResourceValue):
    lastProbeTime: Optional[datetime] = None
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1JobStatus(ResourceValue):
    active: Optional[int] = None
    completedIndexes: Optional[str] = None
    completionTime: Optional[datetime] = None
    conditions: List[V1JobCondition] = Field(default_factory=list)
    failed: Optional[int] = None
    ready: Optional[int] = None
    startTime: Optional[datetime] = None
    succeeded: Optional[int] = None
    uncountedTerminatedPods: V1UncountedTerminatedPods = Field(default_factory=lambda: V1UncountedTerminatedPods())


class V1Job(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1JobSpec = Field(default_factory=lambda: V1JobSpec())
    status: V1JobStatus = Field(default_factory=lambda: V1JobStatus())


class V1IngressList(ResourceItem):
    items: List[V1Ingress] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1IngressClassList(ResourceItem):
    items: List[V1IngressClass] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1IngressClassParametersReference(ResourceValue):
    apiGroup: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None
    scope: Optional[str] = None


class V1IngressClassSpec(ResourceValue):
    controller: Optional[str] = None
    parameters: V1IngressClassParametersReference = Field(default_factory=lambda: V1IngressClassParametersReference())


class V1IngressClass(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1IngressClassSpec = Field(default_factory=lambda: V1IngressClassSpec())


class V1IngressPortStatus(ResourceValue):
    error: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[str] = None


class V1IngressLoadBalancerIngress(ResourceValue):
    hostname: Optional[str] = None
    ip: Optional[str] = None
    ports: List[V1IngressPortStatus] = Field(default_factory=list)


class V1IngressLoadBalancerStatus(ResourceValue):
    ingress: List[V1IngressLoadBalancerIngress] = Field(default_factory=list)


class V1IngressStatus(ResourceValue):
    loadBalancer: V1IngressLoadBalancerStatus = Field(default_factory=lambda: V1IngressLoadBalancerStatus())


class V1IngressTLS(ResourceValue):
    hosts: List[str] = Field(default_factory=list)
    secretName: Optional[str] = None


class V1HTTPIngressPath(ResourceValue):
    backend: V1IngressBackend = Field(default_factory=lambda: V1IngressBackend())
    path: Optional[str] = None
    pathType: Optional[str] = None


class V1HTTPIngressRuleValue(ResourceValue):
    paths: List[V1HTTPIngressPath] = Field(default_factory=list)


class V1IngressRule(ResourceValue):
    host: Optional[str] = None
    http: V1HTTPIngressRuleValue = Field(default_factory=lambda: V1HTTPIngressRuleValue())


class V1ServiceBackendPort(ResourceValue):
    name: Optional[str] = None
    number: Optional[int] = None


class V1IngressServiceBackend(ResourceValue):
    name: Optional[str] = None
    port: V1ServiceBackendPort = Field(default_factory=lambda: V1ServiceBackendPort())


class V1IngressBackend(ResourceValue):
    resource: V1TypedLocalObjectReference = Field(default_factory=lambda: V1TypedLocalObjectReference())
    service: V1IngressServiceBackend = Field(default_factory=lambda: V1IngressServiceBackend())


class V1IngressSpec(ResourceValue):
    defaultBackend: V1IngressBackend = Field(default_factory=lambda: V1IngressBackend())
    ingressClassName: Optional[str] = None
    rules: List[V1IngressRule] = Field(default_factory=list)
    tls: List[V1IngressTLS] = Field(default_factory=list)


class V1HorizontalPodAutoscalerList(ResourceItem):
    items: List[V1HorizontalPodAutoscaler] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1HorizontalPodAutoscalerStatus(ResourceValue):
    currentCPUUtilizationPercentage: Optional[int] = None
    currentReplicas: Optional[int] = None
    desiredReplicas: Optional[int] = None
    lastScaleTime: Optional[datetime] = None
    observedGeneration: Optional[int] = None


class V1HorizontalPodAutoscalerSpec(ResourceValue):
    maxReplicas: Optional[int] = None
    minReplicas: Optional[int] = None
    scaleTargetRef: V1CrossVersionObjectReference = Field(default_factory=lambda: V1CrossVersionObjectReference())
    targetCPUUtilizationPercentage: Optional[int] = None


class V1HorizontalPodAutoscaler(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1HorizontalPodAutoscalerSpec = Field(default_factory=lambda: V1HorizontalPodAutoscalerSpec())
    status: V1HorizontalPodAutoscalerStatus = Field(default_factory=lambda: V1HorizontalPodAutoscalerStatus())


class V1Eviction(ResourceItem):
    deleteOptions: V1DeleteOptions = Field(default_factory=lambda: V1DeleteOptions())
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())


class V1EndpointsList(ResourceItem):
    items: List[V1Endpoints] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class CoreV1EndpointPort(ResourceValue):
    appProtocol: Optional[str] = None
    name: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[str] = None


class V1EndpointAddress(ResourceValue):
    hostname: Optional[str] = None
    ip: Optional[str] = None
    nodeName: Optional[str] = None
    targetRef: V1ObjectReference = Field(default_factory=lambda: V1ObjectReference())


class V1EndpointSubset(ResourceValue):
    addresses: List[V1EndpointAddress] = Field(default_factory=list)
    notReadyAddresses: List[V1EndpointAddress] = Field(default_factory=list)
    ports: List[CoreV1EndpointPort] = Field(default_factory=list)


class V1Endpoints(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    subsets: List[V1EndpointSubset] = Field(default_factory=list)


class V1EndpointSliceList(ResourceItem):
    items: List[V1EndpointSlice] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class DiscoveryV1EndpointPort(ResourceValue):
    appProtocol: Optional[str] = None
    name: Optional[str] = None
    port: Optional[int] = None
    protocol: Optional[str] = None


class V1ForZone(ResourceValue):
    name: Optional[str] = None


class V1EndpointHints(ResourceValue):
    forZones: List[V1ForZone] = Field(default_factory=list)


class V1EndpointConditions(ResourceValue):
    ready: Optional[bool] = None
    serving: Optional[bool] = None
    terminating: Optional[bool] = None


class V1Endpoint(ResourceValue):
    addresses: List[str] = Field(default_factory=list)
    conditions: V1EndpointConditions = Field(default_factory=lambda: V1EndpointConditions())
    deprecatedTopology: Dict[str, str] = Field(default_factory=dict)
    hints: V1EndpointHints = Field(default_factory=lambda: V1EndpointHints())
    hostname: Optional[str] = None
    nodeName: Optional[str] = None
    targetRef: V1ObjectReference = Field(default_factory=lambda: V1ObjectReference())
    zone: Optional[str] = None


class V1EndpointSlice(ResourceItem):
    addressType: Optional[str] = None
    endpoints: List[V1Endpoint] = Field(default_factory=list)
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    ports: List[DiscoveryV1EndpointPort] = Field(default_factory=list)


class V1DeploymentList(ResourceItem):
    items: List[V1Deployment] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1DeploymentCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    lastUpdateTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1DeploymentStatus(ResourceValue):
    availableReplicas: Optional[int] = None
    collisionCount: Optional[int] = None
    conditions: List[V1DeploymentCondition] = Field(default_factory=list)
    observedGeneration: Optional[int] = None
    readyReplicas: Optional[int] = None
    replicas: Optional[int] = None
    unavailableReplicas: Optional[int] = None
    updatedReplicas: Optional[int] = None


class V1RollingUpdateDeployment(ResourceValue):
    maxSurge: Optional[object] = None
    maxUnavailable: Optional[object] = None


class V1DeploymentStrategy(ResourceValue):
    rollingUpdate: V1RollingUpdateDeployment = Field(default_factory=lambda: V1RollingUpdateDeployment())
    type: Optional[str] = None


class V1DeploymentSpec(ResourceValue):
    minReadySeconds: Optional[int] = None
    paused: Optional[bool] = None
    progressDeadlineSeconds: Optional[int] = None
    replicas: Optional[int] = None
    revisionHistoryLimit: Optional[int] = None
    selector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    strategy: V1DeploymentStrategy = Field(default_factory=lambda: V1DeploymentStrategy())
    template: V1PodTemplateSpec = Field(default_factory=lambda: V1PodTemplateSpec())


class V1Deployment(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1DeploymentSpec = Field(default_factory=lambda: V1DeploymentSpec())
    status: V1DeploymentStatus = Field(default_factory=lambda: V1DeploymentStatus())


class V1Preconditions(ResourceValue):
    resourceVersion: Optional[str] = None
    uid: Optional[str] = None


class V1DeleteOptions(ResourceItem):
    dryRun: List[str] = Field(default_factory=list)
    gracePeriodSeconds: Optional[int] = None
    orphanDependents: Optional[bool] = None
    preconditions: V1Preconditions = Field(default_factory=lambda: V1Preconditions())
    propagationPolicy: Optional[str] = None


class V1DaemonSetList(ResourceItem):
    items: List[V1DaemonSet] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1DaemonSetCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1DaemonSetStatus(ResourceValue):
    collisionCount: Optional[int] = None
    conditions: List[V1DaemonSetCondition] = Field(default_factory=list)
    currentNumberScheduled: Optional[int] = None
    desiredNumberScheduled: Optional[int] = None
    numberAvailable: Optional[int] = None
    numberMisscheduled: Optional[int] = None
    numberReady: Optional[int] = None
    numberUnavailable: Optional[int] = None
    observedGeneration: Optional[int] = None
    updatedNumberScheduled: Optional[int] = None


class V1RollingUpdateDaemonSet(ResourceValue):
    maxSurge: Optional[object] = None
    maxUnavailable: Optional[object] = None


class V1DaemonSetUpdateStrategy(ResourceValue):
    rollingUpdate: V1RollingUpdateDaemonSet = Field(default_factory=lambda: V1RollingUpdateDaemonSet())
    type: Optional[str] = None


class V1DaemonSetSpec(ResourceValue):
    minReadySeconds: Optional[int] = None
    revisionHistoryLimit: Optional[int] = None
    selector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    template: V1PodTemplateSpec = Field(default_factory=lambda: V1PodTemplateSpec())
    updateStrategy: V1DaemonSetUpdateStrategy = Field(default_factory=lambda: V1DaemonSetUpdateStrategy())


class V1DaemonSet(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1DaemonSetSpec = Field(default_factory=lambda: V1DaemonSetSpec())
    status: V1DaemonSetStatus = Field(default_factory=lambda: V1DaemonSetStatus())


class V1CustomResourceDefinitionList(ResourceItem):
    items: List[V1CustomResourceDefinition] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1CustomResourceDefinitionCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1CustomResourceDefinitionStatus(ResourceValue):
    acceptedNames: V1CustomResourceDefinitionNames = Field(default_factory=lambda: V1CustomResourceDefinitionNames())
    conditions: List[V1CustomResourceDefinitionCondition] = Field(default_factory=list)
    storedVersions: List[str] = Field(default_factory=list)


class V1CustomResourceSubresourceScale(ResourceValue):
    labelSelectorPath: Optional[str] = None
    specReplicasPath: Optional[str] = None
    statusReplicasPath: Optional[str] = None


class V1CustomResourceSubresources(ResourceValue):
    scale: V1CustomResourceSubresourceScale = Field(default_factory=lambda: V1CustomResourceSubresourceScale())
    status: Optional[object] = None


class V1ExternalDocumentation(ResourceValue):
    description: Optional[str] = None
    url: Optional[str] = None


class V1JSONSchemaProps(ResourceValue):
    additionalItems: Optional[object] = None
    additionalProperties: Optional[object] = None
    allOf: List[V1JSONSchemaProps] = Field(default_factory=list)
    anyOf: List[V1JSONSchemaProps] = Field(default_factory=list)
    default: Optional[object] = None
    definitions: Dict[str, V1JSONSchemaProps] = Field(default_factory=dict)
    dependencies: Dict[str, object] = Field(default_factory=dict)
    description: Optional[str] = None
    enum: List[object] = Field(default_factory=list)
    example: Optional[object] = None
    exclusiveMaximum: Optional[bool] = None
    exclusiveMinimum: Optional[bool] = None
    externalDocs: V1ExternalDocumentation = Field(default_factory=lambda: V1ExternalDocumentation())
    format: Optional[str] = None
    id: Optional[str] = None
    items: Union[V1JSONSchemaProps, List[V1JSONSchemaProps]] = Field(default_factory=list)
    maxItems: Optional[int] = None
    maxLength: Optional[int] = None
    maxProperties: Optional[int] = None
    maximum: Optional[float] = None
    minItems: Optional[int] = None
    minLength: Optional[int] = None
    minProperties: Optional[int] = None
    minimum: Optional[float] = None
    multipleOf: Optional[float] = None
    nullable: Optional[bool] = None
    oneOf: List[V1JSONSchemaProps] = Field(default_factory=list)
    pattern: Optional[str] = None
    patternProperties: Dict[str, V1JSONSchemaProps] = Field(default_factory=dict)
    properties: Dict[str, V1JSONSchemaProps] = Field(default_factory=dict)
    required: List[str] = Field(default_factory=list)
    title: Optional[str] = None
    type: Optional[str] = None
    uniqueItems: Optional[bool] = None


class V1CustomResourceValidation(ResourceValue):
    openAPIV3Schema: V1JSONSchemaProps = Field(default_factory=lambda: V1JSONSchemaProps())


class V1CustomResourceColumnDefinition(ResourceValue):
    description: Optional[str] = None
    format: Optional[str] = None
    jsonPath: Optional[str] = None
    name: Optional[str] = None
    priority: Optional[int] = None
    type: Optional[str] = None


class V1CustomResourceDefinitionVersion(ResourceValue):
    additionalPrinterColumns: List[V1CustomResourceColumnDefinition] = Field(default_factory=list)
    deprecated: Optional[bool] = None
    deprecationWarning: Optional[str] = None
    name: Optional[str] = None
    v1schema: V1CustomResourceValidation = Field(alias="schema")
    served: Optional[bool] = None
    storage: Optional[bool] = None
    subresources: V1CustomResourceSubresources = Field(default_factory=lambda: V1CustomResourceSubresources())


class V1CustomResourceDefinitionNames(ResourceValue):
    categories: List[str] = Field(default_factory=list)
    kind: Optional[str] = None
    listKind: Optional[str] = None
    plural: Optional[str] = None
    shortNames: List[str] = Field(default_factory=list)
    singular: Optional[str] = None


class ApiextensionsV1ServiceReference(ResourceValue):
    name: Optional[str] = None
    namespace: Optional[str] = None
    path: Optional[str] = None
    port: Optional[int] = None


class ApiextensionsV1WebhookClientConfig(ResourceValue):
    caBundle: Optional[str] = None
    service: ApiextensionsV1ServiceReference = Field(default_factory=lambda: ApiextensionsV1ServiceReference())
    url: Optional[str] = None


class V1WebhookConversion(ResourceValue):
    clientConfig: ApiextensionsV1WebhookClientConfig = Field(
        default_factory=lambda: ApiextensionsV1WebhookClientConfig()
    )
    conversionReviewVersions: List[str] = Field(default_factory=list)


class V1CustomResourceConversion(ResourceValue):
    strategy: Optional[str] = None
    webhook: V1WebhookConversion = Field(default_factory=lambda: V1WebhookConversion())


class V1CustomResourceDefinitionSpec(ResourceValue):
    conversion: V1CustomResourceConversion = Field(default_factory=lambda: V1CustomResourceConversion())
    group: Optional[str] = None
    names: V1CustomResourceDefinitionNames = Field(default_factory=lambda: V1CustomResourceDefinitionNames())
    preserveUnknownFields: Optional[bool] = None
    scope: Optional[str] = None
    versions: List[V1CustomResourceDefinitionVersion] = Field(default_factory=list)


class V1CustomResourceDefinition(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1CustomResourceDefinitionSpec = Field(default_factory=lambda: V1CustomResourceDefinitionSpec())
    status: V1CustomResourceDefinitionStatus = Field(default_factory=lambda: V1CustomResourceDefinitionStatus())


class V1CrossVersionObjectReference(ResourceItem):
    name: Optional[str] = None


class V1CronJobList(ResourceItem):
    items: List[V1CronJob] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1CronJobStatus(ResourceValue):
    active: List[V1ObjectReference] = Field(default_factory=list)
    lastScheduleTime: Optional[datetime] = None
    lastSuccessfulTime: Optional[datetime] = None


class V1VsphereVirtualDiskVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    storagePolicyID: Optional[str] = None
    storagePolicyName: Optional[str] = None
    volumePath: Optional[str] = None


class V1StorageOSVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: V1LocalObjectReference = Field(default_factory=lambda: V1LocalObjectReference())
    volumeName: Optional[str] = None
    volumeNamespace: Optional[str] = None


class V1SecretVolumeSource(ResourceValue):
    defaultMode: Optional[int] = None
    items: List[V1KeyToPath] = Field(default_factory=list)
    optional: Optional[bool] = None
    secretName: Optional[str] = None


class V1ScaleIOVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    gateway: Optional[str] = None
    protectionDomain: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: V1LocalObjectReference = Field(default_factory=lambda: V1LocalObjectReference())
    sslEnabled: Optional[bool] = None
    storageMode: Optional[str] = None
    storagePool: Optional[str] = None
    system: Optional[str] = None
    volumeName: Optional[str] = None


class V1RBDVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    image: Optional[str] = None
    keyring: Optional[str] = None
    monitors: List[str] = Field(default_factory=list)
    pool: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: V1LocalObjectReference = Field(default_factory=lambda: V1LocalObjectReference())
    user: Optional[str] = None


class V1QuobyteVolumeSource(ResourceValue):
    group: Optional[str] = None
    readOnly: Optional[bool] = None
    registry: Optional[str] = None
    tenant: Optional[str] = None
    user: Optional[str] = None
    volume: Optional[str] = None


class V1ServiceAccountTokenProjection(ResourceValue):
    audience: Optional[str] = None
    expirationSeconds: Optional[int] = None
    path: Optional[str] = None


class V1SecretProjection(ResourceValue):
    items: List[V1KeyToPath] = Field(default_factory=list)
    name: Optional[str] = None
    optional: Optional[bool] = None


class V1DownwardAPIProjection(ResourceValue):
    items: List[V1DownwardAPIVolumeFile] = Field(default_factory=list)


class V1ConfigMapProjection(ResourceValue):
    items: List[V1KeyToPath] = Field(default_factory=list)
    name: Optional[str] = None
    optional: Optional[bool] = None


class V1VolumeProjection(ResourceValue):
    configMap: V1ConfigMapProjection = Field(default_factory=lambda: V1ConfigMapProjection())
    downwardAPI: V1DownwardAPIProjection = Field(default_factory=lambda: V1DownwardAPIProjection())
    secret: V1SecretProjection = Field(default_factory=lambda: V1SecretProjection())
    serviceAccountToken: V1ServiceAccountTokenProjection = Field(
        default_factory=lambda: V1ServiceAccountTokenProjection()
    )


class V1ProjectedVolumeSource(ResourceValue):
    defaultMode: Optional[int] = None
    sources: List[V1VolumeProjection] = Field(default_factory=list)


class V1PortworxVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    volumeID: Optional[str] = None


class V1PhotonPersistentDiskVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    pdID: Optional[str] = None


class V1PersistentVolumeClaimVolumeSource(ResourceValue):
    claimName: Optional[str] = None
    readOnly: Optional[bool] = None


class V1NFSVolumeSource(ResourceValue):
    path: Optional[str] = None
    readOnly: Optional[bool] = None
    server: Optional[str] = None


class V1ISCSIVolumeSource(ResourceValue):
    chapAuthDiscovery: Optional[bool] = None
    chapAuthSession: Optional[bool] = None
    fsType: Optional[str] = None
    initiatorName: Optional[str] = None
    iqn: Optional[str] = None
    iscsiInterface: Optional[str] = None
    lun: Optional[int] = None
    portals: List[str] = Field(default_factory=list)
    readOnly: Optional[bool] = None
    secretRef: V1LocalObjectReference = Field(default_factory=lambda: V1LocalObjectReference())
    targetPortal: Optional[str] = None


class V1HostPathVolumeSource(ResourceValue):
    path: Optional[str] = None
    type: Optional[str] = None


class V1GlusterfsVolumeSource(ResourceValue):
    endpoints: Optional[str] = None
    path: Optional[str] = None
    readOnly: Optional[bool] = None


class V1GitRepoVolumeSource(ResourceValue):
    directory: Optional[str] = None
    repository: Optional[str] = None
    revision: Optional[str] = None


class V1GCEPersistentDiskVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    partition: Optional[int] = None
    pdName: Optional[str] = None
    readOnly: Optional[bool] = None


class V1FlockerVolumeSource(ResourceValue):
    datasetName: Optional[str] = None
    datasetUUID: Optional[str] = None


class V1FlexVolumeSource(ResourceValue):
    driver: Optional[str] = None
    fsType: Optional[str] = None
    options: Dict[str, str] = Field(default_factory=dict)
    readOnly: Optional[bool] = None
    secretRef: V1LocalObjectReference = Field(default_factory=lambda: V1LocalObjectReference())


class V1FCVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    lun: Optional[int] = None
    readOnly: Optional[bool] = None
    targetWWNs: List[str] = Field(default_factory=list)
    wwids: List[str] = Field(default_factory=list)


class V1TypedObjectReference(ResourceValue):
    apiGroup: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None


class V1TypedLocalObjectReference(ResourceValue):
    apiGroup: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None


class V1PersistentVolumeClaimSpec(ResourceValue):
    accessModes: List[str] = Field(default_factory=list)
    dataSource: V1TypedLocalObjectReference = Field(default_factory=lambda: V1TypedLocalObjectReference())
    dataSourceRef: V1TypedObjectReference = Field(default_factory=lambda: V1TypedObjectReference())
    resources: V1ResourceRequirements = Field(default_factory=lambda: V1ResourceRequirements())
    selector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    storageClassName: Optional[str] = None
    volumeMode: Optional[str] = None
    volumeName: Optional[str] = None


class V1PersistentVolumeClaimTemplate(ResourceValue):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1PersistentVolumeClaimSpec = Field(default_factory=lambda: V1PersistentVolumeClaimSpec())


class V1EphemeralVolumeSource(ResourceValue):
    volumeClaimTemplate: V1PersistentVolumeClaimTemplate = Field(
        default_factory=lambda: V1PersistentVolumeClaimTemplate()
    )


class V1EmptyDirVolumeSource(ResourceValue):
    medium: Optional[str] = None
    sizeLimit: Optional[str] = None


class V1DownwardAPIVolumeFile(ResourceValue):
    fieldRef: V1ObjectFieldSelector = Field(default_factory=lambda: V1ObjectFieldSelector())
    mode: Optional[int] = None
    path: Optional[str] = None
    resourceFieldRef: V1ResourceFieldSelector = Field(default_factory=lambda: V1ResourceFieldSelector())


class V1DownwardAPIVolumeSource(ResourceValue):
    defaultMode: Optional[int] = None
    items: List[V1DownwardAPIVolumeFile] = Field(default_factory=list)


class V1CSIVolumeSource(ResourceValue):
    driver: Optional[str] = None
    fsType: Optional[str] = None
    nodePublishSecretRef: V1LocalObjectReference = Field(default_factory=lambda: V1LocalObjectReference())
    readOnly: Optional[bool] = None
    volumeAttributes: Dict[str, str] = Field(default_factory=dict)


class V1KeyToPath(ResourceValue):
    key: Optional[str] = None
    mode: Optional[int] = None
    path: Optional[str] = None


class V1ConfigMapVolumeSource(ResourceValue):
    defaultMode: Optional[int] = None
    items: List[V1KeyToPath] = Field(default_factory=list)
    name: Optional[str] = None
    optional: Optional[bool] = None


class V1CinderVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    readOnly: Optional[bool] = None
    secretRef: V1LocalObjectReference = Field(default_factory=lambda: V1LocalObjectReference())
    volumeID: Optional[str] = None


class V1CephFSVolumeSource(ResourceValue):
    monitors: List[str] = Field(default_factory=list)
    path: Optional[str] = None
    readOnly: Optional[bool] = None
    secretFile: Optional[str] = None
    secretRef: V1LocalObjectReference = Field(default_factory=lambda: V1LocalObjectReference())
    user: Optional[str] = None


class V1AzureFileVolumeSource(ResourceValue):
    readOnly: Optional[bool] = None
    secretName: Optional[str] = None
    shareName: Optional[str] = None


class V1AzureDiskVolumeSource(ResourceValue):
    cachingMode: Optional[str] = None
    diskName: Optional[str] = None
    diskURI: Optional[str] = None
    fsType: Optional[str] = None
    kind: Optional[str] = None
    readOnly: Optional[bool] = None


class V1AWSElasticBlockStoreVolumeSource(ResourceValue):
    fsType: Optional[str] = None
    partition: Optional[int] = None
    readOnly: Optional[bool] = None
    volumeID: Optional[str] = None


class V1Volume(ResourceValue):
    awsElasticBlockStore: V1AWSElasticBlockStoreVolumeSource = Field(
        default_factory=lambda: V1AWSElasticBlockStoreVolumeSource()
    )
    azureDisk: V1AzureDiskVolumeSource = Field(default_factory=lambda: V1AzureDiskVolumeSource())
    azureFile: V1AzureFileVolumeSource = Field(default_factory=lambda: V1AzureFileVolumeSource())
    cephfs: V1CephFSVolumeSource = Field(default_factory=lambda: V1CephFSVolumeSource())
    cinder: V1CinderVolumeSource = Field(default_factory=lambda: V1CinderVolumeSource())
    configMap: V1ConfigMapVolumeSource = Field(default_factory=lambda: V1ConfigMapVolumeSource())
    csi: V1CSIVolumeSource = Field(default_factory=lambda: V1CSIVolumeSource())
    downwardAPI: V1DownwardAPIVolumeSource = Field(default_factory=lambda: V1DownwardAPIVolumeSource())
    emptyDir: V1EmptyDirVolumeSource = Field(default_factory=lambda: V1EmptyDirVolumeSource())
    ephemeral: V1EphemeralVolumeSource = Field(default_factory=lambda: V1EphemeralVolumeSource())
    fc: V1FCVolumeSource = Field(default_factory=lambda: V1FCVolumeSource())
    flexVolume: V1FlexVolumeSource = Field(default_factory=lambda: V1FlexVolumeSource())
    flocker: V1FlockerVolumeSource = Field(default_factory=lambda: V1FlockerVolumeSource())
    gcePersistentDisk: V1GCEPersistentDiskVolumeSource = Field(
        default_factory=lambda: V1GCEPersistentDiskVolumeSource()
    )
    gitRepo: V1GitRepoVolumeSource = Field(default_factory=lambda: V1GitRepoVolumeSource())
    glusterfs: V1GlusterfsVolumeSource = Field(default_factory=lambda: V1GlusterfsVolumeSource())
    hostPath: V1HostPathVolumeSource = Field(default_factory=lambda: V1HostPathVolumeSource())
    iscsi: V1ISCSIVolumeSource = Field(default_factory=lambda: V1ISCSIVolumeSource())
    name: Optional[str] = None
    nfs: V1NFSVolumeSource = Field(default_factory=lambda: V1NFSVolumeSource())
    persistentVolumeClaim: V1PersistentVolumeClaimVolumeSource = Field(
        default_factory=lambda: V1PersistentVolumeClaimVolumeSource()
    )
    photonPersistentDisk: V1PhotonPersistentDiskVolumeSource = Field(
        default_factory=lambda: V1PhotonPersistentDiskVolumeSource()
    )
    portworxVolume: V1PortworxVolumeSource = Field(default_factory=lambda: V1PortworxVolumeSource())
    projected: V1ProjectedVolumeSource = Field(default_factory=lambda: V1ProjectedVolumeSource())
    quobyte: V1QuobyteVolumeSource = Field(default_factory=lambda: V1QuobyteVolumeSource())
    rbd: V1RBDVolumeSource = Field(default_factory=lambda: V1RBDVolumeSource())
    scaleIO: V1ScaleIOVolumeSource = Field(default_factory=lambda: V1ScaleIOVolumeSource())
    secret: V1SecretVolumeSource = Field(default_factory=lambda: V1SecretVolumeSource())
    storageos: V1StorageOSVolumeSource = Field(default_factory=lambda: V1StorageOSVolumeSource())
    vsphereVolume: V1VsphereVirtualDiskVolumeSource = Field(default_factory=lambda: V1VsphereVirtualDiskVolumeSource())


class V1TopologySpreadConstraint(ResourceValue):
    labelSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    matchLabelKeys: List[str] = Field(default_factory=list)
    maxSkew: Optional[int] = None
    minDomains: Optional[int] = None
    nodeAffinityPolicy: Optional[str] = None
    nodeTaintsPolicy: Optional[str] = None
    topologyKey: Optional[str] = None
    whenUnsatisfiable: Optional[str] = None


class V1Toleration(ResourceValue):
    effect: Optional[str] = None
    key: Optional[str] = None
    operator: Optional[str] = None
    tolerationSeconds: Optional[int] = None
    value: Optional[str] = None


class V1Sysctl(ResourceValue):
    name: Optional[str] = None
    value: Optional[str] = None


class V1PodSecurityContext(ResourceValue):
    fsGroup: Optional[int] = None
    fsGroupChangePolicy: Optional[str] = None
    runAsGroup: Optional[int] = None
    runAsNonRoot: Optional[bool] = None
    runAsUser: Optional[int] = None
    seLinuxOptions: V1SELinuxOptions = Field(default_factory=lambda: V1SELinuxOptions())
    seccompProfile: V1SeccompProfile = Field(default_factory=lambda: V1SeccompProfile())
    supplementalGroups: List[int] = Field(default_factory=list)
    sysctls: List[V1Sysctl] = Field(default_factory=list)
    windowsOptions: V1WindowsSecurityContextOptions = Field(default_factory=lambda: V1WindowsSecurityContextOptions())


class V1PodSchedulingGate(ResourceValue):
    name: Optional[str] = None


class V1ClaimSource(ResourceValue):
    resourceClaimName: Optional[str] = None
    resourceClaimTemplateName: Optional[str] = None


class V1PodResourceClaim(ResourceValue):
    name: Optional[str] = None
    source: V1ClaimSource = Field(default_factory=lambda: V1ClaimSource())


class V1PodReadinessGate(ResourceValue):
    conditionType: Optional[str] = None


class V1PodOS(ResourceValue):
    name: Optional[str] = None


class V1LocalObjectReference(ResourceValue):
    name: Optional[str] = None


class V1HostAlias(ResourceValue):
    hostnames: List[str] = Field(default_factory=list)
    ip: Optional[str] = None


class V1EphemeralContainer(ResourceValue):
    args: List[str] = Field(default_factory=list)
    command: List[str] = Field(default_factory=list)
    env: List[V1EnvVar] = Field(default_factory=list)
    envFrom: List[V1EnvFromSource] = Field(default_factory=list)
    image: Optional[str] = None
    imagePullPolicy: Optional[str] = None
    lifecycle: V1Lifecycle = Field(default_factory=lambda: V1Lifecycle())
    livenessProbe: V1Probe = Field(default_factory=lambda: V1Probe())
    name: Optional[str] = None
    ports: List[V1ContainerPort] = Field(default_factory=list)
    readinessProbe: V1Probe = Field(default_factory=lambda: V1Probe())
    resources: V1ResourceRequirements = Field(default_factory=lambda: V1ResourceRequirements())
    securityContext: V1SecurityContext = Field(default_factory=lambda: V1SecurityContext())
    startupProbe: V1Probe = Field(default_factory=lambda: V1Probe())
    stdin: Optional[bool] = None
    stdinOnce: Optional[bool] = None
    targetContainerName: Optional[str] = None
    terminationMessagePath: Optional[str] = None
    terminationMessagePolicy: Optional[str] = None
    tty: Optional[bool] = None
    volumeDevices: List[V1VolumeDevice] = Field(default_factory=list)
    volumeMounts: List[V1VolumeMount] = Field(default_factory=list)
    workingDir: Optional[str] = None


class V1PodDNSConfigOption(ResourceValue):
    name: Optional[str] = None
    value: Optional[str] = None


class V1PodDNSConfig(ResourceValue):
    nameservers: List[str] = Field(default_factory=list)
    options: List[V1PodDNSConfigOption] = Field(default_factory=list)
    searches: List[str] = Field(default_factory=list)


class V1VolumeMount(ResourceValue):
    mountPath: Optional[str] = None
    mountPropagation: Optional[str] = None
    name: Optional[str] = None
    readOnly: Optional[bool] = None
    subPath: Optional[str] = None
    subPathExpr: Optional[str] = None


class V1VolumeDevice(ResourceValue):
    devicePath: Optional[str] = None
    name: Optional[str] = None


class V1WindowsSecurityContextOptions(ResourceValue):
    gmsaCredentialSpec: Optional[str] = None
    gmsaCredentialSpecName: Optional[str] = None
    hostProcess: Optional[bool] = None
    runAsUserName: Optional[str] = None


class V1SeccompProfile(ResourceValue):
    localhostProfile: Optional[str] = None
    type: Optional[str] = None


class V1SELinuxOptions(ResourceValue):
    level: Optional[str] = None
    role: Optional[str] = None
    type: Optional[str] = None
    user: Optional[str] = None


class V1Capabilities(ResourceValue):
    add: List[str] = Field(default_factory=list)
    drop: List[str] = Field(default_factory=list)


class V1SecurityContext(ResourceValue):
    allowPrivilegeEscalation: Optional[bool] = None
    capabilities: V1Capabilities = Field(default_factory=lambda: V1Capabilities())
    privileged: Optional[bool] = None
    procMount: Optional[str] = None
    readOnlyRootFilesystem: Optional[bool] = None
    runAsGroup: Optional[int] = None
    runAsNonRoot: Optional[bool] = None
    runAsUser: Optional[int] = None
    seLinuxOptions: V1SELinuxOptions = Field(default_factory=lambda: V1SELinuxOptions())
    seccompProfile: V1SeccompProfile = Field(default_factory=lambda: V1SeccompProfile())
    windowsOptions: V1WindowsSecurityContextOptions = Field(default_factory=lambda: V1WindowsSecurityContextOptions())


class V1ResourceClaim(ResourceValue):
    name: Optional[str] = None


class V1ResourceRequirements(ResourceValue):
    claims: List[V1ResourceClaim] = Field(default_factory=list)
    limits: Dict[str, str] = Field(default_factory=dict)
    requests: Dict[str, str] = Field(default_factory=dict)


class V1ContainerPort(ResourceValue):
    containerPort: Optional[int] = None
    hostIP: Optional[str] = None
    hostPort: Optional[int] = None
    name: Optional[str] = None
    protocol: Optional[str] = None


class V1GRPCAction(ResourceValue):
    port: Optional[int] = None
    service: Optional[str] = None


class V1Probe(ResourceValue):
    exec: V1ExecAction = Field(default_factory=lambda: V1ExecAction())
    failureThreshold: Optional[int] = None
    grpc: V1GRPCAction = Field(default_factory=lambda: V1GRPCAction())
    httpGet: V1HTTPGetAction = Field(default_factory=lambda: V1HTTPGetAction())
    initialDelaySeconds: Optional[int] = None
    periodSeconds: Optional[int] = None
    successThreshold: Optional[int] = None
    tcpSocket: V1TCPSocketAction = Field(default_factory=lambda: V1TCPSocketAction())
    terminationGracePeriodSeconds: Optional[int] = None
    timeoutSeconds: Optional[int] = None


class V1TCPSocketAction(ResourceValue):
    host: Optional[str] = None
    port: Optional[object] = None


class V1HTTPHeader(ResourceValue):
    name: Optional[str] = None
    value: Optional[str] = None


class V1HTTPGetAction(ResourceValue):
    host: Optional[str] = None
    httpHeaders: List[V1HTTPHeader] = Field(default_factory=list)
    path: Optional[str] = None
    port: Optional[object] = None
    scheme: Optional[str] = None


class V1ExecAction(ResourceValue):
    command: List[str] = Field(default_factory=list)


class V1LifecycleHandler(ResourceValue):
    exec: V1ExecAction = Field(default_factory=lambda: V1ExecAction())
    httpGet: V1HTTPGetAction = Field(default_factory=lambda: V1HTTPGetAction())
    tcpSocket: V1TCPSocketAction = Field(default_factory=lambda: V1TCPSocketAction())


class V1Lifecycle(ResourceValue):
    postStart: V1LifecycleHandler = Field(default_factory=lambda: V1LifecycleHandler())
    preStop: V1LifecycleHandler = Field(default_factory=lambda: V1LifecycleHandler())


class V1SecretEnvSource(ResourceValue):
    name: Optional[str] = None
    optional: Optional[bool] = None


class V1ConfigMapEnvSource(ResourceValue):
    name: Optional[str] = None
    optional: Optional[bool] = None


class V1EnvFromSource(ResourceValue):
    configMapRef: V1ConfigMapEnvSource = Field(default_factory=lambda: V1ConfigMapEnvSource())
    prefix: Optional[str] = None
    secretRef: V1SecretEnvSource = Field(default_factory=lambda: V1SecretEnvSource())


class V1SecretKeySelector(ResourceValue):
    key: Optional[str] = None
    name: Optional[str] = None
    optional: Optional[bool] = None


class V1ResourceFieldSelector(ResourceValue):
    containerName: Optional[str] = None
    divisor: Optional[str] = None
    resource: Optional[str] = None


class V1ObjectFieldSelector(ResourceValue):
    apiVersion: Optional[str] = None
    fieldPath: Optional[str] = None


class V1ConfigMapKeySelector(ResourceValue):
    key: Optional[str] = None
    name: Optional[str] = None
    optional: Optional[bool] = None


class V1EnvVarSource(ResourceValue):
    configMapKeyRef: V1ConfigMapKeySelector = Field(default_factory=lambda: V1ConfigMapKeySelector())
    fieldRef: V1ObjectFieldSelector = Field(default_factory=lambda: V1ObjectFieldSelector())
    resourceFieldRef: V1ResourceFieldSelector = Field(default_factory=lambda: V1ResourceFieldSelector())
    secretKeyRef: V1SecretKeySelector = Field(default_factory=lambda: V1SecretKeySelector())


class V1EnvVar(ResourceValue):
    name: Optional[str] = None
    value: Optional[str] = None
    valueFrom: V1EnvVarSource = Field(default_factory=lambda: V1EnvVarSource())


class V1Container(ResourceValue):
    args: List[str] = Field(default_factory=list)
    command: List[str] = Field(default_factory=list)
    env: List[V1EnvVar] = Field(default_factory=list)
    envFrom: List[V1EnvFromSource] = Field(default_factory=list)
    image: Optional[str] = None
    imagePullPolicy: Optional[str] = None
    lifecycle: V1Lifecycle = Field(default_factory=lambda: V1Lifecycle())
    livenessProbe: V1Probe = Field(default_factory=lambda: V1Probe())
    name: Optional[str] = None
    ports: List[V1ContainerPort] = Field(default_factory=list)
    readinessProbe: V1Probe = Field(default_factory=lambda: V1Probe())
    resources: V1ResourceRequirements = Field(default_factory=lambda: V1ResourceRequirements())
    securityContext: V1SecurityContext = Field(default_factory=lambda: V1SecurityContext())
    startupProbe: V1Probe = Field(default_factory=lambda: V1Probe())
    stdin: Optional[bool] = None
    stdinOnce: Optional[bool] = None
    terminationMessagePath: Optional[str] = None
    terminationMessagePolicy: Optional[str] = None
    tty: Optional[bool] = None
    volumeDevices: List[V1VolumeDevice] = Field(default_factory=list)
    volumeMounts: List[V1VolumeMount] = Field(default_factory=list)
    workingDir: Optional[str] = None


class V1PodAntiAffinity(ResourceValue):
    preferredDuringSchedulingIgnoredDuringExecution: List[V1WeightedPodAffinityTerm] = Field(default_factory=list)
    requiredDuringSchedulingIgnoredDuringExecution: List[V1PodAffinityTerm] = Field(default_factory=list)


class V1PodAffinityTerm(ResourceValue):
    labelSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    namespaceSelector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    namespaces: List[str] = Field(default_factory=list)
    topologyKey: Optional[str] = None


class V1WeightedPodAffinityTerm(ResourceValue):
    podAffinityTerm: V1PodAffinityTerm = Field(default_factory=lambda: V1PodAffinityTerm())
    weight: Optional[int] = None


class V1PodAffinity(ResourceValue):
    preferredDuringSchedulingIgnoredDuringExecution: List[V1WeightedPodAffinityTerm] = Field(default_factory=list)
    requiredDuringSchedulingIgnoredDuringExecution: List[V1PodAffinityTerm] = Field(default_factory=list)


class V1NodeSelector(ResourceValue):
    nodeSelectorTerms: List[V1NodeSelectorTerm] = Field(default_factory=list)


class V1NodeSelectorRequirement(ResourceValue):
    key: Optional[str] = None
    operator: Optional[str] = None
    values: List[str] = Field(default_factory=list)


class V1NodeSelectorTerm(ResourceValue):
    matchExpressions: List[V1NodeSelectorRequirement] = Field(default_factory=list)
    matchFields: List[V1NodeSelectorRequirement] = Field(default_factory=list)


class V1PreferredSchedulingTerm(ResourceValue):
    preference: V1NodeSelectorTerm = Field(default_factory=lambda: V1NodeSelectorTerm())
    weight: Optional[int] = None


class V1NodeAffinity(ResourceValue):
    preferredDuringSchedulingIgnoredDuringExecution: List[V1PreferredSchedulingTerm] = Field(default_factory=list)
    requiredDuringSchedulingIgnoredDuringExecution: V1NodeSelector = Field(default_factory=lambda: V1NodeSelector())


class V1Affinity(ResourceValue):
    nodeAffinity: V1NodeAffinity = Field(default_factory=lambda: V1NodeAffinity())
    podAffinity: V1PodAffinity = Field(default_factory=lambda: V1PodAffinity())
    podAntiAffinity: V1PodAntiAffinity = Field(default_factory=lambda: V1PodAntiAffinity())


class V1PodSpec(ResourceValue):
    activeDeadlineSeconds: Optional[int] = None
    affinity: V1Affinity = Field(default_factory=lambda: V1Affinity())
    automountServiceAccountToken: Optional[bool] = None
    containers: List[V1Container] = Field(default_factory=list)
    dnsConfig: V1PodDNSConfig = Field(default_factory=lambda: V1PodDNSConfig())
    dnsPolicy: Optional[str] = None
    enableServiceLinks: Optional[bool] = None
    ephemeralContainers: List[V1EphemeralContainer] = Field(default_factory=list)
    hostAliases: List[V1HostAlias] = Field(default_factory=list)
    hostIPC: Optional[bool] = None
    hostNetwork: Optional[bool] = None
    hostPID: Optional[bool] = None
    hostUsers: Optional[bool] = None
    hostname: Optional[str] = None
    imagePullSecrets: List[V1LocalObjectReference] = Field(default_factory=list)
    initContainers: List[V1Container] = Field(default_factory=list)
    nodeName: Optional[str] = None
    nodeSelector: Dict[str, str] = Field(default_factory=dict)
    os: V1PodOS = Field(default_factory=lambda: V1PodOS())
    overhead: Dict[str, str] = Field(default_factory=dict)
    preemptionPolicy: Optional[str] = None
    priority: Optional[int] = None
    priorityClassName: Optional[str] = None
    readinessGates: List[V1PodReadinessGate] = Field(default_factory=list)
    resourceClaims: List[V1PodResourceClaim] = Field(default_factory=list)
    restartPolicy: Optional[str] = None
    runtimeClassName: Optional[str] = None
    schedulerName: Optional[str] = None
    schedulingGates: List[V1PodSchedulingGate] = Field(default_factory=list)
    securityContext: V1PodSecurityContext = Field(default_factory=lambda: V1PodSecurityContext())
    serviceAccount: Optional[str] = None
    serviceAccountName: Optional[str] = None
    setHostnameAsFQDN: Optional[bool] = None
    shareProcessNamespace: Optional[bool] = None
    subdomain: Optional[str] = None
    terminationGracePeriodSeconds: Optional[int] = None
    tolerations: List[V1Toleration] = Field(default_factory=list)
    topologySpreadConstraints: List[V1TopologySpreadConstraint] = Field(default_factory=list)
    volumes: List[V1Volume] = Field(default_factory=list)


class V1PodTemplateSpec(ResourceValue):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1PodSpec = Field(default_factory=lambda: V1PodSpec())


class V1PodFailurePolicyOnPodConditionsPattern(ResourceValue):
    status: Optional[str] = None
    type: Optional[str] = None


class V1PodFailurePolicyOnExitCodesRequirement(ResourceValue):
    containerName: Optional[str] = None
    operator: Optional[str] = None
    values: List[int] = Field(default_factory=list)


class V1PodFailurePolicyRule(ResourceValue):
    action: Optional[str] = None
    onExitCodes: V1PodFailurePolicyOnExitCodesRequirement = Field(
        default_factory=lambda: V1PodFailurePolicyOnExitCodesRequirement()
    )
    onPodConditions: List[V1PodFailurePolicyOnPodConditionsPattern] = Field(default_factory=list)


class V1PodFailurePolicy(ResourceValue):
    rules: List[V1PodFailurePolicyRule] = Field(default_factory=list)


class V1JobSpec(ResourceValue):
    activeDeadlineSeconds: Optional[int] = None
    backoffLimit: Optional[int] = None
    completionMode: Optional[str] = None
    completions: Optional[int] = None
    manualSelector: Optional[bool] = None
    parallelism: Optional[int] = None
    podFailurePolicy: V1PodFailurePolicy = Field(default_factory=lambda: V1PodFailurePolicy())
    selector: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    suspend: Optional[bool] = None
    template: V1PodTemplateSpec = Field(default_factory=lambda: V1PodTemplateSpec())
    ttlSecondsAfterFinished: Optional[int] = None


class V1JobTemplateSpec(ResourceValue):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1JobSpec = Field(default_factory=lambda: V1JobSpec())


class V1CronJobSpec(ResourceValue):
    concurrencyPolicy: Optional[str] = None
    failedJobsHistoryLimit: Optional[int] = None
    jobTemplate: V1JobTemplateSpec = Field(default_factory=lambda: V1JobTemplateSpec())
    schedule: Optional[str] = None
    startingDeadlineSeconds: Optional[int] = None
    successfulJobsHistoryLimit: Optional[int] = None
    suspend: Optional[bool] = None
    timeZone: Optional[str] = None


class V1CronJob(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1CronJobSpec = Field(default_factory=lambda: V1CronJobSpec())
    status: V1CronJobStatus = Field(default_factory=lambda: V1CronJobStatus())


class V1ControllerRevisionList(ResourceItem):
    items: List[V1ControllerRevision] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ControllerRevision(ResourceItem):
    data: Optional[object] = None
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    revision: Optional[int] = None


class V1ConfigMapList(ResourceItem):
    items: List[V1ConfigMap] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ComponentStatusList(ResourceItem):
    items: List[V1ComponentStatus] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ComponentCondition(ResourceValue):
    error: Optional[str] = None
    message: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1ComponentStatus(ResourceItem):
    conditions: List[V1ComponentCondition] = Field(default_factory=list)
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())


class V1ClusterRoleList(ResourceItem):
    items: List[V1ClusterRole] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1ClusterRoleBindingList(ResourceItem):
    items: List[V1ClusterRoleBinding] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1Subject(ResourceValue):
    apiGroup: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None


class V1RoleRef(ResourceValue):
    apiGroup: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None


class V1ClusterRoleBinding(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    roleRef: V1RoleRef = Field(default_factory=lambda: V1RoleRef())
    subjects: List[V1Subject] = Field(default_factory=list)


class V1PolicyRule(ResourceValue):
    apiGroups: List[str] = Field(default_factory=list)
    nonResourceURLs: List[str] = Field(default_factory=list)
    resourceNames: List[str] = Field(default_factory=list)
    resources: List[str] = Field(default_factory=list)
    verbs: List[str] = Field(default_factory=list)


class V1AggregationRule(ResourceValue):
    clusterRoleSelectors: List[V1LabelSelector] = Field(default_factory=list)


class V1ClusterRole(ResourceItem):
    aggregationRule: V1AggregationRule = Field(default_factory=lambda: V1AggregationRule())
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    rules: List[V1PolicyRule] = Field(default_factory=list)


class V1CertificateSigningRequestList(ResourceItem):
    items: List[V1CertificateSigningRequest] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1CertificateSigningRequestCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    lastUpdateTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1CertificateSigningRequestStatus(ResourceValue):
    certificate: Optional[str] = None
    conditions: List[V1CertificateSigningRequestCondition] = Field(default_factory=list)


class V1CertificateSigningRequestSpec(ResourceValue):
    expirationSeconds: Optional[int] = None
    extra: Dict[str, List[str]] = Field(default_factory=dict)
    groups: List[str] = Field(default_factory=list)
    request: Optional[str] = None
    signerName: Optional[str] = None
    uid: Optional[str] = None
    usages: List[str] = Field(default_factory=list)
    username: Optional[str] = None


class V1CertificateSigningRequest(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1CertificateSigningRequestSpec = Field(default_factory=lambda: V1CertificateSigningRequestSpec())
    status: V1CertificateSigningRequestStatus = Field(default_factory=lambda: V1CertificateSigningRequestStatus())


class V1CSIStorageCapacityList(ResourceItem):
    items: List[V1CSIStorageCapacity] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1LabelSelectorRequirement(ResourceValue):
    key: Optional[str] = None
    operator: Optional[str] = None
    values: List[str] = Field(default_factory=list)


class V1LabelSelector(ResourceValue):
    matchExpressions: List[V1LabelSelectorRequirement] = Field(default_factory=list)
    matchLabels: Dict[str, str] = Field(default_factory=dict)


class V1CSIStorageCapacity(ResourceItem):
    capacity: Optional[str] = None
    maximumVolumeSize: Optional[str] = None
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    nodeTopology: V1LabelSelector = Field(default_factory=lambda: V1LabelSelector())
    storageClassName: Optional[str] = None


class V1CSINodeList(ResourceItem):
    items: List[V1CSINode] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1VolumeNodeResources(ResourceValue):
    count: Optional[int] = None


class V1CSINodeDriver(ResourceValue):
    allocatable: V1VolumeNodeResources = Field(default_factory=lambda: V1VolumeNodeResources())
    name: Optional[str] = None
    nodeID: Optional[str] = None
    topologyKeys: List[str] = Field(default_factory=list)


class V1CSINodeSpec(ResourceValue):
    drivers: List[V1CSINodeDriver] = Field(default_factory=list)


class V1CSINode(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1CSINodeSpec = Field(default_factory=lambda: V1CSINodeSpec())


class V1CSIDriverList(ResourceItem):
    items: List[V1CSIDriver] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class StorageV1TokenRequest(ResourceValue):
    audience: Optional[str] = None
    expirationSeconds: Optional[int] = None


class V1CSIDriverSpec(ResourceValue):
    attachRequired: Optional[bool] = None
    fsGroupPolicy: Optional[str] = None
    podInfoOnMount: Optional[bool] = None
    requiresRepublish: Optional[bool] = None
    seLinuxMount: Optional[bool] = None
    storageCapacity: Optional[bool] = None
    tokenRequests: List[StorageV1TokenRequest] = Field(default_factory=list)
    volumeLifecycleModes: List[str] = Field(default_factory=list)


class V1CSIDriver(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1CSIDriverSpec = Field(default_factory=lambda: V1CSIDriverSpec())


class V1Binding(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    target: V1ObjectReference = Field(default_factory=lambda: V1ObjectReference())


class V1APIVersions(ResourceItem):
    serverAddressByClientCIDRs: List[V1ServerAddressByClientCIDR] = Field(default_factory=list)
    versions: List[str] = Field(default_factory=list)


class V1APIServiceList(ResourceItem):
    items: List[V1APIService] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1APIServiceCondition(ResourceValue):
    lastTransitionTime: Optional[datetime] = None
    message: Optional[str] = None
    reason: Optional[str] = None
    status: Optional[str] = None
    type: Optional[str] = None


class V1APIServiceStatus(ResourceValue):
    conditions: List[V1APIServiceCondition] = Field(default_factory=list)


class ApiregistrationV1ServiceReference(ResourceValue):
    name: Optional[str] = None
    namespace: Optional[str] = None
    port: Optional[int] = None


class V1APIServiceSpec(ResourceValue):
    caBundle: Optional[str] = None
    group: Optional[str] = None
    groupPriorityMinimum: Optional[int] = None
    insecureSkipTLSVerify: Optional[bool] = None
    service: ApiregistrationV1ServiceReference = Field(default_factory=lambda: ApiregistrationV1ServiceReference())
    version: Optional[str] = None
    versionPriority: Optional[int] = None


class V1APIService(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1APIServiceSpec = Field(default_factory=lambda: V1APIServiceSpec())
    status: V1APIServiceStatus = Field(default_factory=lambda: V1APIServiceStatus())


class V1APIResource(ResourceValue):
    categories: List[str] = Field(default_factory=list)
    group: Optional[str] = None
    kind: Optional[str] = None
    name: Optional[str] = None
    namespaced: Optional[bool] = None
    shortNames: List[str] = Field(default_factory=list)
    singularName: Optional[str] = None
    storageVersionHash: Optional[str] = None
    verbs: List[str] = Field(default_factory=list)
    version: Optional[str] = None


class V1APIResourceList(ResourceItem):
    groupVersion: Optional[str] = None
    resources: List[V1APIResource] = Field(default_factory=list)


class V1APIGroupList(ResourceItem):
    groups: List[V1APIGroup] = Field(default_factory=list)


class V1ServerAddressByClientCIDR(ResourceValue):
    clientCIDR: Optional[str] = None
    serverAddress: Optional[str] = None


class V1GroupVersionForDiscovery(ResourceValue):
    groupVersion: Optional[str] = None
    version: Optional[str] = None


class V1APIGroup(ResourceItem):
    name: Optional[str] = None
    preferredVersion: V1GroupVersionForDiscovery = Field(default_factory=lambda: V1GroupVersionForDiscovery())
    serverAddressByClientCIDRs: List[V1ServerAddressByClientCIDR] = Field(default_factory=list)
    versions: List[V1GroupVersionForDiscovery] = Field(default_factory=list)


class EventsV1EventList(ResourceItem):
    items: List[EventsV1Event] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class EventsV1EventSeries(ResourceValue):
    count: Optional[int] = None
    lastObservedTime: Optional[datetime] = None


class EventsV1Event(ResourceItem):
    action: Optional[str] = None
    deprecatedCount: Optional[int] = None
    deprecatedFirstTimestamp: Optional[datetime] = None
    deprecatedLastTimestamp: Optional[datetime] = None
    deprecatedSource: V1EventSource = Field(default_factory=lambda: V1EventSource())
    eventTime: Optional[datetime] = None
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    note: Optional[str] = None
    reason: Optional[str] = None
    regarding: V1ObjectReference = Field(default_factory=lambda: V1ObjectReference())
    related: V1ObjectReference = Field(default_factory=lambda: V1ObjectReference())
    reportingController: Optional[str] = None
    reportingInstance: Optional[str] = None
    series: EventsV1EventSeries = Field(default_factory=lambda: EventsV1EventSeries())
    type: Optional[str] = None


class CoreV1EventList(ResourceItem):
    items: List[CoreV1Event] = Field(default_factory=list)
    metadata: V1ListMeta = Field(default_factory=lambda: V1ListMeta())


class V1EventSource(ResourceValue):
    component: Optional[str] = None
    host: Optional[str] = None


class CoreV1EventSeries(ResourceValue):
    count: Optional[int] = None
    lastObservedTime: Optional[datetime] = None


class V1ObjectReference(ResourceItem):
    fieldPath: Optional[str] = None
    name: Optional[str] = None
    namespace: Optional[str] = None
    resourceVersion: Optional[str] = None
    uid: Optional[str] = None


class CoreV1Event(ResourceItem):
    action: Optional[str] = None
    count: Optional[int] = None
    eventTime: Optional[datetime] = None
    firstTimestamp: Optional[datetime] = None
    involvedObject: V1ObjectReference = Field(default_factory=lambda: V1ObjectReference())
    lastTimestamp: Optional[datetime] = None
    message: Optional[str] = None
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    reason: Optional[str] = None
    related: V1ObjectReference = Field(default_factory=lambda: V1ObjectReference())
    reportingComponent: Optional[str] = None
    reportingInstance: Optional[str] = None
    series: CoreV1EventSeries = Field(default_factory=lambda: CoreV1EventSeries())
    source: V1EventSource = Field(default_factory=lambda: V1EventSource())
    type: Optional[str] = None


class V1TokenRequestStatus(ResourceValue):
    expirationTimestamp: Optional[datetime] = None
    token: Optional[str] = None


class V1BoundObjectReference(ResourceItem):
    name: Optional[str] = None
    uid: Optional[str] = None


class V1TokenRequestSpec(ResourceValue):
    audiences: List[str] = Field(default_factory=list)
    boundObjectRef: V1BoundObjectReference = Field(default_factory=lambda: V1BoundObjectReference())
    expirationSeconds: Optional[int] = None


class AuthenticationV1TokenRequest(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1TokenRequestSpec = Field(default_factory=lambda: V1TokenRequestSpec())
    status: V1TokenRequestStatus = Field(default_factory=lambda: V1TokenRequestStatus())


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
