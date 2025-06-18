from django.utils import timezone
from app.models import ProjekModel
from app.api.services.project_api_fetch import fetch
from app.api.utils.parse import parse_date


def sync_projects(*, delete_stale=True, force=False):
    """
    Sync project data from external API into ProjekModel.
    Returns a tuple of (created, updated, deleted).
    """
    try:
        # Fetch data from API
        remote_data = fetch()

        if not remote_data:
            print("❌ API returned no data or failed.")
            return 0, 0, 0

        if not isinstance(remote_data, list):
            print(f"❌ Unexpected API response type: {type(remote_data)}")
            return 0, 0, 0

        created = updated = deleted = 0
        remote_ids = set()
        skipped_ids = set()

        for item in remote_data:
            if not isinstance(item, dict):
                print(f"⚠️ Skipping non-dictionary item: {item}")
                continue

            project_id = item.get("id")
            if project_id is None:
                print(f"⚠️ Skipping item with no ID: {item}")
                continue

            project_id = str(project_id)
            remote_ids.add(project_id)

            # Validate required fields from API (note: use API key names)
            required_fields = {
                'nama_proyek': (str, ""),  # (expected_type, default_value)
                'tanggal_mulai': (str, None),
                'tanggal_selesai': (str, None),
            }

            # Prepare data with defaults for missing fields
            processed_data = {}
            errors = []
            
            for field, (expected_type, default_value) in required_fields.items():
                value = item.get(field, default_value)
                
                if value is None:
                    errors.append(f"Missing required {field}")
                elif not isinstance(value, expected_type):
                    errors.append(f"Invalid type for {field} (expected {expected_type.__name__})")
                else:
                    processed_data[field] = value

            if errors:
                print(f"⚠️ Skipping project {project_id}: {', '.join(errors)}")
                skipped_ids.add(project_id)
                continue

            try:
                # Convert dates
                processed_data['tanggal_mulai'] = parse_date(processed_data['tanggal_mulai'])
                processed_data['tanggal_selesai'] = parse_date(processed_data['tanggal_selesai'])
                
                obj, created_flag = ProjekModel.objects.update_or_create(
                    id_projek=project_id,
                    defaults={
                        'nama_projek': processed_data['nama_proyek'],
                        'deskripsi': item.get('deskripsi_proyek', ''),
                        'lokasi': item.get('lokasi', ''),
                        'tanggal_mulai': processed_data['tanggal_mulai'],
                        'tanggal_selesai': processed_data['tanggal_selesai'],
                        'supervisor_proyek': item.get('supervisor_proyek', ''),
                    }
                )
                if created_flag:
                    created += 1
                    print(f"✅ Created project {project_id}")
                else:
                    updated += 1
                    print(f"🔄 Updated project {project_id}")

            except Exception as e:
                print(f"❌ Failed to process project {project_id}: {str(e)}")
                continue

        # Optionally delete stale local projects
        if delete_stale:
            # Don't delete projects that were skipped due to validation errors
            stale_query = ProjekModel.objects.exclude(id_projek__in=remote_ids | skipped_ids)
            deleted = stale_query.count()
            if deleted:
                print(f"🗑️ Deleting {deleted} stale projects...")
                stale_query.delete()

        print(f"✅ Sync complete — Created: {created}, Updated: {updated}, Deleted: {deleted}")
        if skipped_ids:
            print(f"⚠️ Skipped projects ({len(skipped_ids)}): {', '.join(skipped_ids)}")
        return created, updated, deleted

    except Exception as e:
        print(f"💥 Critical sync error: {e}")
        return 0, 0, 0