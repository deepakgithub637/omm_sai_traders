"""
OMM SAI TRADERS - FastAPI Backend
Owner: Prafulla Kumar Sahoo
Location: Bandhabhuin, Nayagarh, Odisha - 752082
GSTIN: 21FDBPS9893G2Z1

Run locally in PyCharm:
    1. Create backend/.env with your Supabase credentials
    2. pip install -r requirements.txt
    3. Run this file directly (python main.py)
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import logging

# ── Logging setup (shows errors in PyCharm console) ─────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
log = logging.getLogger(__name__)

# ── Load .env file ───────────────────────────────────────────────
# Create a file called .env in the backend/ folder with:
#   SUPABASE_URL=https://xxxx.supabase.co
#   SUPABASE_KEY=your_anon_key_here
try:
    from dotenv import load_dotenv
    load_dotenv()
    log.info(".env file loaded")
except Exception:
    log.warning("python-dotenv not found, reading from system environment")

# ── Supabase Connection ──────────────────────────────────────────
SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "").strip()

supabase = None
SUPABASE_ENABLED = False

if SUPABASE_URL and SUPABASE_KEY:
    try:
        from supabase import create_client, Client
        supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        SUPABASE_ENABLED = True
        log.info(f"✅ Supabase connected: {SUPABASE_URL}")
    except Exception as e:
        log.error(f"❌ Supabase connection FAILED: {e}")
        SUPABASE_ENABLED = False
else:
    log.warning("⚠️  SUPABASE_URL or SUPABASE_KEY not set — running in MOCK mode")
    log.warning("    Create backend/.env file with your Supabase credentials")

# ── App Setup ────────────────────────────────────────────────────
app = FastAPI(
    title="OMM SAI TRADERS API",
    description="Backend for OMM SAI TRADERS - Fertilizer & Pesticide Shop, Odisha",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Pydantic Models ──────────────────────────────────────────────
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    category: str
    price: float
    stock: int
    description: str
    image_url: Optional[str] = None
    rating: Optional[float] = 4.0
    brand: Optional[str] = None

class OrderItem(BaseModel):
    product_id: int
    quantity: int
    price: float

class Order(BaseModel):
    customer_name: str
    customer_email: str
    customer_phone: str
    customer_address: str
    items: List[OrderItem]
    total_amount: float
    payment_method: str = "COD"
    notes: Optional[str] = None

class ContactMessage(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str

# ── Mock Data (used when Supabase is not connected) ──────────────
MOCK_PRODUCTS = [
    {"id": 1,  "name": "DAP Fertilizer 50kg",      "category": "fertilizer", "price": 1350.00, "stock": 100, "description": "Di-Ammonium Phosphate - Best for Kharif crops.",      "image_url": "https://placehold.co/400x400/1a472a/white?text=DAP+50kg",        "rating": 4.8, "brand": "IFFCO"},
    {"id": 2,  "name": "Urea 45kg Bag",             "category": "fertilizer", "price":  266.00, "stock": 200, "description": "Government subsidized urea. Best nitrogen source.",   "image_url": "https://placehold.co/400x400/2d5a27/white?text=UREA+45kg",       "rating": 4.9, "brand": "NFL"},
    {"id": 3,  "name": "NPK 10-26-26 Fertilizer",   "category": "fertilizer", "price": 1450.00, "stock":  80, "description": "Balanced NPK for paddy and vegetables.",              "image_url": "https://placehold.co/400x400/1b5e20/white?text=NPK+10-26-26",    "rating": 4.7, "brand": "Coromandel"},
    {"id": 4,  "name": "MOP Potash 50kg",            "category": "fertilizer", "price": 1100.00, "stock":  75, "description": "Muriate of Potash - Improves fruit quality.",        "image_url": "https://placehold.co/400x400/b71c1c/white?text=MOP+50kg",        "rating": 4.6, "brand": "IPL"},
    {"id": 5,  "name": "Chlorpyrifos 20% EC 1L",    "category": "pesticide",  "price":  320.00, "stock": 150, "description": "Broad-spectrum insecticide for rice pests.",          "image_url": "https://placehold.co/400x400/1a237e/white?text=Chlorpyrifos",    "rating": 4.5, "brand": "Dhanuka"},
    {"id": 6,  "name": "Imidacloprid 17.8% SL",     "category": "pesticide",  "price":  480.00, "stock":  90, "description": "Systemic insecticide for sucking pests.",             "image_url": "https://placehold.co/400x400/283593/white?text=Imidacloprid",    "rating": 4.6, "brand": "Bayer"},
    {"id": 7,  "name": "Mancozeb 75% WP 500g",      "category": "fungicide",  "price":  260.00, "stock": 120, "description": "Protectant fungicide for blast and brown spot.",      "image_url": "https://placehold.co/400x400/4a148c/white?text=Mancozeb",        "rating": 4.4, "brand": "Indofil"},
    {"id": 8,  "name": "Tricyclazole 75% WP 250g",  "category": "fungicide",  "price":  380.00, "stock":  85, "description": "Curative action against rice blast.",                 "image_url": "https://placehold.co/400x400/4e342e/white?text=Tricyclazole",    "rating": 4.5, "brand": "Dow"},
    {"id": 9,  "name": "Glyphosate 41% SL 1L",      "category": "herbicide",  "price":  390.00, "stock": 110, "description": "Non-selective herbicide for weed control.",           "image_url": "https://placehold.co/400x400/e65100/white?text=Glyphosate",      "rating": 4.3, "brand": "Monsanto"},
    {"id": 10, "name": "Pretilachlor 50% EC 1L",    "category": "herbicide",  "price":  520.00, "stock":  70, "description": "Pre-emergence herbicide for paddy.",                  "image_url": "https://placehold.co/400x400/bf360c/white?text=Pretilachlor",    "rating": 4.5, "brand": "Syngenta"},
    {"id": 11, "name": "Hybrid Paddy Seeds 5kg",    "category": "seeds",      "price":  750.00, "stock":  60, "description": "High-yielding hybrid paddy seeds for Odisha.",       "image_url": "https://placehold.co/400x400/f57f17/white?text=Paddy+Seeds",     "rating": 4.7, "brand": "Pioneer"},
    {"id": 12, "name": "Vegetable Seeds Kit",        "category": "seeds",      "price":  299.00, "stock": 200, "description": "10 varieties - Tomato, Brinjal, Okra and more.",    "image_url": "https://placehold.co/400x400/558b2f/white?text=Veg+Seeds",       "rating": 4.6, "brand": "East-West"},
    {"id": 13, "name": "Knapsack Sprayer 16L",       "category": "equipment",  "price": 1250.00, "stock":  30, "description": "Manual sprayer with adjustable nozzle.",             "image_url": "https://placehold.co/400x400/37474f/white?text=Sprayer+16L",     "rating": 4.8, "brand": "Neptune"},
    {"id": 14, "name": "Battery Sprayer 12L",        "category": "equipment",  "price": 3200.00, "stock":  15, "description": "Rechargeable battery operated sprayer.",             "image_url": "https://placehold.co/400x400/263238/white?text=Battery+Sprayer", "rating": 4.7, "brand": "E-agro"},
]

# ── Helper: safe Supabase call with logging ──────────────────────
def db_insert(table: str, data: dict):
    """Insert into Supabase and log any errors clearly."""
    if not SUPABASE_ENABLED:
        log.warning(f"MOCK MODE: skipping insert into '{table}'")
        return None
    try:
        result = supabase.table(table).insert(data).execute()
        log.info(f"✅ Inserted into '{table}': {result.data}")
        return result.data
    except Exception as e:
        log.error(f"❌ INSERT into '{table}' FAILED: {e}")
        log.error(f"   Data was: {data}")
        raise HTTPException(status_code=500, detail=f"Database insert failed: {str(e)}")

def db_select(table: str, filters: dict = None):
    """Select from Supabase with optional filters."""
    if not SUPABASE_ENABLED:
        return None
    try:
        query = supabase.table(table).select("*")
        if filters:
            for key, val in filters.items():
                query = query.eq(key, val)
        result = query.execute()
        return result.data
    except Exception as e:
        log.error(f"❌ SELECT from '{table}' FAILED: {e}")
        return None

# ── Routes ───────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "shop": "OMM SAI TRADERS",
        "owner": "Prafulla Kumar Sahoo",
        "location": "Bandhabhuin, Nayagarh, Odisha - 752082",
        "gstin": "21FDBPS9893G2Z1",
        "contact": "9937464218",
        "email": "prafullakumar.s978@gmail.com",
        "status": "API Running ✅",
        "supabase": "connected ✅" if SUPABASE_ENABLED else "mock mode ⚠️ (set .env)",
        "docs": "/docs"
    }

@app.get("/health")
def health():
    """Check if Supabase is actually reachable."""
    supabase_status = "disconnected"
    supabase_error = None

    if SUPABASE_ENABLED:
        try:
            # Try a real query to verify connection
            test = supabase.table("products").select("id").limit(1).execute()
            supabase_status = "connected ✅"
        except Exception as e:
            supabase_status = "error ❌"
            supabase_error = str(e)
    else:
        supabase_status = "not configured ⚠️"
        supabase_error = "SUPABASE_URL or SUPABASE_KEY missing in .env"

    return {
        "status": "ok",
        "supabase": supabase_status,
        "supabase_error": supabase_error,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/products")
def get_products(
    category: Optional[str] = Query(None),
    search:   Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
):
    if SUPABASE_ENABLED:
        try:
            query = supabase.table("products").select("*")
            if category:
                query = query.eq("category", category)
            if search:
                query = query.ilike("name", f"%{search}%")
            result = query.execute()
            products = result.data
            log.info(f"Loaded {len(products)} products from Supabase")
        except Exception as e:
            log.error(f"❌ Failed to load products from Supabase: {e}")
            products = MOCK_PRODUCTS
    else:
        products = MOCK_PRODUCTS

    # Price filters
    if min_price is not None:
        products = [p for p in products if p["price"] >= min_price]
    if max_price is not None:
        products = [p for p in products if p["price"] <= max_price]

    # Apply filters manually in mock mode
    if not SUPABASE_ENABLED:
        if category:
            products = [p for p in products if p["category"] == category]
        if search:
            products = [p for p in products if search.lower() in p["name"].lower()]

    return {"products": products, "count": len(products)}

@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    if SUPABASE_ENABLED:
        try:
            result = supabase.table("products").select("*").eq("id", product_id).execute()
            if result.data:
                return result.data[0]
        except Exception as e:
            log.error(f"❌ Failed to get product {product_id}: {e}")

    product = next((p for p in MOCK_PRODUCTS if p["id"] == product_id), None)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/orders")
def create_order(order: Order):
    order_id = f"OMM-{int(datetime.now().timestamp())}"
    log.info(f"New order received: {order_id} from {order.customer_name}")

    if SUPABASE_ENABLED:
        # Step 1: Insert order
        order_data = {
            "order_id":         order_id,
            "customer_name":    order.customer_name,
            "customer_email":   order.customer_email or "",
            "customer_phone":   order.customer_phone,
            "customer_address": order.customer_address,
            "total_amount":     order.total_amount,
            "payment_method":   order.payment_method,
            "notes":            order.notes or "",
            "status":           "pending",
            "created_at":       datetime.now().isoformat()
        }
        try:
            result = supabase.table("orders").insert(order_data).execute()
            db_id = result.data[0]["id"]
            log.info(f"✅ Order saved to DB with id={db_id}")

            # Step 2: Insert order items
            for item in order.items:
                item_data = {
                    "order_id":   db_id,
                    "product_id": item.product_id,
                    "quantity":   item.quantity,
                    "price":      item.price
                }
                supabase.table("order_items").insert(item_data).execute()
                log.info(f"✅ Order item saved: product_id={item.product_id}, qty={item.quantity}")

        except Exception as e:
            log.error(f"❌ Failed to save order to Supabase: {e}")
            # Still return success to customer, but log the error
            log.error("   Order data was: " + str(order_data))

    return {
        "success": True,
        "order_id": order_id,
        "message": f"Order {order_id} placed! We'll call {order.customer_phone} to confirm.",
        "estimated_delivery": "2-3 business days"
    }

@app.post("/api/contact")
def send_contact(msg: ContactMessage):
    log.info(f"Contact message from: {msg.name} / {msg.phone}")

    if SUPABASE_ENABLED:
        contact_data = {
            "name":       msg.name,
            "email":      msg.email or "",
            "phone":      msg.phone or "",
            "message":    msg.message,
            "created_at": datetime.now().isoformat()
        }
        try:
            result = supabase.table("contacts").insert(contact_data).execute()
            log.info(f"✅ Contact message saved to DB: {result.data}")
        except Exception as e:
            log.error(f"❌ Failed to save contact to Supabase: {e}")
            log.error("   Data was: " + str(contact_data))

    return {
        "success": True,
        "message": "Thank you! We'll get back to you within 24 hours."
    }

@app.get("/api/categories")
def get_categories():
    return {
        "categories": [
            {"id": "fertilizer", "name": "Fertilizers", "icon": "🌱", "color": "#22c55e"},
            {"id": "pesticide",  "name": "Pesticides",  "icon": "🧪", "color": "#3b82f6"},
            {"id": "fungicide",  "name": "Fungicides",  "icon": "🍄", "color": "#8b5cf6"},
            {"id": "herbicide",  "name": "Herbicides",  "icon": "🌿", "color": "#f59e0b"},
            {"id": "seeds",      "name": "Seeds",       "icon": "🌾", "color": "#ec4899"},
            {"id": "equipment",  "name": "Equipment",   "icon": "🔧", "color": "#06b6d4"},
        ]
    }

# ── Entry point ──────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*55)
    print("  🌿  OMM SAI TRADERS - API Server")
    print("="*55)
    print(f"  Supabase : {'✅ Connected' if SUPABASE_ENABLED else '⚠️  Mock Mode (check .env)'}")
    print(f"  API Docs : http://localhost:8000/docs")
    print(f"  Health   : http://localhost:8000/health")
    print("="*55 + "\n")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)