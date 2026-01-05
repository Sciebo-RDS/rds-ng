{{/*
Basic chart helpers
*/}}

{{- define "rds.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "rds.name" -}}
{{- default "rds" .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "rds.fullname" -}}
{{- default "rds" .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "rds.namespace" }}
{{- default "" .Values.namespace }}
{{- end}}

{{- define "rds.labels" -}}
helm.sh/chart: {{ include "rds.chart" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{ include "rds.selectorLabels" . }}
{{- end }}

{{- define "rds.selectorLabels" -}}
app.kubernetes.io/instance: {{ .Release.Name }}
app.kubernetes.io/name: {{ include "rds.name" . }}
{{- end }}
