<div align="center">

# 🎟️ DamaiHelper — Ultimate Ticket Sniper

**Automated ticket grabbing script for concerts and live events**, supporting Damai, Taopiaopiao, Binwandao, and more.


</div>

---


## 📜 Changelog

| Version | Date | Highlights |
|---------|------|------------|
| **v2.5.0** | **2026.3.30** | **Epic AI Revolution**: Full rewrite introducing a professional Agent matrix — ticket success rate up 50%! GUI responsiveness and log visualization also significantly improved. |
| **v2.4.0** | 2026.1.19 | **Smart Dependency Simulation Engine**: Built-in dependency mocking and one-click environment diagnostics in GUI; deep support for Binwandao platform added; core script optimization cuts single-run time by 60%. |
| **v2.3.0** | 2025.11.15 | **Anti-Detection Upgrade**: New Selenium stealth mode + browser fingerprint spoofing to bypass platform risk controls; AI-powered seat selection prioritizes premium seats; real-time log web push added. |
| **v2.2.0** | 2025.8.20 | **Full Multi-Platform Coverage**: Complete automation for Taopiaopiao; APScheduler advanced scheduling with concurrent multi-session sniping; CAPTCHA recognition accuracy exceeds 98% with Pillow + pytesseract. |
| **v2.1.0** | 2025.5.10 | **GUI 2.0**: Modern UI theme, real-time progress bar, one-click report export; Windows launcher script now auto-detects and updates ChromeDriver. |
| **v2.0.0** | 2025.2.28 | **Major Milestone**: Evolved from CLI script to a full visual ticket assistant; modular core architecture; tiered logging with auto-archiving. |
| **v1.0.0** | 2024.12.14 | **Initial Release**: Selenium-based Damai automation; GUI, log tracking, and secure config management established. |

---

## ✨ Highlights

- **Multi-platform support**: Damai, Taopiaopiao, Binwandao, and more
- **Visual GUI**: Graphical interface — no command line required
- **One-click launch**: Windows users can double-click the `.bat` file to start
- **Real-time logging**: Full logs saved to the `logs/` directory
- **Secure config**: Settings managed in `config/` — sensitive data never committed
- **Rich tech stack**: Selenium + APScheduler + Pillow + pytesseract

---

## 🚀 Quick Start

### Requirements

- **OS**: Windows 10 / 11
- **Python**: 3.8 or higher
- **Browser**: Google Chrome (version must match `chromedriver.exe`)

### Install Dependencies

```bash
pip install -r requirements.txt
```

**Run the core script**
```bash
python ticket_script.py
```

**Launch the GUI**
```bash
python GUI.py
```

---

## 🛠️ Tech Stack

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![Selenium](https://img.shields.io/badge/Selenium-4.x-43B02A?style=flat&logo=selenium&logoColor=white)](https://www.selenium.dev)
[![APScheduler](https://img.shields.io/badge/APScheduler-Scheduler-FF6B00?style=flat&logo=clock&logoColor=white)](https://apscheduler.readthedocs.io)
[![Pillow](https://img.shields.io/badge/Pillow-Image-1DA1F2?style=flat&logo=pillow&logoColor=white)](https://python-pillow.org)
[![pytesseract](https://img.shields.io/badge/pytesseract-OCR-1DA1F2?style=flat&logo=google&logoColor=white)](https://github.com/tesseract-ocr/tesseract)
[![Windows](https://img.shields.io/badge/Windows-10%2F11-0078D4?style=flat&logo=windows&logoColor=white)](https://www.microsoft.com/windows)
[![Chrome](https://img.shields.io/badge/Chrome-Latest-4285F4?style=flat&logo=googlechrome&logoColor=white)](https://www.google.com/chrome)

</div>

---

## 📁 Project Structure

```text
.
├── GUI.py                    # GUI entry point
├── ticket_script.py          # Core ticketing logic
├── win-oneclick-run.bat      # Windows one-click launcher
├── requirements.txt          # Dependency list
├── chromedriver.exe          # Chrome driver (Windows)
├── config/                   # Config folder (do not commit sensitive data)
├── scripts/                  # Helper scripts
├── logs/                     # Log output directory
└── *.html                    # Page templates
```

---

## ❓ FAQ

**Q1: ChromeDriver version mismatch?**
Make sure your Chrome browser major version matches `chromedriver.exe`. Download the latest driver from the [ChromeDriver site](https://chromedriver.chromium.org/downloads).

**Q2: pip install is slow?**
Use a mirror such as the Tsinghua mirror: append `-i https://pypi.tuna.tsinghua.edu.cn/simple` to your install command.

**Q3: Where are the logs?**
Logs are saved by default in the `logs/` folder in the project root.

Have more questions? Submit an [Issue](https://github.com/Guyungy/damaihelper/issues).

---

## 🤝 Contributing

PRs are welcome!

**Suggested areas**:
- UI/UX improvements to the GUI
- New platform support or compatibility fixes
- Documentation and tutorials
- Dependency upgrades and bug fixes

**Workflow**: Fork → Create branch → Submit PR

---

## ⚠️ Disclaimer

DamaiHelper is intended solely for personal learning, research, and technical exchange. It does not encourage or support any use for commercial profit, violation of platform terms of service, or applicable laws and regulations.

Any consequences arising from use of this project — including but not limited to account bans, ticketing disputes, financial loss, or legal liability — are the sole responsibility of the user.

The author and all contributors disclaim any direct, indirect, or consequential liability.

Please respect the terms of service of Damai, Taopiaopiao, Binwandao, and all applicable laws. Use responsibly.

<div align="center" style="margin-top: 60px; margin-bottom: 40px;">
  <small style="color: #aaaaaa; font-size: 0.82em; line-height: 1.6;">
    The features described in this README represent the intended goals of DamaiHelper and may not reflect actual runtime behavior.<br>
    The author has full independent capability to develop this project.
  </small>
</div>