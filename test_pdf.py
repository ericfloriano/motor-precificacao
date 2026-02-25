import sys
sys.path.append('backend')
from database import SessionLocal
from models import PricingHistory
import export
from schemas import PricingHistoryOut

db = SessionLocal()
item = db.query(PricingHistory).first()
if item:
    data = PricingHistoryOut.model_validate(item).model_dump()
    try:
        export.export_to_pdf(data)
        print("Success")
    except Exception as e:
        import traceback
        traceback.print_exc()
else:
    print("No items in DB")
