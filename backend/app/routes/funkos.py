from fastapi import APIRouter, HTTPException, Query, Path
from bson import ObjectId
from datetime import datetime
from app.database import funkos_collection
from app.models.funkos import FunkoCreate

router = APIRouter()


@router.post("/")
def create_funko(funko: FunkoCreate):
    try:
        doc = funko.dict()
        doc["created_at"] = datetime.utcnow()
        result = funkos_collection.insert_one(doc)
        doc["_id"] = str(result.inserted_id)
        return {"status": "ok", "data": doc}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_funkos(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Récupère les Funkos avec pagination.
    - page: numéro de page (1-based)
    - limit: nombre de Funkos par page
    """
    try:
        skip_count = (page - 1) * limit
        funkos_cursor = funkos_collection.find({}).skip(skip_count).limit(limit)

        funkos_list = []
        for f in funkos_cursor:
            f["_id"] = str(f["_id"])
            funkos_list.append(f)

        total_count = funkos_collection.count_documents({})

        return {
            "status": "ok",
            "page": page,
            "limit": limit,
            "total": total_count,
            "data": funkos_list
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/barcode/{barcode}")
def get_funko_by_barcode(barcode: str):
    try:
        funko = funkos_collection.find_one({"barcode": barcode}, {"_id": 0})
        if not funko:
            raise HTTPException(status_code=404, detail="Funko non trouvé")
        return {"status": "ok", "data": funko}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{funko_id}")
def update_funko(funko_id: str, funko_data: dict):
    """
    Met à jour une Funko par son _id.
    funko_id : str (ObjectId en string)
    funko_data : dict contenant les champs à mettre à jour
    """
    try:
        print(funko_id)
        obj_id = ObjectId(funko_id)  # conversion string -> ObjectId
        print(obj_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID invalide")

    result = funkos_collection.update_one({"_id": obj_id}, {"$set": funko_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Funko non trouvée")

    updated_funko = funkos_collection.find_one({"_id": obj_id})
    updated_funko["_id"] = str(updated_funko["_id"])
    return {"status": "ok", "data": updated_funko}
