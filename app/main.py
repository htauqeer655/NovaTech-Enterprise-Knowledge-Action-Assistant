from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File,
    Depends,
)
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials,
)
from pydantic import BaseModel

from app.assistant import assistant

from app.auth import (
    hash_password,
    verify_password,
    create_access_token,
    decode_access_token,
)

from app.database import (
    get_connection,
    initialize_database,
)

from app.index_documents import (
    index_new_documents,
)

app = FastAPI(
    title="NovaTech Enterprise Knowledge & Action Assistant",
    version="1.0.0"
)

UPLOAD_DIR = Path("data/documents")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)

initialize_database()

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    payload = decode_access_token(token)

    if payload is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token."
        )

    username = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=401,
            detail="Invalid authentication token."
        )

    return username


class ChatRequest(BaseModel):
    question: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    answer: str


class RegisterRequest(BaseModel):
    username: str
    password: str


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


@app.get("/")
def root():
    return {
        "message": "NovaTech Enterprise Assistant API is running."
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/register")
def register(
    request: RegisterRequest
):

    username = request.username.strip()

    if not username:
        raise HTTPException(
            status_code=400,
            detail="Username is required."
        )

    if len(request.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters."
        )

    connection = get_connection()

    existing_user = connection.execute(
        """
        SELECT id
        FROM users
        WHERE username = ?
        """,
        (username,)
    ).fetchone()

    if existing_user:
        connection.close()

        raise HTTPException(
            status_code=409,
            detail="Username already exists."
        )

    password_hash = hash_password(
        request.password
    )

    connection.execute(
        """
        INSERT INTO users (
            username,
            password_hash
        )
        VALUES (?, ?)
        """,
        (
            username,
            password_hash,
        )
    )

    connection.commit()

    connection.close()

    return {
        "success": True,
        "message": "User registered successfully.",
        "username": username,
    }


@app.post(
    "/login",
    response_model=TokenResponse
)
def login(
    request: LoginRequest
):

    connection = get_connection()

    user = connection.execute(
        """
        SELECT *
        FROM users
        WHERE username = ?
        """,
        (request.username.strip(),)
    ).fetchone()

    connection.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    if not verify_password(
        request.password,
        user["password_hash"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password."
        )

    token = create_access_token(
        {
            "sub": user["username"]
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    current_user: str = Depends(
        get_current_user
    )
):

    try:
        answer = assistant(
            request.question,
            session_id=f"{current_user}:{request.session_id}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Something went wrong: {e}"
        )

    return {
        "answer": answer
    }


@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: str = Depends(
        get_current_user
    )
):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No filename provided."
        )

    allowed_extensions = {
        ".pdf",
        ".docx"
    }

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail="Only PDF and DOCX files are supported."
        )

    safe_filename = Path(
        file.filename
    ).name

    destination = UPLOAD_DIR / safe_filename

    content = await file.read()

    with open(
        destination,
        "wb"
    ) as f:
        f.write(content)

    try:
        index_new_documents()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=(
                "Document uploaded but "
                f"indexing failed: {e}"
            )
        )

    return {
        "success": True,
        "filename": safe_filename,
        "message": (
            "Document uploaded and "
            "indexed successfully."
        ),
        "path": str(destination),
        "uploaded_by": current_user,
    }