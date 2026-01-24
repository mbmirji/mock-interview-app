from supabase import create_client, Client
from app.config import get_settings
import uuid

settings = get_settings()

class StorageService:
    def __init__(self):
        # Initialize only if credentials are present to avoid errors during test/startup if unconfigured
        if settings.supabase_url and settings.supabase_service_key:
            self.supabase: Client = create_client(settings.supabase_url, settings.supabase_service_key)
        else:
            self.supabase = None
        self.bucket_name = settings.supabase_storage_bucket

    def upload_audio(self, file_bytes: bytes, filename: str, mime_type: str = "audio/webm") -> str:
        """
        Uploads audio to Supabase Storage and returns the public URL
        """
        if not self.supabase:
            raise Exception("Supabase credentials not configured")

        try:
            # Create a unique filename to avoid collisions
            unique_filename = f"{uuid.uuid4()}-{filename}"
            
            # Upload file
            self.supabase.storage.from_(self.bucket_name).upload(
                path=unique_filename,
                file=file_bytes,
                file_options={"content-type": mime_type}
            )
            
            # Get Public URL
            public_url = self.supabase.storage.from_(self.bucket_name).get_public_url(unique_filename)
            
            return public_url
        except Exception as e:
            print(f"Error uploading to Supabase: {e}")
            raise e
