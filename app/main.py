import hashlib
import json
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from app.database import engine, SessionLocal
from app.models import ITDRRecord
from app.normalizers.generic import normalize_data
from app.parser import parse_json, parse_csv, parse_xml
app = FastAPI(
    title="ITDR Generic Data Ingestion Framework"
)

# Create database tables
ITDRRecord.metadata.create_all(bind=engine)

@app.get("/")
def home():
    return {
        "message": "ITDR Ingestion Framework is running"
    }

def generate_event_id(record, normalized_data):
    """
    Generate a unique event ID.

    If the input record already contains event_id,
    use it.

    Otherwise generate an ID from the complete
    original record.
    """

    if isinstance(record, dict) and record.get("event_id"):
        return str(record["event_id"])

    event_string = json.dumps(
        record,
        sort_keys=True,
        default=str
    )

    return hashlib.sha256(
        event_string.encode()
    ).hexdigest()


@app.post("/ingest/file")
async def ingest_file(
    source: str = Form(...),
    operation: str = Form("insert"),
    file: UploadFile = File(...)
):

    # Step 1: Validate operation

    operation = operation.lower().strip()

    allowed_operations = {
        "insert",
        "append",
        "truncate",
        "upsert"
    }

    if operation not in allowed_operations:
        raise HTTPException(
            status_code=400,
            detail="Use insert, append, truncate or upsert"
        )

    # Step 2: Read uploaded file
    content = await file.read()
    filename = file.filename.lower()

    # Step 3: Parse file

    if filename.endswith(".json"):
        records = parse_json(content)

    elif filename.endswith(".csv"):
        records = parse_csv(content)

    elif filename.endswith(".xml"):
        records = parse_xml(content)

    else:
        raise HTTPException(
            status_code=400,
            detail="Only JSON, CSV and XML files are supported"
        )
    # Step 4: Create database session
    db: Session = SessionLocal()

    try:
        # Step 5: TRUNCATE
        if operation == "truncate":

            db.query(ITDRRecord).delete(
                synchronize_session=False
            )

            db.commit()

        normalized_records = []

        # Step 6: Normalize records

        for record in records:

            normalized_data = normalize_data(
                record,
                source
            )

            event_id = generate_event_id(
                record,
                normalized_data
            )

            normalized_data["event_id"] = event_id

            normalized_records.append(
                normalized_data
            )

        # Step 7: INSERT / APPEND / TRUNCATE

        if operation in {
            "insert",
            "append",
            "truncate"
        }:

            for normalized_data, record in zip(
                normalized_records,
                records
            ):

                db_record = ITDRRecord(
                    event_id=normalized_data["event_id"],
                    source=normalized_data["source"],
                    raw_data=record
                )

                db.add(db_record)

        # Step 8: UPSERT

        elif operation == "upsert":

            for normalized_data, record in zip(
                normalized_records,
                records
            ):

                statement = insert(
                    ITDRRecord
                ).values(
                    event_id=normalized_data["event_id"],
                    source=normalized_data["source"],
                    raw_data=record
                )

                statement = statement.on_conflict_do_update(
                    index_elements=["event_id"],
                    set_={
                        "source": normalized_data["source"],
                        "raw_data": record
                    }
                )

                db.execute(statement)

        # Step 9: Commit

        db.commit()

        return {
            "message": "File processed successfully",
            "source": source,
            "operation": operation,
            "records_received": len(records),
            "data": normalized_records
        }

    except Exception as e:

        db.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        db.close()