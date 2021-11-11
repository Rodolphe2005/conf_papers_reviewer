from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from create_db import Papers, User, engine, UserInteractions
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/next_paper_to_check/{user_id}")
def next_paper_to_check(user_id: int):
    with Session(engine) as session:
        user = session.query(User).filter(User.id == user_id).one()
        papers_ids_viewed = [user_interaction.paper_id for user_interaction in session.query(UserInteractions.paper_id).filter(UserInteractions.user_id == user_id)]
        all_paper_ids = [paper.id for paper in session.query(Papers.id).all()]
        eligible_papers_ids = set(all_paper_ids).difference(set(papers_ids_viewed))
        chosen_paper_id = list(eligible_papers_ids)[0]
        chosen_paper = session.query(Papers).filter(Papers.id == chosen_paper_id).one()
        return {
            'paper_id': chosen_paper.id,
            'title': chosen_paper.title,
            'abstract': chosen_paper.abstract
        }

@app.get("/save_user_interaction/{user_id}/{paper_id}/{decision}")
def save_user_interaction(user_id: int, paper_id: int, decision: str):
    with Session(engine) as session:
        user_interaction = UserInteractions(
            user_id=user_id, 
            paper_id=paper_id,
            decision=decision)
        session.add(user_interaction)
        session.flush()
        session.commit()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)