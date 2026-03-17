{{/*
Global configuration-specific chart helpers
*/}}

{{- define "rds.generalSettings" }}
RDS_GENERAL_DEBUG: {{ default "false" .Values.debug.enabled | quote }}
RDS_GENERAL_DEBUG_TRACE: {{ default "false" .Values.debug.enableTracing | quote }}
RDS_NETWORK_SERVER_ALLOWED_ORIGINS: "*"
{{- end }}

{{- define "rds.clientSettings" }}
RDS_NETWORK_CLIENT_SERVER_ADDRESS: {{ printf "https://%s" (required "No server address specified" .Values.server.ingress.hostname) | quote }}
{{- end }}
