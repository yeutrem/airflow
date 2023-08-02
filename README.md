Step 1: Create VPC (test-vpc) and subnet (test-vpc-asia), create network tag if needed)
Step 2: Create VM (VM name: airflow-prod, external IP: xxx.xxx.xxx.xxx) which is in the VPC and subnet.
Step 3: Edit .env in prod folder (Note that if you deploy postgresql, redis in different VM, please modify REDIS_HOST, POSTGRESQL_HOST in .env)
    a. (edit AIRFLOW_HOST, AIRFLOW__WEBSERVER__BASE_URL, AIRFLOW__LOGGING__GOOGLE_KEY_PATH, AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER). Note: If AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER is gcs object => Service account should have permission to access (read, write) the bucket.
    b. AIRFLOW__WEBSERVER__BASE_URL: should be http://${AIRFLOW_HOST}:8080, it will be http://airflow-prod:8080 following by the example.
Step 4: Edit mount volume (dag folder, service account)
Step 5: Edit webserser_config.py (Fill out OAUTH_PROVIDERS)
Step 6: run command line: docker compose -f docker-compose.yaml --profile flower up -d (may return error for some container)
Step 7: Edit file pg_hba.conf (Add Ip range of subnet - test-vpc-asia, you can run: psql -U airflow -c "SHOW hba_file;")
Do Step 8 -> Step 10 in case of using ssl (In the example, I use namecheap domain: lelong140694.store
Step 8: Generate ssl profile in namecheap webpage
Step 9: Add/Edit Advance DNS:
  Type      HOST     VALUE                                        TTL
  Record    @        External_IP_of_VM_which_host_webserver        Automatic
Step 10: Add airflow_nginx into /etc/nginx/sites-enabled
Step 11: sudo systemctl restart nginx



