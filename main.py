import os
import platform
import subprocess
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

def execute_command(command):
    """Executes a system command and prints the output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e.stderr}")

def list_directory(path):
    """Lists the contents of a directory."""
    try:
        contents = os.listdir(path)
        for item in contents:
            print(item)
    except Exception as e:
        print(f"Error listing directory {path}: {e}")

def create_directory(path):
    """Creates a new directory."""
    try:
        os.makedirs(path, exist_ok=True)
        print(f"Directory created: {path}")
    except Exception as e:
        print(f"Error creating directory {path}: {e}")

def delete_file(path):
    """Deletes a file."""
    try:
        os.remove(path)
        print(f"File deleted: {path}")
    except Exception as e:
        print(f"Error deleting file {path}: {e}")

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
    while True:
        print("\nChoose an option:")
        print("1. Backup to cloud")
        print("2. Execute a system command")
        print("3. List directory contents")
        print("4. Create a directory")
        print("5. Delete a file")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            backup_to_cloud()
        elif choice == "2":
            command = input("Enter the command to execute: ")
            execute_command(command)
        elif choice == "3":
            path = input("Enter the directory path: ")
            list_directory(path)
        elif choice == "4":
            path = input("Enter the directory path to create: ")
            create_directory(path)
        elif choice == "5":
            path = input("Enter the file path to delete: ")
            delete_file(path)
        elif choice == "6":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")
