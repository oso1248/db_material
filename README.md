# Instructions
1. Terminal Command: To Clone Repo
    -  ```git clone https://github.com/oso1248/baseAPI.git```

2. Terminal Command: To Create Virtual Environment
    -  ```python3 -m venv venv```

3. Terminal Command: Enter Virtual Enviroment
    -  ```source venv/bin/activate```   Prompt Prepended With: (venv)

4. Terminal Command: In Virtual Environment
    -  ``` pip install -r requirements.txt```

5. Create Database:
    -   In PostgreSQL Create New Database With Desired Name

6. Generate Enviroment Varibles:
    -   Open Project In VsCode
    -   Open File: `api/env_generator.py`
    -   Fill Out Variables
    -   Run file: `api/env_generator.py`

7. Change File Name:
    -   ```env.txt``` to ```.env```

8. Terminal Command: Exit Virtual Enviroment
    -   ```deactivate```

9. Terminal Command: Create Database Tables
    -   ```alembic upgrade head```

10. Terminal Command: Enter Virtual Enviroment
    -   ```source venv/bin/activate```

11. Terminal Command: Start Local Server
    -   ```uvicorn api.main:app --reload```

12. Open In Browser:
    -   http://127.0.0.1:8000/docs