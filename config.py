ACCOUNT_NAME = "silpa"
ACCOUNT_KEY = "euy+IZyhvLaXwP+pbO+3DXTZ6Dp8xvk+wneV0eCYMJO6eQLG3iQOkhpApXz8F4/YRoBy5HwtZgwm+AStQnvqDw=="
CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=fileuploads;AccountKey=euy+IZyhvLaXwP+pbO+3DXTZ6Dp8xvk+wneV0eCYMJO6eQLG3iQOkhpApXz8F4/YRoBy5HwtZgwm+AStQnvqDw==;EndpointSuffix=core.windows.net"
CONTAINER = "fileuploads1"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg','csv'])
MAX_CONTENT_LENGTH = 20 * 1024 * 1024    # 20 Mb limit
UPLOAD_FOLDER = "static/"
BLOB_SAS_URL= "https://fileuploads.blob.core.windows.net/fileuploads1/people.csv?sp=r&st=2022-06-08T18:00:57Z&se=2022-06-09T02:00:57Z&spr=https&sv=2020-08-04&sr=b&sig=0no1rSKz9FcbFwY1JEW1stW7vAC2yUGr8m1GcBiE3O4%3D"