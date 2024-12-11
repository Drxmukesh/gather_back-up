import os
import platform
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

def get_backup_path():
    """Determines the backup directory based on the operating system."""
    system = platform.system()
    if system == "Windows":
        return os.path.expandvars(r"C:\\Users\\Admin")
    elif system in ["Linux", "Darwin"]:  # Darwin is macOS
        return os.path.expanduser("/home")
    else:
        raise ValueError(f"Unsupported operating system: {system}")

def authenticate_google_drive():
    """Authenticates with Google Drive and returns a drive instance."""
    gauth = GoogleAuth()

    # Load saved client credentials or authenticate manually
    gauth.LoadCredentialsFile("credentials.json")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()  # Authenticate if no credentials
    elif gauth.access_token_expired:
        gauth.Refresh()  # Refresh expired credentials
    else:
        gauth.Authorize()  # Authorize saved credentials

    gauth.SaveCredentialsFile("credentials.json")
    return GoogleDrive(gauth)

def upload_to_drive(drive, folder_id, file_path):
    """Uploads a file to Google Drive in the specified folder."""
    file_name = os.path.basename(file_path)
    print(f"Uploading {file_name}...")

    file = drive.CreateFile({"parents": [{"id": folder_id}]})
    file.SetContentFile(file_path)
    file['title'] = file_name
    file.Upload()

    print(f"Uploaded: {file_name}")

def backup_to_cloud():
    """Backs up data to the cloud from the specified directory."""
    try:
        backup_path = get_backup_path()
        print(f"Backing up files from: {backup_path}")

        drive = authenticate_google_drive()
        folder_id = "root"  # Replace with your folder ID on Google Drive if needed

        for root, _, files in os.walk(backup_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    upload_to_drive(drive, folder_id, file_path)
                except Exception as e:
                    print(f"Failed to upload {file_path}: {e}")

        print("Backup completed successfully.")

    except Exception as e:
        print(f"Error during backup: {e}")

if __name__ == "__main__":
    backup_to_cloud()
