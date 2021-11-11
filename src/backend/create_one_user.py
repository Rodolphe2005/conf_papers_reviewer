from sqlalchemy import select
from sqlalchemy.orm import Session
from create_db import User, engine

with Session(engine) as session:
    results = session.execute(select(User).where(User.name == 'Rodolphe'))
    num_results = len(list(results))
    print(num_results)
    if num_results == 0:
        print('Add user')
        new_user = User(name='Rodolphe')
        session.add(new_user)
        session.flush()
        session.commit()
    else:
        print('Already there')
