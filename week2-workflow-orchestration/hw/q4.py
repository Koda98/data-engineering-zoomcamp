from prefect.deployments import Deployment
from prefect.filesystems import GitHub
from etl_web_to_gcs import etl_web_to_gcs

github_block = GitHub.load("zoom-github")

docker_dep = Deployment.build_from_flow(
    flow=etl_web_to_gcs,
    name='github-deploy',
    storage=github_block,
    entrypoint="week2-workflow-orchestration/hw/etl_web_to_gcs.py:etl_web_to_gcs"
)

if __name__ == "__main__":
    docker_dep.apply()
