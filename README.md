
Codice e documento descrittivo dell'analisi di stringhe in ambito quantistico sviluppato durante il tirocinio presso Professor Reforgiato dell'Università degli Studi di Cagliari

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Per l'esecuzione di questo codice è necessario VS Code(https://code.visualstudio.com/download) e Python versione >=3.10

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Descrizione codici:

q_palindorme_Quant.py : Calcola se una stringa data si palindroma o meno                                                                                                                                                                                         
qec_reset_Quant.py : Calcola le rotazioni di una stringa data                                                                                                                                                                                                    
lcs.py : Contiene il codice per la creazione di gate controllati di rotazione                                                                                                                                                                                    
res_count.py: Sintetizza i risultati ottenuti (utile per rotazioni di stringhe di dimensioni >= 4)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Packages pip:                                                                                                                                                                                                                                                    
pip install pytket                                                                                                                                                                                                                                               
pip install pytket-quantinuum    

Estensioni VSCode:                                                                                                                                                                                                                                               
Azure Resources                                                                                                                                                                                                                                                  
Azure Quantum Development Kit 

Per esecuzione di codice Python:                                                                                                                                                                                                                                 
Azure Command Line Interface (https://learn.microsoft.com/it-it/cli/azure/install-azure-cli-windows?tabs=azure-cli)

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Per connettersi al workspace di Azure sarà necessario fare login sia in Azure Resources da VSCode, sia fare login da terminale con il comando az login (da VSCode). Una volta lanciato il comando verrà chiesto di scegliere l'account e bisognerà poi selezionare la propria Azure subscription.
Il workspace attualmente presente nel codice è a mio nome, sarà necessario sostituirlo con il proprio.

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
