import psycopg2
from dotenv import load_dotenv
from os import getenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

conn = None   # Conexão com o banco de destino (DB1)
conn2 = None  # Conexão com o banco de origem (DB2)

try:  
    # --- Conexão com o banco de destino ---
    conn = psycopg2.connect(
        dbname=getenv("DB1_NAME"),
        user=getenv("DB1_USER"),
        password=getenv("DB1_PASSWORD"),
        host=getenv("DB1_HOST"),
        port=getenv("DB1_PORT")
    )
    cur1 = conn.cursor()  # Cursor para executar comandos no DB1

    # --- Conexão com o banco de origem ---
    conn2 = psycopg2.connect(
        dbname=getenv("DB2_NAME"),
        user=getenv("DB2_USER"),
        password=getenv("DB2_PASSWORD"),
        host=getenv("DB2_HOST"),
        port=getenv("DB2_PORT")
    )
    cur2 = conn2.cursor()  # Cursor para executar comandos no DB2

    # Garante que não haja transações pendentes
    conn2.rollback()
    conn.rollback()
    print("Conexão com o banco feita com sucesso!")

    # --- Migração de Plan_temp (Tabela de planos) ---
    try:
        print("Migrando Plan_temp")
        # Seleciona dados do banco de origem
        cur2.execute("select idplano, nvalor, nativo, cnmplano from plano")
        plan_temp = cur2.fetchall()

        # Cria tabela temporária no banco de destino
        cur1.execute("DROP TABLE IF EXISTS Plan_temp")
        cur1.execute("""
        CREATE TABLE Plan_temp (
            idPlan INT,
            nPrice NUMERIC,
            cActive VARCHAR(50),
            cPlanName VARCHAR(255),
            nActive CHAR(1) DEFAULT '1'
        )
        """)

        # Insere os dados extraídos na tabela temporária
        insert_query = "INSERT INTO Plan_temp (idPlan, nPrice, cActive, cPlanName, nActive) VALUES (%s,%s,%s,%s,DEFAULT)"
        cur1.executemany(insert_query, plan_temp)
        conn.commit()

        # Executa a procedure par atualizar a tabela de UpdatePlan com os dados da temporária 
        print("Executando SP_UpdatePlan()")
        cur1.execute("CALL SP_UpdatePlan()")
        conn.commit()
        print("SP_UpdatePlan executada com sucesso.")
    except psycopg2.Error as e:
        # Em caso de erro, realiza rollback
        print(f"Erro na migração Plan_temp: {e}")
        conn.rollback()

    # --- Migração de IndustryType_temp (Tipos de indústria) ---
    try:
        print("Migrando IndustryType_temp")
        cur2.execute("select idtipoindustria, cnmtipoindustria, cdescricao from tipoindustria")
        industryType_temp = cur2.fetchall()

        # Cria tabela temporária no banco de destino
        cur1.execute("DROP TABLE IF EXISTS IndustryType_temp")
        cur1.execute("""
        CREATE TABLE IndustryType_temp (
            idIndustryType INT,
            cIndustryTypeName VARCHAR(255),
            cInfo TEXT,
            cActive CHAR(1) DEFAULT '1'
        )
        """)

        # Corrige o formato dos dados (tupla)
        industryType_temp_corrected = [(row[0], row[1], row[2]) for row in industryType_temp]

        # Insere os dados na tabela temporária
        insert_query = "INSERT INTO IndustryType_temp (idIndustryType, cIndustryTypeName, cInfo, cActive) VALUES (%s,%s,%s,DEFAULT)"
        cur1.executemany(insert_query, industryType_temp_corrected)
        conn.commit()

        # Executa Stored Procedure para atualizar tabela final
        print("Executando SP_UpdateIndustryType()")
        cur1.execute("CALL SP_UpdateIndustryType()")
        conn.commit()
        print("SP_UpdateIndustryType executada com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro na migração IndustryType_temp: {e}")
        conn.rollback()

    # --- Migração de Benefit_temp (Vantagens) ---
    try:
        print("Migrando Benefit_temp")
        cur2.execute("select idvantagem, cnmvantagem, cdescricao from vantagem")
        benefit_temp = cur2.fetchall()

        # Cria tabela temporária no banco de destino
        cur1.execute("DROP TABLE IF EXISTS Benefit_temp")
        cur1.execute("""
        CREATE TABLE Benefit_temp (
            idBenefit INT,
            cBenefitName VARCHAR(255),
            cDescription TEXT,
            cActive CHAR(1) DEFAULT '1'
        )
        """)

        benefit_temp_corrected = [(row[0], row[1], row[2]) for row in benefit_temp]

        # Insere os dados na tabela temporária
        insert_query = "INSERT INTO Benefit_temp (idBenefit, cBenefitName, cDescription, cActive) VALUES (%s,%s,%s,DEFAULT)"
        cur1.executemany(insert_query, benefit_temp_corrected)
        conn.commit()

        # Executa Stored Procedure
        print("Executando SP_UpdateBenefit()")
        cur1.execute("CALL SP_UpdateBenefit()")
        conn.commit()
        print("SP_UpdateBenefit executada com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro na migração Benefit_temp: {e}")
        conn.rollback()

    # --- Migração de ProductCategory_temp (Categorias de produto) ---
    try:
        print("Migrando ProductCategory_temp")
        cur2.execute("select idcategoriaproduto, cnmcategoria, cdescricao from categoriaproduto")
        productCategory_temp = cur2.fetchall()

        # Cria tabela temporária
        cur1.execute("DROP TABLE IF EXISTS ProductCategory_temp")
        cur1.execute("""
        CREATE TABLE ProductCategory_temp (
            idProductCategory INT,
            cCategoryName VARCHAR(255),
            cInfo TEXT,
            cActive CHAR(1) DEFAULT '1'
        )
        """)

        # Insere dados na tabela temporária
        insert_query = "INSERT INTO ProductCategory_temp (idProductCategory, cCategoryName, cInfo, cActive) VALUES (%s,%s,%s,DEFAULT)"
        cur1.executemany(insert_query, productCategory_temp)
        conn.commit()

        # Executa Stored Procedure
        print("Executando SP_UpdateProductCategory()")
        cur1.execute("CALL SP_UpdateProductCategory()")
        conn.commit()
        print("SP_UpdateProductCategory executada com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro na migração ProductCategory_temp: {e}")
        conn.rollback()

# --- Fechamento das conexões ---
finally:
    if conn:
        conn.close()  # Fecha conexão com o banco de destino
    if conn2:
        conn2.close()  # Fecha conexão com o banco de origem
    print("Conexões com os bancos de dados fechadas.")
