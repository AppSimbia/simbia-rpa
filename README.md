# SIMBIA - RPAs

Este projeto visa automatizar a **transferência e sincronização de dados** entre o banco de origem e o banco de destino do aplicativo **SIMBIA**, garantindo que todas as informações estejam sempre atualizadas e consistentes.

---

## Funcionalidades

- Extrair os dados do banco de origem (sistema legado);
- Criar tabelas temporárias no banco de destino;
- Inserir os dados extraídos e consolidar as informações;
- Executar stored procedures responsáveis por atualizar as tabelas finais;
- Aplicar regras de normalização conforme o modelo do app SIMBIA;
- Garantir rollback automático em caso de falha durante a migração.

---

## Modelagens

A seguir, são apresentadas as modelagens utilizadas para os bancos de dados SQL do projeto.

### Modelagem SQL Origem

<img width="401" height="438" alt="image" src="https://github.com/user-attachments/assets/13c8ad93-6550-46f8-b614-4ff82f7036f7" />

### Modelagem SQL Destino

<img width="401" height="393" alt="image" src="https://github.com/user-attachments/assets/25844cab-9f7b-4e45-b317-85e3fbcfecb9" />

---

## Tabelas Contempladas

A seguir, estão as tabelas que tiveram os dados transferidos do **Banco Origem → Banco Destino**:

- Planos → `Plan_temp`
- Tipo de Indústria → `IndustryType_temp`
- Vantagens → `Benefit_temp`
- Categoria de Produto → `ProductCategory_temp`
- Permissões → `Permission_temp`

Cada tabela temporária é criada no banco de destino, recebe os dados extraídos do banco de origem e, em seguida, é utilizada nas *stored procedures* de atualização:

- `SP_UpdatePlan()`
- `SP_UpdateIndustryType()`
- `SP_UpdateBenefit()`
- `SP_UpdateProductCategory()`
- `SP_UpdatePermission()`

---

## Normalização

Durante a etapa de transformação, foram aplicados conceitos de normalização para manter a consistência dos dados.

### Planos
- Separação dos campos de status e valores em colunas específicas;
- Inclusão de campo de controle `nActive` para identificar registros ativos.

### Vantagens
- O campo de descrição foi isolado para permitir buscas textuais mais rápidas;
- Foi padronizada a nomenclatura dos campos de texto (`cBenefitName`, `cDescription`).

### Categoria de Produto
- Separação de nomes e descrições de categorias para normalização de dados e redução de redundâncias.

### Permissões
- Criação de tabela simplificada contendo apenas identificador e nome da permissão.

---

## Dependências

Para executar este projeto, você precisará instalar as seguintes bibliotecas e ferramentas:

### Python
- Python 3.12 ou superior
- psycopg2-binary 2.9.9
- python-dotenv 1.0.0

Instalação:
```bash
pip install -r requirements.txt
```

### Banco de Dados
- PostgreSQL (banco relacional de origem e destino)

#### Criar Bancos de Dados
Para criar os bancos de dados, execute os scripts `DDL_Origem.sql` e `DDL_Destino.sql` no seu SGBD.  
⚠️ Não se esqueça de criar previamente os bancos de dados e configurar as variáveis de ambiente no arquivo `.env`.

Exemplo de `.env`:
```bash
DB1_NAME=nome_banco_destino
DB1_USER=usuario_destino
DB1_PASSWORD=senha_destino
DB1_HOST=host_destino
DB1_PORT=5432

DB2_NAME=nome_banco_origem
DB2_USER=usuario_origem
DB2_PASSWORD=senha_origem
DB2_HOST=host_origem
DB2_PORT=5432
```

---

## Outras Ferramentas

- Git
- AWS EC2 (para execução em nuvem)
- dotenv (gerenciamento seguro de variáveis de ambiente)

---

## Autores

- [@MatheusMakita](https://github.com/MatheusMakita)
- [@Valenaantunes](https://github.com/Valenaantunes)
