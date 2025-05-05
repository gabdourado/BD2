# Criação do Ambiente Virtual

sudo apt install python3-venv

python3 -m venv venv

source venv/bin/activate

pip install fastapi uvicorn mysqlclient python-dotenv

uvicorn main:app --reload