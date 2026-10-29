# Document Analyzer

API FastAPI que recebe um PDF, classifica o documento jurídico e extrai os
campos da categoria identificada, usando um modelo de linguagem via proxy.

## Rotas

| Método | Rota | Descrição |
|--------|------|-----------|
| `GET` | `/health` | Confirma que o serviço está no ar. |
| `POST` | `/upload` | Recebe um PDF no campo `file` (multipart), classifica e extrai os campos. Responde `document_type`, `justification` e `data`. Retorna 422 se o arquivo não for um PDF legível ou não tiver texto selecionável. |

## Estrutura por funcionalidade

```
document_analyzer/
  main.py                  cria a aplicação e inclui as rotas (uvicorn document_analyzer.main:app)
  api/routes.py            rotas /health e /upload
  auth/client.py           cliente do auth service e obtenção do token (singleton)
  pdf/text.py              extração do texto das páginas do PDF
  llm/client.py            modelo do proxy e limite de texto (MAX_TEXT_CHARS)
  classification/
    classifier.py          chain que classifica o documento
    schemas.py             DocumentType e DocumentClassification
  extraction/
    extractor.py           chain de extração por categoria
    schemas.py             campos extraídos de cada categoria
  analysis/pipeline.py     classifica e, em seguida, extrai os campos
tests/                     espelha a estrutura do pacote
```

## Variáveis de ambiente

No `.env` local (já está no `.gitignore`):

- `PGL_REGISTRATION_NUMBER`: matrícula usada no login do auth service.
- `PGL_PASSWORD`: senha usada no login.

O token obtido no login é a chave de acesso ao proxy do modelo.

## Ambiente virtual

```bash
uv venv .venv --python 3.13
uv pip install --python .venv/Scripts/python.exe -r requirements-dev.txt   # Windows
uv pip install --python .venv/bin/python -r requirements-dev.txt          # Linux/macOS
```

## Executar

```bash
uvicorn document_analyzer.main:app --reload
```

A documentação interativa fica em http://127.0.0.1:8000/docs.

## Testes

```bash
pytest
```

## Qualidade e CI

O workflow `.github/workflows/ci.yml` roda a cada pull request e a cada push
na `main`. Ele instala `requirements-dev.txt` com `uv` e executa:

```bash
pylint document_analyzer --fail-under=10
pylint tests --disable=missing-function-docstring,missing-class-docstring,too-few-public-methods,redefined-outer-name,unused-argument,line-too-long --fail-under=10
pytest -q
```

O pacote de produção deve ficar com nota 10/10. Nos testes, algumas regras
são desligadas porque fixtures e modelos falsos não precisam de docstring.
Para exigir o CI antes de mesclar, marque o check **Tests and pylint (Python 3.13)**
como obrigatório em *Settings → Branches* da `main`.

## Frontend de exemplo

`frontend/index.html` é uma página única, sem build, que envia um PDF para a
API e mostra o resultado em cartões animados (a animação usa o GSAP, carregado
do cdnjs, então é preciso de internet).

1. Suba a API: `uvicorn document_analyzer.main:app --reload`.
2. Abra `frontend/index.html` no navegador (duplo clique basta).
3. Arraste um PDF, clique em **Analisar documento** e veja a classificação e os campos.

Se a API estiver em outro endereço, troque o campo **Endereço da API**. O CORS
da API libera chamadas vindas de qualquer origem, o que permite abrir a página
direto do disco durante a aula.
