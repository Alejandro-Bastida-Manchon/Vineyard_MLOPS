from datetime import datetime, timedelta

from airflow.decorators import dag, task


@dag(
    dag_id="ingest_validate",
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    default_args={"retries": 2, "retry_delay": timedelta(minutes=2)},
    tags=["vineyard", "ingest"],
)
def ingest_validate():
    @task
    def list_new_images() -> list[str]:
        from vineyard.storage import list_keys

        return list_keys("raw/")

    @task
    def validate_and_move(keys: list[str]) -> dict:
        from vineyard.storage import BUCKET, get_s3, list_keys
        from vineyard.validation import image_hash, validate_image

        s3 = get_s3()
        seen = {k.rsplit("/", 1)[-1].split(".")[0] for k in list_keys("validated/")}
        stats = {"ok": 0, "duplicate": 0, "rejected": 0}

        for key in keys:
            data = s3.get_object(Bucket=BUCKET, Key=key)["Body"].read()
            digest = image_hash(data)
            ext = key.rsplit(".", 1)[-1].lower()
            ok, reason = validate_image(data)

            if not ok:
                outcome, dest = "rejected", f"rejected/{reason}/{digest}.{ext}"
            elif digest in seen:
                outcome, dest = "duplicate", f"rejected/duplicate/{digest}.{ext}"
            else:
                outcome, dest = "ok", f"validated/{digest}.{ext}"
                seen.add(digest)

            s3.put_object(Bucket=BUCKET, Key=dest, Body=data)
            s3.delete_object(Bucket=BUCKET, Key=key)
            stats[outcome] += 1

        return stats

    @task
    def report(stats: dict):
        print(f"Resumen de ingesta: {stats}")

    report(validate_and_move(list_new_images()))


ingest_validate()