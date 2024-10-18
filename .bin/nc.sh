#!/bin/bash
docker stop nextcloud
docker rm -f nextcloud
docker run -d -p 8080:80 \
--name nextcloud \
-e NEXTCLOUD_ADMIN_USER=admin \
-e NEXTCLOUD_ADMIN_PASSWORD=admin \
-v nextcloud:/var/www/html \
-v /proj/Nextcloud/custom_apps:/var/www/html/custom_apps \
-v /proj/RDS/rds-ng-nextcloud:/var/www/html/custom_apps/rdsng \
-v /proj/Overleaf/overleaf-nextcloud:/var/www/html/custom_apps/overleaf_nextcloud \
nextcloud:28

docker exec -w /var/www/html/custom_apps/rdsng nextcloud make build
docker exec -u 33 nextcloud /var/www/html/occ config:system:set trusted_domains 10 --value=10.0.2.15
docker exec -u 33 nextcloud /var/www/html/occ config:system:set overwritehost --value=10.0.2.15:8080
