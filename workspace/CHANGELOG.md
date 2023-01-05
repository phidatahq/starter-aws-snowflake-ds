### 1/5/2023

1. Enable Superset Public Role
2. Enable Github Authentication - differentiate between admin & users based on team.
3. Use Rds as database
4. Use Elasticache as cache
5. Build custom image (ECR) using github actions
6. Fix connectivity issues using cross-zone load balancing
7. Add 3 jupyterlab notebooks
8. Run new DAGs
9. Run Airflow & Jupyter dev locally

Steps:

1. Clone: https://github.com/phidatahq/starter-aws-snowflake-ds.git
2. Update workspace
3. Create new AWS resources
4. Create IAM user `github-actions` with permission: AmazonEC2ContainerRegistryPowerUser
5. Update Github secrets
6. Create new ECR repo
7. Create new ECR images
8. Update database + cache creds in airflow secrets
9. Update database + cache creds in superset secrets
10. Create Github Oauth App
11. Update Github client creds in airflow secrets
12. Update Github client creds in superset secrets
13. Create new k8s resources
