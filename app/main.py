from enum import Enum
from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel
# from typing import Optional

app = FastAPI()

class Difficulty(str, Enum):
  easy="easy"
  medium="medium"
  hard="hard"


class Tour(BaseModel):
  name: str
  slug: str
  summary: str
  description: str
  price: float
  photo: str = "no-photo.jpg"
  difficulty: Difficulty = Difficulty.easy

tours = [{
    "name": "Aburi Tour",
    "slug": "aburi-tour",
    "summary": "A beautiful tour to Aburi",
    "description": "This is one of the most amazing tours ever",
    "price": 44.95,
    "photo": "aburi.jpg",
    "difficulty": Difficulty.medium,
    "id": 1
  },
  {
    "name": "Kumasi Tour",
    "slug": "kumasi-tour",
    "summary": "A beautiful journey to kumasi",
    "description": "This is one of the hardest tours in ghana",
    "price": 100.95,
    "photo": "kumasi.jpg",
    "difficulty": Difficulty.hard,
    "id": 2
  }]

def find_tour(id):
  for tour in tours:
    if tour["id"] == id:
      return tour

def find_tour_index(id):
  for idx,val in enumerate(tours):
    if val["id"] == id:
      return idx

@app.get('/tours')
def get_all_tours():
  return {"status": "success", "count": len(tours), "data": tours}

@app.get('/tours/{id}')
def get_a_tour(id: int):
  tour = find_tour(id)
  if not tour:
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Tour with id {id} not found')
  return {"status": "success", "data": tour}

@app.post('/tours', status_code=status.HTTP_201_CREATED)
def create_new_tour(tour: Tour):
  tour_dict = tour.dict()
  tour_dict["id"] = len(tours) + 1
  tours.append(tour_dict)
  return {"status": "success", "data": tour}

@app.put('/tours/{id}')
def update_tour(id: int, tour: Tour):
  tour_index = find_tour_index(id)
  if tour_index == None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tour with id {id} not found")
  tour_dict = tour.dict()
  tour_dict["id"] = id
  tours[tour_index] = tour_dict
  return {"status": "success", "data": tour_dict}


@app.delete('/tours/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_tour(id: int):
  tour = find_tour(id)
  if not tour:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Tour with id {id} not found")
  tours.remove(tour)
  return Response(status_code=status.HTTP_204_NO_CONTENT)
