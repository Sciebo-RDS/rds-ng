{{/*
Ingress helpers
*/}}

{{- define "rds.ingress" }}
{{- $top := index . 0 -}}
{{- $ingress := index . 1 -}}
{{- $name := index . 2 -}}
{{- $service := index . 3 -}}
{{- $port := index . 4 -}}
{{- if $ingress.enabled }}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
    name: {{ include "rds.fullname" $top }}-{{ $name }}
    namespace: {{ include "rds.namespace" $top }}
    annotations:
        {{- range $key, $value := $ingress.annotations }}
        {{ $key }}: {{ $value | quote }}
        {{- end }}
spec:
    {{- if $ingress.class }}
    ingressClassName: {{ $ingress.class }}
    {{- end }}
    rules:
        -   host: {{ required "No hostname specified" $ingress.hostname | quote }}
            http:
                paths:
                    -   path: {{ default "/" $ingress.path | quote}}
                        pathType: {{ default "Prefix" $ingress.pathPrefix | quote}}
                        backend:
                            service:
                                name: {{ include "rds.fullname" $top }}-{{ $service }}
                                port:
                                    number: {{ $port }}
    {{- if $ingress.tlsSecret }}
    tls:
        -   hosts:
                -   {{ required "No hostname specified" $ingress.hostname | quote }}
            secretName: {{ $ingress.tlsSecret }}
    {{- end }}
{{- end }}
{{- end }}
