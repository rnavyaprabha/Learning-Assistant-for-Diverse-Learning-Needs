# Learning Assistant for Diverse Learning Needs

The **Learning Assistant** leverages **deep learning** to enhance accessibility in classrooms for students with diverse learning challenges. This tool integrates advanced capabilities like **summarization**, **translation**, and **correction**, designed to assist educators and learners alike.

---

## Key Features
- **Real-time Speech-to-Text**: Captures real-time audio input and converts speech into text transcriptions.
- **Summarization**: Generates concise summaries of the transcription provided.
- **Translation**: Provides translations in multiple languages, improving accessibility for non-native speakers.
- **Correction**: Assists with grammar and spelling improvements for clearer notes of the transcription.

---

## Setup Enviroment Variables

1. Add a `.env` file to the app folder.
2. Include the following the keys for OpenAI, Huggin Faces and Google Cloud:
   ```env
   OPENAI_API_KEY=paste-your-openai-key-here
   HF_KEY=paste-your-hugginface-key-here
   GOOGLE_APPLICATION_CREDENTIALS=past-json-folder-location-here
   ```
---

## Steps for Deployment

### **Local Deployment**
1. Install **Docker** on your local machine.
2. Build the Docker image:
   ```
   docker build -t learning-assistant .
3. Run the Docker container:
   ```
   docker run -d -p 8080:8080 --env-file .env learning-assistant
4. Open your browser and navigate to http://localhost:8080 to access the application.

### **Google Cloud Deployment**

1. **Set Up Your Environment**
   - Install the [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) on your local machine.
   - Authenticate with Google Cloud:
     ```bash
     gcloud auth login
     gcloud config set project [PROJECT_ID]
     ```

2. **Prepare Your Docker Image**
   - Tag your Docker image:
     ```bash
     docker tag learning-assistant gcr.io/[PROJECT_ID]/learning-assistant
     ```
   - Push the Docker image to Google Container Registry (GCR):
     ```bash
     docker push gcr.io/[PROJECT_ID]/learning-assistant
     ```

3. **Deploy to Google Cloud Run**
   - Deploy your application to Cloud Run:
     ```bash
     gcloud run deploy learning-assistant \
       --image gcr.io/[PROJECT_ID]/learning-assistant \
       --platform managed \
       --region [REGION] \
       --allow-unauthenticated
     ```
     Replace `[PROJECT_ID]` with your Google Cloud project ID and `[REGION]` with your preferred region (e.g., `us-central1`).

4. **Access Your Deployed Application**
   - Once the deployment completes, Google Cloud Run will provide a URL for your application. Copy and open this URL in your browser to access the application.

### **Notes**
- Ensure your **Dockerfile** includes all required dependencies and is properly set up for FastAPI.
- Configure environment variables, such as API keys, in the **Google Cloud Console** under your Cloud Run service settings.


---

## Technologies Used

- **FastAPI**: For backend API development.
- **Docker**: For containerization and portability.
- **Google Cloud**: For scalable deployment using Cloud Run.

### **Steps to run**
1. cd app
2. Create virtual environment
3. venv\Scripts\activate
4. uvicorn main:app --reload