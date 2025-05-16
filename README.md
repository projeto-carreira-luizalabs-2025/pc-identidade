# pc-identidade

## 📌 Identidade do Varejista

O projeto pc-identidade é responsável por estruturar e definir quem é o varejista dentro do sistema do marketplace. A proposta é identificar, validar e organizar as informações que permitem que o varejista seja reconhecido, aprovado e integrado com segurança e clareza ao ecossistema do marketplace.
Esta camada de identidade será essencial para garantir a confiabilidade dos vendedores na plataforma, atender requisitos legais, e oferecer um processo de onboarding eficiente.

[Documentação do Projeto](https://docs.google.com/document/d/11eIj0-f68q7rLtMQsC7VShPTmDfvgnPDPt6HPMMM_Z4/edit?tab=t.0#heading=h.4bbpjvh4rnth)

## 🎯 Objetivos principais:
- Identificação e validação da identidade do varejista
- Recolhimento e análise de dados/documentos obrigatórios
- Avaliação da reputação e relevância do vendedor
- Organização das informações operacionais e de negócio
- Preparação dos dados para uso nas demais áreas do marketplace

## 👥 Participantes do Time:

- João Pedro
- Marcella Palazzo
- Murilo Alves
- Victor Hugo Buiatti

## ✨ Configuração do ambiente local

### Linux 🐧

Todos os comandos serão via terminal.

Este _seed_ trabalha com o [Python 3.12](https://docs.python.org/3.12/), confirme se o mesmo está instalado em sua máquina.

Depois de clonar o projeto, acesse o diretório:

```sh
cd pc-identidade
```

Crie o [ambiente virtual](https://docs.python.org/3.12/tutorial/venv.html)
para instalar as bibliotecas e trabalharmos com o projeto:

```sh
make build-venv
# ou
# python3.12 -m venv venv
```

Uma vez criado o ambiente virtual do Python, você precisa ativá-lo
(estou supondo que você está no Linux 🐧):

```sh
. ./venv/bin/activate
```

Quaisquer comandos daqui para frente, iremos considerar que você está dentro
do ambiente virtual `(venv)`.

Instale as bibliotecas necessárias

```sh
pip install -r requirements.txt
```

Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

```env
ENV=dev
```

Rode o servidor FastAPI com Uvicorn

```sh
uvicorn app.api_main:app --reload
```

A aplicação estará disponível em: 📍 http://127.0.0.1:8000

🩺 Verifique o status em: http://127.0.0.1:8000/api/health

### Windows 🖥️

#### 1. Clone o repositório

```powershell
git clone https://github.com/projeto-carreira-luizalabs-2025/pc-identidade.git
cd pc-catalogo
```

#### 2. Crie o ambiente virtual

```powershell
python -m venv venv
.\venv\Scripts\activate
```

#### 3. Instale as dependências

```powershell
pip install -r requirements.txt
```

#### 4. Configure variáveis de ambiente

Crie um arquivo .env na raiz do projeto com o seguinte conteúdo:

```env
ENV=dev
```

#### 5. Rode o servidor

```powershell
uvicorn app.api_main:app --reload
```

A aplicação estará disponível em: 📍 http://127.0.0.1:8000

🩺 Verifique o status em: http://127.0.0.1:8000/api/health

## Contribuições e Atualizações
O projeto está aberto a contribuições e atualizações da comunidade. O processo para contribuições é o seguinte:

* **Pull Requests**: Contribuições devem ser submetidas como pull requests.
* **Code Review**: Cada pull request passará por um code review detalhado pela equipe. Isso garante que o código esteja alinhado com os padrões de qualidade e funcionamento do projeto.
* **Incorporação de Mudanças**: Após a aprovação no code review, as mudanças serão integradas ao código principal.

## 📖 Recursos úteis

- [Conventional Commits](https://www.conventionalcommits.org)