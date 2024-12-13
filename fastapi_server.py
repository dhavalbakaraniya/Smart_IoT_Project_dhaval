from fastapi import FastAPI

app = FastAPI()

# Global variable to store the latest moisture value
latest_moisture_value = "No Data Yet"

@app.get("/humidity")
def read_humidity():
    return {"moisture_value": latest_moisture_value}
