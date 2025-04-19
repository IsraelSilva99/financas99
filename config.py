class Config:
    SECRET_KEY = '5a682626547e2e48a17f925ee1a6efcf'  # Substitua pela chave gerada
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/financas99'  # Adicione a senha aqui se precisar
    SQLALCHEMY_TRACK_MODIFICATIONS = False