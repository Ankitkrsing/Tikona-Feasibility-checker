# 🚀 Tikona Feasibility Checker

<div align="center">

A fast and efficient tool to check the feasibility of network locations based on TDN network coverage and distance metrics.

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-App-red)
![Status](https://img.shields.io/badge/Status-Active-success)

🔗 **Live Demo:** https://your-app-link.streamlit.app

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Tech Stack](#tech-stack)

</div>

---

## 📋 Project Description

**Tikona Feasibility Checker** is a web-based application designed for network engineers to quickly validate the feasibility of proposed locations within the TDN (Tikona Direct Network) infrastructure.

The tool automates **distance-based feasibility checks** across bulk location datasets, reducing manual effort and enabling faster decision-making for network expansion and planning.

---

## 📈 Business Impact

- ⏱️ Reduced manual feasibility checking time by up to **80%**
- 📊 Handles **8000+ location datasets** efficiently
- ⚡ Enables quick and data-driven decision-making
- 🎯 Improves accuracy in telecom network planning

---

## ✨ Features

- 📂 **Bulk Location Upload** – Process multiple locations at once  
- 📄 **Excel/CSV Support** – Works with `.xlsx` and `.csv` files  
- 📍 **Distance-Based Logic** – Automated feasibility calculation  
- ⚡ **Fast Processing** – Optimized for large datasets  
- 🖥️ **Simple UI** – Built with Streamlit  
- 📊 **Clear Results** – Feasible / Not Feasible output  
- 📥 **Export Option** – Download results in Excel/CSV  

---

## ⚙️ How It Works

1. Upload location dataset (CSV/Excel)  
2. Extract latitude & longitude  
3. Calculate distance from TDN network nodes  
4. Compare with threshold distance  
5. Mark locations as **Feasible / Not Feasible**  

---

## 🎯 Use Cases

- Telecom Network Planning  
- Site Feasibility Analysis  
- Infrastructure Expansion  
- Data-driven Network Optimization  

---

## 🚀 Installation

### Prerequisites
- Python 3.8+
- pip

### Setup Steps

```bash
# Clone repository
git clone https://github.com/Ankitkrsing/Tikona-Feasibility-checker.git

# Go to project folder
cd Tikona-Feasibility-checker

# Create virtual environment (optional)
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## 💻 Usage

### Running the Application

1. **Start the Streamlit Server**
   ```bash
   streamlit run app.py
   ```

2. **Access the Web Interface**
   - Open your browser and navigate to `http://localhost:8501`
   - The application will automatically reload when code changes

### Using the Tool

1. **Upload Your Data**
   - Click "Browse files" and select your Excel or CSV file
   - Ensure your file contains required columns: Location Name, Latitude, Longitude

2. **Configure Parameters**
   - Set distance threshold and other feasibility parameters as needed
   - Review the configuration preview

3. **Run Feasibility Check**
   - Click the "Check Feasibility" button
   - Wait for processing to complete

4. **Review Results**
   - View feasibility results in the dashboard
   - Download results as Excel or CSV file

### Example Input Format

| Location Name | Latitude | Longitude | Site Type |
|---|---|---|---|
| Site-A-Mumbai | 19.0760 | 72.8777 | Tower |
| Site-B-Delhi | 28.7041 | 77.1025 | Facility |
| Site-C-Bangalore | 12.9716 | 77.5946 | Tower |

---

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| **Python 3.8+** | Core programming language |
| **Streamlit** | Web application framework |
| **Pandas** | Data manipulation and analysis |
| **OpenPyXL** | Excel file handling |

---

## 📸 Screenshots

### Dashboard Overview
![Dashboard Overview](https://via.placeholder.com/800x400?text=Dashboard+Overview)

### Results Display
![Results Display](https://via.placeholder.com/800x400?text=Results+Display)

### Data Upload Interface
![Upload Interface](https://via.placeholder.com/800x400?text=Upload+Interface)

*Replace placeholder images with actual screenshots of your application*

---

## 📦 Project Structure

```
tikona-feasibility-checker/
├── app.py                  # Main Streamlit application
├── requirements.txt        # Project dependencies
├── README.md              # This file
├── data/                  # Sample data files
│   └── sample_locations.csv
└── utils/                 # Utility modules (if applicable)
    └── feasibility.py     # Feasibility logic
```

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Ankit Kumar Singh**
- GitHub: [@Ankitkrsing](https://github.com/Ankitkrsing)
- LinkedIn: www.linkedin.com/in/ankit-singh-704a47287

---

## 🆘 Support & Feedback

If you encounter any issues or have suggestions for improvement:

- 📧 Open an issue on [GitHub Issues](https://github.com/Ankitkrsing/Tikona-Feasibility-checker/issues)
- 💬 Start a discussion on [GitHub Discussions](https://github.com/Ankitkrsing/Tikona-Feasibility-checker/discussions)

---

## 🙏 Acknowledgments

- Thanks to the TDN network team for infrastructure specifications
- Streamlit community for excellent documentation and support
- All contributors who have helped with feedback and improvements

---

<div align="center">

Made with ❤️ for Network Engineers

[⬆ Back to Top](#tikona-feasibility-checker)

</div>
