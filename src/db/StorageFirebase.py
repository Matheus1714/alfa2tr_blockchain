from firebase_admin import credentials, initialize_app, storage
from os.path import exists
from more_itertools import bucket
from dotenv import dotenv_values

class StorageFirebase:
    def __init__(self) -> None:
        self.connect_db()

    def connect_db(self):
        config = dotenv_values(".env")
        SERVICE_ACCOUNT_FIREBASE = config.get('SERVICE_ACCOUNT_FIREBASE')
        cred = credentials.Certificate(SERVICE_ACCOUNT_FIREBASE)
        initialize_app(cred, {'storageBucket': 'alfa2tr.appspot.com'})

    def check_local_path(self, local_path: str) -> None:
        try:
            assert exists(local_path)
        except:
            print("%s file doesn't exist" % local_path)

    def upload_file(self, local_path : str, cloud_path : str="/"):
        try:
            bucket = storage.bucket()
            if cloud_path == "/":
                if local_path.startswith("."):
                    cloud_path = local_path.lstrip("./")
                else:
                    cloud_path = local_path
            blob = bucket.blob(cloud_path)
            blob.upload_from_filename(local_path)

            print(f"File {local_path} has been uploaded as object {cloud_path}")
        except BaseException as err:
            print("Try running initialize()")
            print(err)

    def download_file(self, cloud_path: str, local_path: str = "./") -> None:
        bucket = storage.bucket()
        blob = bucket.blob(cloud_path)
        if local_path == "./":
            local_path += cloud_path.split("/")[-1]
        blob.download_to_filename(local_path)

        print(f"Downloaded object {cloud_path} to file {local_path}")

    def copy_file(self, cloud_source_path: str, cloud_destination_path: str) -> None:
        bucket = storage.bucket()
        blob = bucket.blob(cloud_source_path)
        new_blob = bucket.copy_blob(blob, bucket, cloud_destination_path)

        print(f"Blob {blob.name} has been copy to {new_blob.name}")

    def move_file(self, old_cloud_path: str, new_cloud_path: str) -> None:
        bucket = storage.bucket()
        blob = bucket.blob(old_cloud_path)
        new_blob = bucket.rename_blob(blob, new_cloud_path)

        print(f"Blob {blob.name} has been renamed to {new_blob.name}")

    def delete_file(self, cloud_path: str) -> None:
        bucket = storage.bucket()
        blob = bucket.blob(cloud_path)
        blob.delete()

        print(f"Blob {blob.name} has been deleted.")

    def list_files(self) -> list:
        bucket = storage.bucket()
        blobs = bucket.list_blobs()

        return [blob.name for blob in blobs]