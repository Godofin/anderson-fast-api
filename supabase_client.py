import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

url: str = "https://ghnqlsnjbeckzxidfesh.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImdobnFsc25qYmVja3p4aWRmZXNoIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjAxMDAyMjgsImV4cCI6MjA3NTY3NjIyOH0.ey9UD0CNm4vByVhZ6oSfgmZxXV9Ma6GVC_8aYbh1N7g"

# Cria uma única instância do cliente Supabase para ser usada em toda a aplicação
try:
    supabase: Client = create_client(url, key)
    print("Conexão com Supabase bem-sucedida!")
except Exception as e:
    print(f"Erro ao inicializar o cliente Supabase: {e}")
    supabase = None

