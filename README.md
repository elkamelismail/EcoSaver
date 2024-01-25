# EcoSaver

## Getting Started

### Backend Setup

1. Create a virtual environment

```powershell
cd .\back\
```

```powershell
py -m venv venv
```

2. Activate the virtual environment

```powershell
.\venv\Scripts\activate
```

3. Install the dependencies

```powershell
pip install -r .\requirements.txt
```

4. Create a .env file in the back folder and add the following variables

```
SECRET_KEY=your_secret_key
REDIS_URL='redis://127.0.0.1:6379'
```

5. Run the server

```powershell
py .\server.py
```
