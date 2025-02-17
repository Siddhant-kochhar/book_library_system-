from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from database import collection
from bson import ObjectId
from fastapi import HTTPException
from typing import Optional

app = FastAPI()

# CORS middleware setup
origins = [
    "http://127.0.0.1:5500",  
    "http://localhost:5500",  
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class BookDetails(BaseModel):
    book_title: Optional[str] = None
    author_name: Optional[str] = None
    genre: Optional[str] = None
    publication_date: Optional[str] = None
    copies_available: Optional[int] = None  


# API to enter book details
@app.post("/books/add_books")
async def create_book_details(user_data: BookDetails):
   
    book_data = user_data.dict()

  
    result = collection.insert_one(book_data)

   
    return {"msg": "Book added successfully!", "book_id": str(result.inserted_id)}


@app.get("/books/details", response_model=List[BookDetails])
async def get_all_book_details():
    books = list(collection.find())

    
    for book in books:
        book["_id"] = str(book["_id"]) 
       
        if "book_title" not in book or "author_name" not in book:
            continue  
    return books


@app.get("/books/details/{book_id}")
async def get_detail_of_specific_book(book_id: str):
    try:
        book_detail = collection.find_one({"_id": ObjectId(book_id)})

        if not book_detail:
            raise HTTPException(status_code=404, detail="Book not found")

        book_detail["_id"] = str(book_detail["_id"])  # Convert ObjectId to string
        return book_detail

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.put("/books/update_details/{book_id}")
async def update_book_details(book_id: str, update_data: BookDetails):
    try:
        book_id = book_id.strip()  
        obj_id = ObjectId(book_id) 

        
        update_dict = {k: v for k, v in update_data.dict().items() if v is not None}

        if not update_dict:
            raise HTTPException(status_code=400, detail="No valid fields to update")

        result = collection.update_one({"_id": obj_id}, {"$set": update_dict})

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Book not found or no changes made")

        return {"msg": "Book updated successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid book_id: {str(e)}")



@app.delete("/books/delete_details/{book_id}")
async def delete_book_data(book_id: str):
    try:
       
        obj_id = ObjectId(book_id)

       
        delete_book = collection.delete_one({"_id": obj_id})

       
        if delete_book.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Book not found")

        return {"msg": "Book deleted successfully"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid book_id: {str(e)}")
