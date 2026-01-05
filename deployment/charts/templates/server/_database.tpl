{{/*
Database-specific helpers
*/}}

{{- define "rds.database.settings" }}
{{- $settings := index . 0 -}}
{{- $name := index . 1 -}}
RDS_STORAGE_DATABASE_{{- $name | upper -}}_HOST: {{ required (printf "%s host is required" $name) $settings.host | quote }}
RDS_STORAGE_DATABASE_{{- $name | upper -}}_PORT: {{ required (printf "%s port is required" $name) $settings.port }}
RDS_STORAGE_DATABASE_{{- $name | upper -}}_DATABASE: {{ default "rds-ng" $settings.database | quote }}
RDS_STORAGE_DATABASE_{{- $name | upper -}}_USER: {{ required (printf "%s username is required" $name) $settings.user | quote }}
{{- end }}

{{- define "rds.database.secrets" }}
{{- $settings := index . 0 -}}
{{- $name := index . 1 -}}
RDS_STORAGE_DATABASE_{{- $name | upper -}}_PASSWORD: {{ required (printf "%s password is required" $name) $settings.password | quote }}
{{- end }}
