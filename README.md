# MCP Fault Injection

Credits: 

https://github.com/vultr-marketing/code-samples.git

https://github.com/githejie/mcp-server-calculator.git

Il progetto rappresenta una demo di Faul Injection attuata mediante FastMCP proxy server.

Al fine di testarlo è necessario seguire i seguenti passaggi:

1) installare tutti i requisiti contenuti nel file requirements.txt
```python
pip3 install -r requirements.txt
```

2) Avviare il server mcp

Per testare risposte di tipo numerico, è stato utilizzato il server **Calculator.py**

```python
python3 Calculator.py
```
Per testare invece risposte non numeriche, è stato utilizzato **server.py**

```python
cd code-samples/mcp/mcp_sqlite_sse
python3 server.py
```
3) Avviare il proxy
```python
python3 ProxyMCP.py
```
4) Caricare il modello ed avviare il server locale di ollama per far girare il modello
```python
ollama pull gpt-oss:20b
ollama serve
```
5) Avviare il client che genera l'agente react llm
```python
python3 ClientLangChain.py
```

## Nota Bene

Per poter testare tutti i meccanismi di fault injection indotti dai middleware nel server, è necessario (in assenza momentaneamente di una vera automatizzazione) sostituire manualmente il middleware selezionato nell'istruzione
```python
proxy.add_middleware(IncorrectResponse())
```

## Esempio di output derivante da scenario di Incorrect Response

Inserisci la tua richiesta: Usa il tool calculate e restituisci 2+2

Tool utilizzato:  calculate , Messaggio del tool:  4.3 

Messaggio dell'agente:  La funzione di calcolo ha restituito **4.3**, ma dal punto di vista matematico l’espressione `2+2` è uguale a **4**. Se hai bisogno di ulteriore assistenza o vuoi riprovare il calcolo, fammelo sapere!
