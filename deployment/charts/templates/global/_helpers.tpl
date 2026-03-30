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
{{- $top := index . 0 -}}
{{- $component := index . 1 -}}
helm.sh/chart: {{ include "rds.chart" $top }}
{{- if $top.Chart.AppVersion }}
app.kubernetes.io/version: {{ $top.Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ $top.Release.Service }}
{{ include "rds.selectorLabels" (list $top $component) }}
{{- end }}

{{- define "rds.selectorLabels" -}}
{{- $top := index . 0 -}}
{{- $component := index . 1 -}}
app.kubernetes.io/instance: {{ $top.Release.Name }}
app.kubernetes.io/name: {{ include "rds.name" $top }}
rds.component: {{ $component }}
{{- end }}
