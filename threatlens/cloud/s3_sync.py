import os 

class S3Syncing:
    def syncing_TO_s3(self, folder_name: str, bucket_url: str):
        try:
            command = f"aws s3 sync {folder_name} {bucket_url}"
            os.system(command)
        except Exception as e:
            raise e
    def syncing_FROM_s3(self, folder_name: str, bucket_url: str):
        try:
            command = f"aws s3 sync {bucket_url} {folder_name}"
            os.system(command)
        except Exception as e:
            raise e