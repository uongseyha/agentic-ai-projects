import warnings
from dotenv import load_dotenv
from modules.app import rag_application

load_dotenv()

warnings.warn = lambda *args, **kwargs: None
warnings.filterwarnings('ignore')

if __name__ == "__main__":
    rag_application.launch(server_name="localhost", server_port=7860, share=True)

