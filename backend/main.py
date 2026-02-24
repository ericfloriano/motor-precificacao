from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import timedelta
import models, schemas, auth, calculos
from database import engine, get_db
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Motor de Precificação API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "Motor de Precificação API Online e Operante"}

# --- AUTH ENDPOINTS ---
@app.post("/api/v1/auth/register", response_model=schemas.UserOut)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    allowed_domain = os.getenv("ALLOWED_EMAIL_DOMAIN", "@empresa.com.br")
    if not user.email.lower().endswith(allowed_domain):
        raise HTTPException(status_code=400, detail=f"Cadastro restrito a e-mails institucionais ({allowed_domain}).")
    
    expected_invite = os.getenv("INVITE_CODE", "DEFAULT_SECRET_KEY")
    if user.invite_code != expected_invite:
        raise HTTPException(status_code=400, detail="Código de convite inválido ou expirado.")

    db_user = auth.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="E-mail já registrado")
    hashed_password = auth.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        is_admin=user.is_admin
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/api/v1/auth/token", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.UserCreate, db: Session = Depends(get_db)):
    # Note: we are taking UserCreate for simplicity in json, 
    # usually OAuth2PasswordRequestForm is used, but React is easier with JSON
    user = auth.get_user_by_email(db, email=form_data.email)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/v1/auth/me", response_model=schemas.UserOut)
def read_users_me(current_user: models.User = Depends(auth.get_current_user)):
    return current_user

# --- ADMIN ENDPOINTS ---
@app.get("/api/v1/admin/users", response_model=list[schemas.UserOut])
def get_all_users(db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    users = db.query(models.User).all()
    return users

@app.put("/api/v1/admin/users/{user_id}", response_model=schemas.UserOut)
def update_user(user_id: int, user_update: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    user.full_name = user_update.full_name
    user.email = user_update.email
    user.is_admin = user_update.is_admin
    if user_update.password:
        user.hashed_password = auth.get_password_hash(user_update.password)
    db.commit()
    db.refresh(user)
    return user

@app.delete("/api/v1/admin/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_admin_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    db.delete(user)
    db.commit()
    return {"status": "success", "message": "Usuário deletado"}

# --- PRICING ENDPOINTS ---
@app.post("/api/v1/calculate")
def calculate_pricing(
    payload: schemas.PricingInput, 
    db: Session = Depends(get_db), 
    current_user: models.User = Depends(auth.get_current_user)
):
    import random
    import string
    
    resultado = calculos.precificar(payload.model_dump())
    
    now_brt = models.get_local_time()
    random_str = ''.join(random.choices(string.digits, k=6))
    new_protocolo = f"{now_brt.strftime('%d%m%Y')}-{random_str}"
    
    # Save to history
    history_entry = models.PricingHistory(
        protocolo=new_protocolo,
        owner_id=current_user.id,
        created_at=now_brt,
        **payload.model_dump(),
        **resultado
    )
    db.add(history_entry)
    db.commit()
    db.refresh(history_entry)
    
    return {"status": "success", "data": history_entry}

@app.get("/api/v1/history")
def get_pricing_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if current_user.is_admin:
        pricings = db.query(models.PricingHistory).order_by(models.PricingHistory.created_at.desc()).all()
    else:
        pricings = db.query(models.PricingHistory).filter(models.PricingHistory.owner_id == current_user.id).order_by(models.PricingHistory.created_at.desc()).all()
    
    results = []
    for p in pricings:
        p_dict = {k: v for k, v in p.__dict__.items() if not k.startswith('_')}
        p_dict['owner_name'] = p.owner.full_name if p.owner else "Desconhecido"
        results.append(p_dict)
        
    return results

@app.delete("/api/v1/history/{history_id}")
def delete_pricing_history(
    history_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_admin_user)
):
    pricing = db.query(models.PricingHistory).filter(models.PricingHistory.id == history_id).first()
    if not pricing:
        raise HTTPException(status_code=404, detail="Cotação não encontrada")
    db.delete(pricing)
    db.commit()
    return {"message": "Cotação deletada com sucesso"}

from fastapi.responses import StreamingResponse
import export

@app.get("/api/v1/export/pdf/{pricing_id}")
def export_pricing_pdf(pricing_id: int, db: Session = Depends(get_db)):
    pricing = db.query(models.PricingHistory).filter(models.PricingHistory.id == pricing_id).first()
    if not pricing:
        raise HTTPException(status_code=404, detail="Precificação não encontrada")
    
    # We will use __dict__ representation of model and just pop internal sqlalchemy stuff 
    data_dict = {k: v for k, v in pricing.__dict__.items() if not k.startswith('_')}
    
    # Get Author Name
    author = db.query(models.User).filter(models.User.id == pricing.owner_id).first()
    author_name = author.full_name if author else "Consultor"

    pdf_file = export.export_to_pdf(data_dict, author_name=author_name)
    
    return StreamingResponse(
        pdf_file, 
        media_type="application/pdf", 
        headers={"Content-Disposition": f"attachment; filename=Precificacao_{pricing_id}.pdf"}
    )

@app.get("/api/v1/export/excel/{pricing_id}")
def export_pricing_excel(pricing_id: int, db: Session = Depends(get_db)):
    pricing = db.query(models.PricingHistory).filter(models.PricingHistory.id == pricing_id).first()
    if not pricing:
        raise HTTPException(status_code=404, detail="Precificação não encontrada")
    
    data_dict = {k: v for k, v in pricing.__dict__.items() if not k.startswith('_')}
    excel_file = export.export_to_excel(data_dict)
    
    return StreamingResponse(
        excel_file, 
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
        headers={"Content-Disposition": f"attachment; filename=Precificacao_{pricing_id}.xlsx"}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
