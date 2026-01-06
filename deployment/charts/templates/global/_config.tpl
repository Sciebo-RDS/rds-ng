{{/*
Global configuration-specific chart helpers
*/}}

{{- define "rds.generalSettings" }}
RDS_GENERAL_DEBUG: {{ .Values.debug.enabled | default "false" }}
RDS_GENERAL_DEBUG_TRACE: {{ .Values.debug.enableTracing | default "false" }}
RDS_NETWORK_SERVER_ALLOWED_ORIGINS: "*"
{{- end }}

{{- define "rds.clientSettings" }}
RDS_NETWORK_CLIENT_SERVER_ADDRESS: {{ printf "https://%s" (required "No server address specified" .Values.server.ingress.hostname) | quote }}
{{- end }}
