# 🥗 NutriDiet AI

### 🤖 Personalized Nutrition. Powered by AI.

NutriDiet AI is an AI-powered personalized diet plan generator that analyzes health data, medical reports, lifestyle habits, dietary preferences, and health goals to generate intelligent and customized nutrition plans.

The project combines **Machine Learning, Natural Language Processing (NLP), OCR, and Generative AI** to transform complex health information into actionable dietary recommendations.

---

## 🌟 Features

* 🧬 **Personalized Diet Plans**
  Generates diet recommendations based on individual health profiles.

* 📄 **Medical Report Analysis**
  Extracts relevant health information from medical reports and documents.

* 🧠 **Machine Learning-Based Health Analysis**
  Uses ML models to analyze patient data and identify relevant health conditions.

* 🔤 **NLP-Powered Medical Text Processing**
  Processes medical notes, prescriptions, and other unstructured health-related text.

* 🤖 **Generative AI Recommendations**
  Converts analyzed health information into personalized dietary guidelines.

* 🥗 **Nutrition Planning**
  Provides recommendations for calories, protein, carbohydrates, fats, fiber, and other nutritional requirements.

* 📊 **Data-Driven Insights**
  Uses structured health data and lifestyle information to create more personalized recommendations.

---

## 🔄 How It Works

```text
User Health Data / Medical Reports
              ↓
      Data Extraction & OCR
              ↓
      Data Cleaning & Processing
              ↓
       NLP & Medical Analysis
              ↓
      Machine Learning Prediction
              ↓
     Personalized Nutrition Logic
              ↓
        Generative AI Processing
              ↓
       Customized Diet Plan
```

---

## 🧠 Technologies Used

### Programming Language

* Python

### Machine Learning

* Scikit-learn
* XGBoost
* Random Forest
* LightGBM

### Natural Language Processing

* NLTK
* Transformers
* BERT-based Models
* Clinical NLP Techniques

### OCR & Document Processing

* Tesseract OCR
* PaddleOCR
* PyPDF2
* pdfplumber
* PIL

### Generative AI

* Large Language Models for personalized diet recommendations

### Data Processing & Visualization

* Pandas
* NumPy
* Matplotlib
* Plotly

### Deployment

* Streamlit

---

## 📊 Input Data

NutriDiet AI can work with various types of health and lifestyle information, including:

* Age and gender
* Height and weight
* BMI and body composition
* Blood glucose levels
* HbA1c
* Cholesterol levels
* LDL and HDL
* Triglycerides
* Serum creatinine
* Vitamin levels
* Medical conditions
* Medications
* Dietary preferences
* Food intolerances
* Activity level
* Sleep duration
* Stress level
* Health goals

---

## 🥗 Example Output

Based on the user's health profile, NutriDiet AI can generate personalized recommendations such as:

* Daily calorie requirements
* Protein, carbohydrate, and fat targets
* Recommended foods
* Foods to limit or avoid
* Meal suggestions
* Lifestyle recommendations
* Condition-specific dietary guidelines

---

## 🏗️ Project Architecture

```text
                    ┌──────────────────────┐
                    │    User Input Data    │
                    │  Medical Reports/Data  │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Data Extraction Layer │
                    │   OCR & PDF Parsing   │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │  Data Preprocessing  │
                    │ Cleaning & Formatting │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   NLP Processing     │
                    │ Medical Text Analysis│
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │   ML Prediction      │
                    │ Health Condition     │
                    │      Analysis        │
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │ Personalized Diet   │
                    │ Recommendation Engine│
                    └──────────┬───────────┘
                               ↓
                    ┌──────────────────────┐
                    │    NutriDiet AI      │
                    │   Generated Plan     │
                    └──────────────────────┘
```

---

## 📁 Project Structure

```text
NutriDiet-AI/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── models/
│
├── notebooks/
│
├── src/
│   ├── data_processing.py
│   ├── ml_predictor.py
│   ├── nlp_processor.py
│   └── diet_generator.py
│
├── app.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/NutriDiet-AI.git
cd NutriDiet-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the environment:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run app.py
```

---

## 🔮 Future Enhancements

* 📱 Mobile application
* 🧬 More advanced medical NLP models
* 🥘 Indian food recognition and nutrition estimation
* 📸 Image-based food analysis
* 📈 Long-term nutrition tracking
* 🔔 Personalized meal reminders
* 🩺 Integration with wearable health devices
* 🌍 Support for multiple cuisines and languages
* 📊 Advanced health analytics dashboard

---

## ⚠️ Disclaimer

NutriDiet AI is an educational and research-oriented project. The generated diet recommendations should not replace professional medical advice, diagnosis, or treatment from qualified healthcare professionals.

---

## 👨‍💻 Author

Developed with ❤️ using **Python, Machine Learning, NLP, and Generative AI**.

---

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub!
