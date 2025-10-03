import psycopg2
from dotenv import load_dotenv
from os import getenv

load_dotenv()

conn = None
conn2 = None

try:  
    conn = psycopg2.connect(
        dbname=getenv("DB1_NAME"),
        user=getenv("DB1_USER"),
        password=getenv("DB1_PASSWORD"),
        host=getenv("DB1_HOST"),
        port=getenv("DB1_PORT")
    )
    cur1 = conn.cursor()

    conn2 = psycopg2.connect(
        dbname=getenv("DB2_NAME"),
        user=getenv("DB2_USER"),
        password=getenv("DB2_PASSWORD"),
        host=getenv("DB2_HOST"),
        port=getenv("DB2_PORT")
    )
    cur2 = conn2.cursor()

    conn2.rollback()
    conn.rollback()
    print("Conexão com o banco feita com sucesso!")

    # --- Plan_temp --- plano 
    try:
        print("Migrando Plan_temp")
        cur2.execute("select idplano, nvalor, nativo, cnmplano from plano")
        plan_temp = cur2.fetchall()

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

        insert_query = "INSERT INTO Plan_temp (idPlan, nPrice, cActive, cPlanName, nActive) VALUES (%s,%s,%s,%s,DEFAULT)"
        cur1.executemany(insert_query, plan_temp)
        conn.commit()

        print("Executando SP_UpdatePlan()")
        cur1.execute("CALL SP_UpdatePlan()")
        conn.commit()
        print("SP_UpdatePlan executada com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro na migração Plan_temp: {e}")
        conn.rollback()

    # --- Industry_temp ---
    # try:
    #     print("Migrando Industry_temp")
    #     cur2.execute("""
    #         SELECT idIndustry, industryName, email, idIndustryCategory, idPlan, status
    #         FROM industry
    #     """)
    #     industry_temp = cur2.fetchall()

    #     cur1.execute("DROP TABLE IF EXISTS Industry_temp")
    #     cur1.execute("""
    #     CREATE TABLE Industry_temp (
    #         idIndustry INT,
    #         cIndustryName VARCHAR(255),
    #         cContactMail VARCHAR(255),
    #         idIndustryCategory INT,
    #         idPlan INT,
    #         status VARCHAR(50),
    #         nActive CHAR(1) DEFAULT '1'
    #     )
    #     """)

    #     insert_query = """
    #     INSERT INTO Industry_temp (idIndustry, cIndustryName, cContactMail, idIndustryCategory, idPlan, status, nActive)
    #     VALUES (%s,%s,%s,%s,%s,%s,DEFAULT)
    #     """
    #     cur1.executemany(insert_query, industry_temp)
    #     conn.commit()
    #     print("Industry_temp migrada com sucesso")
    # except psycopg2.Error as e:
    #     print(f"Erro na migração Industry_temp: {e}")
    #     conn.rollback()

    # --- IndustryType_temp --- tipoindustria
    try:
        print("Migrando IndustryType_temp")
        cur2.execute("""
            select idtipoindustria, cnmtipoindustria, cdescricao from tipoindustria
        """)
        industryType_temp = cur2.fetchall()

        cur1.execute("DROP TABLE IF EXISTS IndustryType_temp")
        cur1.execute("""
        CREATE TABLE IndustryType_temp (
            idIndustryType INT,
            cIndustryTypeName VARCHAR(255),
            cInfo TEXT,
            cActive CHAR(1) DEFAULT '1'
        )
        """)

        industryType_temp_corrected = [(row[0], row[1], row[2]) for row in industryType_temp]

        insert_query = "INSERT INTO IndustryType_temp (idIndustryType, cIndustryTypeName, cInfo, cActive) VALUES (%s,%s,%s,DEFAULT)"
        cur1.executemany(insert_query, industryType_temp_corrected)
        conn.commit()

        print("Executando SP_UpdateIndustryType()")
        cur1.execute("CALL SP_UpdateIndustryType()")
        conn.commit()
        print("SP_UpdateIndustryType executada com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro na migração IndustryType_temp: {e}")
        conn.rollback()

    # --- Benefit_temp --- vantagem 
    try:
        print("Migrando Benefit_temp")
        cur2.execute("select idvantagem, cnmvantagem, cdescricao from vantagem")
        benefit_temp = cur2.fetchall()

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

        insert_query = "INSERT INTO Benefit_temp (idBenefit, cBenefitName, cDescription, cActive) VALUES (%s,%s,%s,DEFAULT)"
        cur1.executemany(insert_query, benefit_temp_corrected)
        conn.commit()

        print("Executando SP_UpdateBenefit()")
        cur1.execute("CALL SP_UpdateBenefit()")
        conn.commit()
        print("SP_UpdateBenefit executada com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro na migração Benefit_temp: {e}")
        conn.rollback()

    # --- ProductCategory_temp --- categoriaproduto
    try:
        print("Migrando ProductCategory_temp")
        cur2.execute("select idcategoriaproduto, cnmcategoria, cdescricao from categoriaproduto")
        productCategory_temp = cur2.fetchall()

        cur1.execute("DROP TABLE IF EXISTS ProductCategory_temp")
        cur1.execute("""
        CREATE TABLE ProductCategory_temp (
            idProductCategory INT,
            cCategoryName VARCHAR(255),
            cInfo TEXT,
            cActive CHAR(1) DEFAULT '1'
        )
        """)

        insert_query = "INSERT INTO ProductCategory_temp (idProductCategory, cCategoryName, cInfo, cActive) VALUES (%s,%s,%s,DEFAULT)"
        cur1.executemany(insert_query, productCategory_temp)
        conn.commit()

        print("Executando SP_UpdateProductCategory()")
        cur1.execute("CALL SP_UpdateProductCategory()")
        conn.commit()
        print("SP_UpdateProductCategory executada com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro na migração ProductCategory_temp: {e}")
        conn.rollback()

    # --- Permission_temp --- permissao
    try:
        print("Migrando Permission_temp")
        cur2.execute("select idpermissao, cnmpermissao from permissao")
        permission_temp = cur2.fetchall()

        cur1.execute("DROP TABLE IF EXISTS Permission_temp")
        cur1.execute("""
        CREATE TABLE Permission_temp (
            idPermission INT,
            cPermissionName VARCHAR(255),
            cActive CHAR(1) DEFAULT '1'
        )
        """)

        insert_query = "INSERT INTO Permission_temp (idPermission, cPermissionName, cActive) VALUES (%s,%s,DEFAULT)"
        cur1.executemany(insert_query, permission_temp)
        conn.commit()

        print("Executando SP_UpdatePermission()")
        cur1.execute("CALL SP_UpdatePermission()")
        conn.commit()
        print("SP_UpdatePermission executada com sucesso.")
    except psycopg2.Error as e:
        print(f"Erro na migração Permission_temp: {e}")
        conn.rollback()

    print("\nScript de migração concluído com sucesso!")

except psycopg2.Error as e:
    print(f"\nOcorreu um erro no banco de dados: {e}")
    if conn:
        conn.rollback()
    if conn2:
        conn2.rollback()
except Exception as e:
    print(f"\nOcorreu um erro inesperado: {e}")
finally:
    if conn:
        conn.close()
    if conn2:
        conn2.close()
    print("Conexões com os bancos de dados fechadas.")
