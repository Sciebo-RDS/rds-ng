{{/*
General chart helpers
*/}}

{{- define "rds.image" -}}
{{- $top := index . 0 -}}
{{- $image := index . 1 -}}
image: "{{ $top.Values.image.host | default "ghcr.io/sciebo-rds" }}/{{ $image }}:{{ $top.Values.image.tag | default "latest" }}"
imagePullPolicy: {{ $top.Values.image.pullPolicy | default "always" }}
{{- end }}

{{- define "rds.serverAddress" }}
{{- printf "https://%s" (required "No server address specified" .Values.server.ingress.hostname) -}}
{{- end }}
