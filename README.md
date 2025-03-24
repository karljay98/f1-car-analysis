# 🏎️ F1 Data Visualisation & Analysis Project

This project is a Python-based data pipeline and visualization tool that fetches real-time Formula 1 race data using the **Ergast Developer API**, stores it in a **SQLite database**, and generates insightful **visualizations** using `matplotlib` and `pandas`. It’s a compact, script-based dashboard designed for motorsport fans, analysts, or data enthusiasts.

---

## 📦 Project Components

### 1. **Data Source – Ergast API**

The project pulls live race results from the [Ergast Developer API](https://ergast.com/mrd/), which provides a public RESTful interface for historical and real-time Formula 1 data. This includes:
- Race results
- Drivers and constructors
- Points scored
- Race rounds and dates

The specific endpoint used is:

