from django.utils import timezone
from datetime import timedelta
from app.models import ProjekModel
from app.api.services.project_api_fetch import fetch
from app.api.utils.parse import parse_date

def sync_projects(*, delete_stale=True, force=False):
    """
    Enhanced version with better error handling and null checks
    """
    try:
        # Fetch and validate data
        remote_data = fetch()
        if not remote_data:
            print("API returned no data or failed")
            return 0, 0, 0

        if not isinstance(remote_data, list):
            print(f"Unexpected API response format: {type(remote_data)}")
            return 0, 0, 0

        remote_ids = set()
        created = updated = deleted = 0

        for item in remote_data:
            # Skip if item is not a dictionary
            if not isinstance(item, dict):
                print(f"Skipping invalid item (not a dictionary): {item}")
                continue

            # Validate project ID
            project_id = item.get('id')
            if project_id is None:
                print(f"Skipping item with null ID: {item}")
                continue

            # Convert ID to string if needed (avoid integer/string mismatch)
            project_id = str(project_id)
            remote_ids.add(project_id)

            # Skip if recently updated via push (unless forced)
            existing = ProjekModel.objects.filter(id_projek=project_id).first()
            if existing and not force:
                if existing.last_updated_source == 'API_PUSH' and \
                   (timezone.now() - existing.updated_at) < timedelta(hours=1):
                    continue

            # Validate required fields with type checking
            required_fields = {
                'nama_projek': (str,),
                'tanggal_mulai': (str,),
                'tanggal_selesai': (str,),
                'status_projek': (str,)
            }

            validation_errors = []
            for field, types in required_fields.items():
                field_value = item.get(field)
                if field_value is None:
                    validation_errors.append(f"Missing {field}")
                elif not isinstance(field_value, types):
                    validation_errors.append(f"Invalid type for {field}")

            if validation_errors:
                print(f"Skipping project {project_id}: {', '.join(validation_errors)}")
                continue

            # Process valid item
            try:
                obj, created_flag = ProjekModel.objects.update_or_create(
                    id_projek=project_id,
                    defaults={
                        'nama_projek': item['nama_projek'],
                        'deskripsi': item.get('deskripsi', ''),
                        'lokasi': item.get('lokasi', ''),
                        'tanggal_mulai': parse_date(item['tanggal_mulai']),
                        'tanggal_selesai': parse_date(item['tanggal_selesai']),
                        'supervisor': item.get('supervisor', ''),
                        'status_projek': item['status_projek'],
                        'last_updated_source': 'API_PULL',
                    }
                )
                
                if created_flag:
                    created += 1
                    print(f"Created project {project_id}")
                else:
                    updated += 1
                    print(f"Updated project {project_id}")

            except Exception as e:
                print(f"Failed to process project {project_id}: {str(e)}")
                continue

        # Handle stale projects
        if delete_stale:
            stale_query = ProjekModel.objects.exclude(id_projek__in=remote_ids)
            deleted = stale_query.count()
            if deleted:
                print(f"Deleting {deleted} stale projects")
                stale_query.delete()

        return created, updated, deleted

    except Exception as e:
        print(f"Critical sync error: {str(e)}")
        return 0, 0, 0