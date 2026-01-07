{{/*
Database-specific helpers
*/}}

{{- define "rds.database.settings" }}
{{- $settings := index . 0 -}}
{{- $name := index . 1 -}}
RDS_STORAGE_DATABASE_{{- upper $name -}}_HOST: {{ required (printf "%s host is required" $name) $settings.host | quote }}
RDS_STORAGE_DATABASE_{{- upper $name -}}_PORT: {{ required (printf "%s port is required" $name) $settings.port | quote }}
RDS_STORAGE_DATABASE_{{- upper $name -}}_DATABASE: {{ default "rds-ng" $settings.database | quote }}
RDS_STORAGE_DATABASE_{{- upper $name -}}_USER: {{ required (printf "%s username is required" $name) $settings.user | quote }}
{{- end }}

{{- define "rds.database.secrets" }}
{{- $settings := index . 0 -}}
{{- $name := index . 1 -}}
RDS_STORAGE_DATABASE_{{- upper $name -}}_PASSWORD: {{ required (printf "%s password is required" $name) $settings.password | quote }}
{{- end }}
