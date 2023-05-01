import boto3
from config.environ import Environ


class AWSSession:
    @classmethod
    def connector_cl(cls, service):
        session = boto3.session.Session()
        conn = session.client(service,
                              aws_access_key_id=Environ.AWS_ACCESS_KEY,
                              aws_secret_access_key=Environ.AWS_SECRET_ACCESS_KEY,
                              region_name=Environ.AWS_REGION)
        return conn

    @classmethod
    def connector_re(cls, service):
        session = boto3.session.Session()
        conn = session.resource(service)
        return conn
