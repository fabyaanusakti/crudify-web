from django.utils import timezone
from app.models import ProjekModel
from app.api.services.project_api_fetch import fetch
from app.api.utils.parse import parse_date


def sync_projects(*, delete_stale=True, force=False):
    try:
        remote_data = fetch()

        if not remote_data:
            print("API tidak mengembalikan data atau terjadi kegagalan.")
            return 0, 0, 0

        if not isinstance(remote_data, list):
            print(f"Tipe respon API tidak sesuai: {type(remote_data)}")
            return 0, 0, 0

        created = updated = deleted = 0
        remote_ids = set()
        skipped_ids = set()

        for item in remote_data:
            if not isinstance(item, dict):
                print(f"Melewati item yang bukan dictionary: {item}")
                continue

            project_id = item.get("id")
            if project_id is None:
                print(f"Melewati item tanpa ID: {item}")
                continue

            project_id = str(project_id)
            remote_ids.add(project_id)

            required_fields = {
                'nama_proyek': (str, ""),
                'tanggal_mulai': (str, None),
                'tanggal_selesai': (str, None),
            }

            processed_data = {}
            errors = []
            
            for field, (expected_type, default_value) in required_fields.items():
                value = item.get(field, default_value)
                
                if value is None:
                    errors.append(f"{field} wajib diisi")
                elif not isinstance(value, expected_type):
                    errors.append(f"Tipe data tidak valid untuk {field} (harus {expected_type.__name__})")
                else:
                    processed_data[field] = value

            if errors:
                print(f"Melewati proyek {project_id}: {', '.join(errors)}")
                skipped_ids.add(project_id)
                continue

            try:
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
                    print(f"Berhasil menambahkan proyek {project_id}")
                else:
                    updated += 1
                    print(f"Berhasil memperbarui proyek {project_id}")

            except Exception as e:
                print(f"Gagal memproses proyek {project_id}: {str(e)}")
                continue

        if delete_stale:
            stale_query = ProjekModel.objects.exclude(id_projek__in=remote_ids | skipped_ids)
            deleted = stale_query.count()
            if deleted:
                print(f"Menghapus {deleted} proyek yang tidak ditemukan di API...")
                stale_query.delete()

        print(f"Sinkronisasi selesai — Ditambahkan: {created}, Diperbarui: {updated}, Dihapus: {deleted}")
        if skipped_ids:
            print(f"Proyek yang dilewati ({len(skipped_ids)}): {', '.join(skipped_ids)}")
        return created, updated, deleted

    except Exception as e:
        print(f"Kesalahan kritis saat sinkronisasi: {e}")
        return 0, 0, 0