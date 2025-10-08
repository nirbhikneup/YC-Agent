# 🤖 AI Setup Guide for YC Company Explorer

## 🚀 **What's New: AI-Powered Features**

This version includes AI analysis powered by the **Hugging Face hosted Meta LLaMA 3 80B Instruct** model, making it a true **Software + AI** project perfect for your resume!

## 🎯 **AI Features Added:**

### **🧠 AI Analysis Tab**
- **Market Analysis** - AI analyzes YC company trends
- **Investment Recommendations** - AI suggests investment opportunities  
- **Industry Trends** - AI identifies market patterns
- **Company Insights** - AI provides business intelligence
- **Custom Queries** - Ask AI anything about the data

### **💬 AI Chat Interface**
- Interactive chat with AI about YC companies
- Natural language queries
- Real-time AI responses

### **🎯 AI-Powered Recommendations**
- Top AI/ML companies
- High-value investment targets
- Contact-rich companies for partnerships

## 🛠️ **Local Setup (For Full AI Features)**

### **Step 1: Create a Hugging Face account**
- Sign up at [https://huggingface.co](https://huggingface.co) (free tier works!)

### **Step 2: Generate an access token**
1. Visit [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)
2. Click **Create new token**
3. Choose **Read** permissions and copy the token value

### **Step 3: Configure your environment**
Set the token as an environment variable before launching Streamlit:

```bash
export HUGGINGFACE_API_TOKEN="hf_your_token_here"
# Optional: override the default 80B model with another Inference API model
export HUGGINGFACE_MODEL_ID="meta-llama/Meta-Llama-3-80B-Instruct"
```

### **Step 4: Install dependencies and run the app**
```bash
pip install -r requirements-ai.txt
streamlit run streamlit_ai.py
```

## ☁️ **Streamlit Cloud Deployment**

The deployed app uses the real Hugging Face LLaMA 3 80B backend. Configure Streamlit secrets like this:

1. In Streamlit Cloud, open **App settings → Secrets**
2. Add the following content:
   ```toml
   HUGGINGFACE_API_TOKEN = "hf_your_token_here"
   HUGGINGFACE_MODEL_ID = "meta-llama/Meta-Llama-3-80B-Instruct"
   ```
3. Deploy with `streamlit_ai.py` as the main file and `requirements-ai.txt` as the dependency list

## 🎨 **UI Improvements**

- **Gradient AI boxes** for AI responses
- **Better styling** with AI-themed colors
- **No duplicate key errors** - completely fixed
- **Cleaner interface** with proper separation

## 🔧 **Technical Improvements**

- **Fixed all Streamlit errors** - no more duplicate keys
- **Better performance** with proper caching
- **Cleaner code structure** 
- **Production-ready** error handling

## 🎯 **For Your Resume**

This is now a **Software + AI** project that demonstrates:

- **Full-stack development** (backend + frontend)
- **AI integration** with LLM models
- **Data analysis** and visualization
- **Cloud deployment** and DevOps
- **Modern tech stack** (Python, Streamlit, AI/ML)

## 🚀 **Deploy the AI Version**

1. **Create new Streamlit app**
2. **Repository**: `nirbhikneup/YC-Agent`
3. **Main file**: `streamlit_ai.py`
4. **Requirements**: `requirements-ai.txt`
5. **Deploy!**

The AI version is much more impressive and will stand out on your resume! 🤖✨
