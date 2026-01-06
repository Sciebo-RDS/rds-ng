{{/*
Connector template, which defines all resources for a connector
*/}}

{{- define "rds.connector" }}
{{- $top := index . 0 -}}
{{- $connector := index . 1 -}}
{{- $name := index . 2 -}}
{{- $defaultTarget := index . 3 -}}
{{- $defaultOAuth2Host := index . 4 -}}
{{- $componentName := printf "connector-%s" $name}}

{{- if $connector.enabled }}
---
apiVersion: apps/v1
kind: Deployment
metadata:
    name: {{ include "rds.fullname" $top }}-{{ $componentName }}
    namespace: {{ include "rds.namespace" $top }}
    labels: {{- include "rds.labels" (list $top $componentName) | nindent 8 }}
spec:
    replicas: 1
    selector:
        matchLabels: {{- include "rds.selectorLabels" (list $top $componentName) | nindent 12 }}
    template:
        metadata:
            labels: {{- include "rds.selectorLabels" (list $top $componentName) | nindent 16 }}
        spec:
            containers:
                -   name: {{ include "rds.fullname" $top }}-{{ $componentName }}
                    {{- include "rds.image" (list $top (printf "rds-ng-%s" $componentName)) | nindent 20 }}
                    ports:
                        -   containerPort: 6969
                    envFrom:
                        -   secretRef:
                                name: {{ include "rds.fullname" $top }}-network-api-secret
                        -   configMapRef:
                                name: {{ include "rds.fullname" $top }}-{{ $componentName }}-config
                        -   secretRef:
                                name: {{ include "rds.fullname" $top }}-{{ $componentName }}-config-secret
            restartPolicy: Always

---
apiVersion: v1
kind: Service
metadata:
    name: {{ include "rds.fullname" $top }}-{{ $componentName }}-service
    namespace: {{ include "rds.namespace" $top }}
    labels: {{- include "rds.labels" (list $top "server") | nindent 8 }}
spec:
    selector:
        {{- include "rds.selectorLabels" (list $top "server") | nindent 8 }}
    ports:
        -   protocol: TCP
            port: 4500
            targetPort: 6969

---
apiVersion: v1
kind: ConfigMap
metadata:
    name: {{ include "rds.fullname" $top }}-{{ $componentName }}-config
    namespace: {{ include "rds.namespace" $top }}
data:
    {{- include "rds.generalSettings" $top | indent 4 }}
    {{- include "rds.clientSettings" $top | indent 4 }}

    RDS_CONNECTOR_TARGET: {{ required (printf "Missing target for connector %s" $name) (default $defaultTarget $connector.targetUrl) | quote }}

    {{ if $connector.oauth2 -}}
    RDS_AUTHORIZATION_OAUTH2_SERVER_HOST: {{ required (printf "Missing OAuth2 host for connector %s" $name) (default $defaultOAuth2Host $connector.oauth2.host) | quote }}
    RDS_AUTHORIZATION_OAUTH2_CLIENT_ID: {{ required (printf "Missing OAuth2 client ID for connector %s" $name) $connector.oauth2.clientId | quote }}
    RDS_AUTHORIZATION_OAUTH2_CLIENT_REDIRECT_URL: {{ printf "https://%s/authorize/oauth2" (required "No Domo hostname specified" $top.Values.domo.ingress.hostname) | quote }}
    {{- end }}

---
apiVersion: v1
kind: Secret
metadata:
    name: {{ include "rds.fullname" $top }}-{{ $componentName }}-config-secret
    namespace: {{ include "rds.namespace" $top }}
type: Opaque
stringData:
    {{ if $connector.oauth2 -}}
    RDS_AUTHORIZATION_OAUTH2_CLIENT_SECRET: {{ required (printf "Missing OAuth2 client secret for connector %s" $name) $connector.oauth2.clientSecret | quote }}
    {{- end }}

{{- end }}
{{- end }}
