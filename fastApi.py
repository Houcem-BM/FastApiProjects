#import library
from fastapi import FastAPI, Query
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


class BMIOutput(BaseModel):
    bmi: float
    message : str



# Create API app
app = FastAPI()

app.add_middleware(CORSMiddleware,
    allow_origins=["*"],  allow_methods=["*"],allow_headers=["*"],
)



# Determine the main path
@app.get("/")

#Determine the path function
def Hi():
    return {"message": "Welcome"}

@app.get("/calculate_bmi")
def calculate_bmi(
    weight: float= Query(..., gt=20, lt= 200, description="الوزن بالكيلوغرام"),
    height: float= Query(..., gt=1, lt= 3, description="الطول بالمتر")):
 
    bmi = weight / (height ** 2)

    if bmi < 18.5:
        message = "لديك نقص في الوزن، كُل أكثر"
    elif 18.5 <= bmi < 25:
        message = "لديك وزن طبيعي، حافظ عليه"
    elif 25 <= bmi < 30:
        message = "لديك زيادة في الوزن، تمرن أكثر"
    else:
        message = "أنت تعاني من السمنة، قم بمراجعة طبيب"
    #result = BMIOutput(bmi= bmi, message = message)
    #print(f"result:{result}")

    #return result
    return BMIOutput(bmi= bmi, message = message)
