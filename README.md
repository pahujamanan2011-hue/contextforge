# 📦 ContextForge

**ContextForge** is a ultra-lightweight, zero-dependency command-line utility built to eliminate prompt engineering friction. It seamlessly scans, filters, and packages an entire project folder into a single, beautifully organized Markdown file designed for Large Language Models (LLMs).

Stop wasting time copy-pasting code file-by-file into ChatGPT, Claude, or local tools like Ollama. Use ContextForge to give AI an exact, structured architecture map and entire file payload of your project in seconds.

---

## ✨ Core Features

- **🚀 Instant Consolidation:** Flattens multiple source code files across deep directory layers into a single `.md` file.
- **🌳 Structure Visualizer:** Automatically builds an text-art directory hierarchy tree at the header of the document so the AI instantly catches your architectural pattern.
- **🔒 Gitignore Enforcement:** Automatically honors your local `.gitignore` specifications alongside strict built-in defaults (skips `node_modules`, python caches, and binary files) to keep context payloads lean.
- **📊 Token Counter Metrics:** Features a built-in content analyzer that calculates absolute character volume and estimates token demands before feeding payloads to AI windows.
- **🎨 Auto-Syntax Recognition:** Detects file extensions natively to frame code outputs within correct structural Markdown markers (`python`, `javascript`, etc.) for seamless parsing.
- **🪶 Pure Python Infrastructure:** Written exclusively with internal native standard libraries. Zero installations or third-party dependencies required.

---

## 🛠️ Get Started

Clone down the repository or grab the `contextforge.py` file directly onto your workstation machine:

```bash
git clone [https://github.com/pahujamanan2011-hue/contextforge.git](https://github.com/pahujamanan2011-hue/contextforge.git)
cd contextforge
```
No additional configuration or package installs are needed. Runs natively on Python 3.8+.
## 🚀 How to Run

### Choose Your Execution Method

You can run ContextForge in two different ways depending on your workflow preference:

#### Option A: The Standard Way (No Setup)



Execute the engine directly from your terminal console, providing target project scopes:
```bash
python contextforge.py [path_to_project] [output_file_name.md]
```

#### Option B: Make it an Executable Shortcut (Recommended)
You can make the script executable so you don't have to type python every time.
 1. Give the file executable permissions:
   ```bash
   chmod +x contextforge.py
   
   ```
 2. Run it using ./:
   ```bash
   ./contextforge.py . context_bundle.md
   
   ```
*(Optional)* If you want to use the tool from **any folder** on your machine by just typing contextforge, move it to your system binaries:
```bash
sudo mv contextforge.py /usr/local/bin/contextforge

```
Now you can simply run:
```bash
contextforge . context_bundle.md

```
```

```



```
### Usage Examples
**Bundle your current working workspace directory:**
```bash
python contextforge.py . context_bundle.md

```
**Target and package a separate workspace pathway safely:**
```bash
python contextforge.py /users/developer/projects/my-web-app output.md

```
## 📂 Layout Blueprint Export Example
Your bundled export file is structured cleanly so AI tools can parse it instantly:
```markdown
# Repository Context: demo-app

## Directory Tree
├── src/
│   ├── app.js
│   └── database.js
├── package.json
└── README.md

## File Contents

### File: `src/app.js`
```javascript
// Internal code files from app.js show up here seamlessly

```
### File: src/database.js
```javascript
// Database script layouts show here

```
```

---

## 📄 Licensing

This project is open-sourced under the terms of the **MIT License**. Check out the accompanying `LICENSE` file details for complete distribution freedoms.

```
