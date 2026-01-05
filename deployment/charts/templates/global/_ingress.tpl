{{/*
Ingress helpers
*/}}

{{- define "rds.ingress" }}
{{- $top := index . 0 -}}
{{- $fullname := index . 1 -}}
{{- $namespace := index . 2 -}}
{{- $name := index . 3 -}}
{{- $service := index . 4 -}}
{{- $port := index . 5 -}}
{{- if $top.enabled -}}
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
    name: {{ $fullname }}-{{ $name }}
    namespace: {{ $namespace }}
    annotations:
        {{- range $key, $value := $top.annotations }}
        {{ $key }}: {{ $value | quote }}
        {{- end }}
spec:
    {{- if $top.class }}
    ingressClassName: {{ $top.class }}
    {{- end }}
    rules:
        -   host: {{ required "No hostname specified" $top.hostname }}
            http:
                paths:
                    -   path: {{ default "/" $top.path | quote}}
                        pathType: {{ default "Prefix" $top.pathPrefix | quote}}
                        backend:
                            service:
                                name: {{ $fullname }}-{{ $service }}
                                port:
                                    number: {{ $port }}
    {{- if $top.tlsSecret }}
    tls:
        -   hosts:
                -   {{ required "No hostname specified" $top.hostname }}
            secretName: {{ $top.tlsSecret }}
    {{- end }}
{{- end -}}
{{- end }}
