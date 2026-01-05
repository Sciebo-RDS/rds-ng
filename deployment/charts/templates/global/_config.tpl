{{/*
General configuration specific chart helpers
*/}}

{{- define "rds.generalSettings" }}
RDS_GENERAL_DEBUG: {{ .Values.debug.enabled | default "false" }}
RDS_GENERAL_DEBUG_TRACE: {{ .Values.debug.enableTracing | default "false" }}
{{- end }}
