# 🗺️ U.S. State Map Generator

This project creates **publication-ready choropleth maps** of all U.S. states using user-provided data.  
It automatically downloads the U.S. shapefile from GitHub and produces a `.png` map showing your numeric data (e.g., income, tax rate, etc.) across states.

---

## 🧩 **Features**

- Works on any computer with Python or Conda  
- No manual download of shapefiles — everything loads automatically  
- Clean and consistent fonts, colorbar, and styling  
- Customizable color scale and titles  
- Missing data automatically shown in grey  

---

## ⚙️ **Setup Instructions**

### 1️⃣ Clone this repository
```bash
git clone https://github.com/kalyanidhusia/geomap.git
cd geomap
```

### 2️⃣ Create and activate the environment
Using **Conda** (recommended):

```bash
conda create -n geomap python=3.11 --file requirements.txt
conda activate geomap
```

Or using **pip**:
```bash
pip install -r requirements.txt
```

---

## 🧾 **Input File Format**

The input file should be a **tab-separated text file (`.txt`)** with at least these two columns:

| Column | Description |
|---------|--------------|
| `State` | Full state name (must match Census shapefile names) |
| `<Value>` | Numeric data to be plotted (e.g., income, tax burden, rate, etc.) |

### 🧱 Example — `data.txt`
```
State	Property_Tax_Burden
Idaho	2.12
Montana	3.24
North Dakota	2.44
South Dakota	2.58
Wyoming	3.10
```

Or use the full mock dataset `data.txt` with all 50 states provided in this repo.

---

## ▶️ **How to Run**

Run the script from the command line:

```bash
python plot_us_state_map.py --data data.txt --value_column Property_Tax_Burden
```

### Optional arguments:
| Flag | Description | Default |
|------|--------------|----------|
| `--data` | Path to your input file | **required** |
| `--value_column` | Column name to visualize | **required** |
| `--output` | Name of the output image file | `us_state_map.png` |

---

## 🖼️ **Output**

- The map will be saved automatically as a `.png` file in your working directory.  
- Example output file: `Property_Tax_Burden_Map.png`  
- Colored states represent data values, grey states have missing data.  
- The map includes:
  - White state borders  
  - Data labels (state abbreviations + values)  
  - Smooth color gradient legend  

---

## 🌎 **Example Run**

```bash
python plot_us_state_map.py \
  --data data.txt \
  --value_column Per_Capita_Income \
  --output PerCapitaIncome_Map.png
```

✅ Output saved as:
```
PerCapitaIncome_Map.png
```

---

## 📦 **Repository Contents**

```
geomap/
 ├── plot_us_state_map.py        # Main script
 ├── requirements.txt            # Required Python packages
 ├── data.txt                    # Example input file
 ├── README.md                   # Instructions
 └── state_geo_files/            # (Optional local shapefiles, auto-downloaded if missing)
```

---

## 🙌 **Credits**

Created and maintained by **[Kalyani Dhusia](https://github.com/kalyanidhusia)**  
Shapefile source: [U.S. Census Bureau 2018 Cartographic Boundary Files](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.html)
