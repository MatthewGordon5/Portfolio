# Forecasting US Economic Trends and Analysing Hotel Customer Satisfaction

This project addresses two real-world business tasks: forecasting US personal consumption expenditure (PCE) and analysing hotel customer reviews to identify key satisfaction drivers. Both tasks were completed using R and compiled into a single business report aimed at guiding management decisions.

---

## 📈 Part 1: Economic Forecasting

The first task involved forecasting seasonally adjusted US personal consumption expenditures using historical data. Three forecasting methods were evaluated:
- **Naïve method** (simple benchmark)
- **Exponential smoothing**
- **ARIMA modelling**

The objective was to identify the most accurate forecasting method for projecting PCE values over the next 12 months. Performance was assessed through visual and statistical comparisons with actual values.

---

## 💬 Part 2: Text Analysis of Hotel Reviews

The second task focused on extracting actionable insights from hotel customer reviews. The dataset consisted of user ratings on a Likert scale (1–5) and accompanying review text.

Key steps:
- Preprocessing and cleaning of text data
- Sampling 2,000 reviews using `dplyr::sample_n()` for performance
- Topic modelling using **Latent Dirichlet Allocation (LDA)** to identify themes in high and low satisfaction reviews

This helped pinpoint the dominant factors influencing both positive and negative customer experiences.

---

## 🧰 Tools & Packages Used

- **R**: Core analysis language
- **Forecasting**: `forecast`, `imputeTS`, `ggplot2`
- **Text Analysis**: `wordcloud`, `topicmodels`, `ldatuning`, `dplyr

---

## 📁 File Structure

- `Code.R` – Combined R code for forecasting and text analysis  
- `PCE.csv` – Seasonally adjusted US PCE data  
- `HotelsData.csv` – Hotel reviews with satisfaction scores  
- `Report.pdf` – Final business report with findings for both tasks  
- `Brief.docx` – Original assignment brief
