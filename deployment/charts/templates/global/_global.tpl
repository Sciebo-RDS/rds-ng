{{/*
General chart helpers
*/}}

{{- define "rds.image" -}}
{{- $top := index . 0 -}}
{{- $image := index . 1 -}}
image: "{{ $top.Values.image.host | default "ghcr.io/sciebo-rds" }}/{{ $image }}:{{ $top.Values.image.tag | default "latest" }}"
imagePullPolicy: {{ $top.Values.image.pullPolicy | default "Always" }}
{{- end }}

{{- define "rds.serverAddress" }}
{{- printf "https://%s" (required "No server address specified" .Values.server.ingress.hostname) -}}
{{- end }}

{{- define "rds.extraEnv" }}
{{- $top := index . 0 -}}
{{- $env := index . 1 -}}
{{- range $env }}
- name: {{ .name }}
  {{- if hasKey . "value" }}
  value: {{ .value | quote }}
  {{- else if .valueFrom }}
  valueFrom:
    {{- toYaml .valueFrom | nindent 28 }}
  {{- end }}
{{- end }}
{{- end }}
