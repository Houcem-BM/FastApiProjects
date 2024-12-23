from fastapi import FastAPI, Query
from pycaret.classification import load_model, predict_model
import pandas as pd

# إنشاء التطبيق
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],  # يسمح بالوصول من أي مصدر. قم بتقييد هذا في الإنتاج
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)
# تحميل النموذج المدرب
model = load_model("bestModel")
@app.get("/predict")
async def predict(
  Pregnancies: int = Query(..., description="عدد مرات الحمل "),
  Glucose: int = Query(..., description="مستوى سكر الدم "),
  BloodPressure: int = Query(..., description="ضغط الدم "),
  SkinThickness: int = Query(..., description="سمك الجلد "),
  Insulin: int = Query(..., description="الانسولين "),
  BMI: float = Query(..., description="مؤشر الكتلة "),
  DiabetesPedigreeFunction: float = Query(..., description="تاريخ عائلي لمرض السكري "),
  Age: int = Query(..., description="السن ")
  ):
  # تجميع البيانات في قاموس
  data = {
    "Pregnancies": Pregnancies,
    "Glucose": Glucose,
    "BloodPressure": BloodPressure,
    "SkinThickness": SkinThickness,
    "Insulin": Insulin,
    "BMI": BMI,
    "DiabetesPedigreeFunction": DiabetesPedigreeFunction,
    "Age": Age
       
  }
  
  # تحويل البيانات إلى DataFrame
  df = pd.DataFrame([data])
  # إجراء التنبؤ
  predictions = predict_model(model, data=df)
  # استخراج التنبؤ
  predicted_grade = int(predictions["prediction_label"].iloc[0])
  grade_map={
     0:"NO",
     1:"YES"
   }
  r = grade_map.get(predicted_grade)

  return {"result": r }

