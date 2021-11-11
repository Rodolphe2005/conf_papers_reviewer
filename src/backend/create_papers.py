from sqlalchemy.orm import Session
from create_db import engine, Papers

with Session(engine) as session:
    for i in range(20):
        new_paper = Papers(title=f'title {i}', abstract=f'abstract {i}')
        session.add(new_paper)
    session.flush()
    session.commit()