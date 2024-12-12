ITA
Codice e documento descrittivo dell'analisi di stringhe in ambito quantistico sviluppato durante il tirocinio presso Professor Reforgiato dell'Università degli Studi di Cagliari

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Per l'esecuzione di questo codice è necessario VS Code(https://code.visualstudio.com/download), Python versione >=3.10 ed una subscription attiva ad Azure. Le risorse di Azure Quantum sono gratuite ma l'invio di codice al processore H1 richiede crediti, soprattutto per la rotazione di stringhe con error correction.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Descrizione codici:

q_palindorme_Quant.py : Calcola se una stringa data si palindroma o meno                                                                                                                                                                                         
qec_reset_Quant.py : Calcola le rotazioni di una stringa data                                                                                                                                                                                                    
lcs.py : Contiene il codice per la creazione di gate controllati di rotazione                                                                                                                                                                                    
res_count.py: Sintetizza i risultati ottenuti (utile per rotazioni di stringhe di dimensioni >= 4)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Packages pip:                                                                                                                                                                                                                                                    
pip install pytket                                                                                                                                                                                                                                               
pip install pytket-quantinuum    

Estensioni VSCode:                                                                                                                                                                                                                                               
Azure Resources                                                                                                                                                                                                                                                  
Azure Quantum Development Kit 

Per esecuzione di codice Python:                                                                                                                                                                                                                                 
Azure Command Line Interface (https://learn.microsoft.com/it-it/cli/azure/install-azure-cli-windows?tabs=azure-cli)

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Per connettersi al workspace di Azure sarà necessario fare login sia in Azure Resources da VSCode, sia fare login da terminale con il comando az login (da VSCode). Una volta lanciato il comando verrà chiesto di scegliere l'account e bisognerà poi selezionare la propria Azure subscription.
Il workspace attualmente presente nel codice è a mio nome, sarà necessario sostituirlo con il proprio.

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
ENG
Code and descriptive document of string analysis in the quantum field developed during the internship with Professor Reforgiato of the University of Cagliari

To run this code you need VS Code(https://code.visualstudio.com/download), Python version >=3.10 and an active Azure subscription. Azure Quantum resources are free but sending code to the H1 processor requires credits, especially for rotating error-corrected strings.

Code description:

q_palindorme_Quant.py : Calculates whether a given string is palindromic or not
qec_reset_Quant.py : Calculate rotations of a given string
lcs.py : Contains code for creating rotation controlled gates
res_count.py: Summarizes the results obtained (useful for rotations of strings of size >= 4)

Pip Packages:
pip install pytket
pip install pytket-quantinuum

VSCode Extensions:
Azure Resources
Azure Quantum Development Kit

For running Python code:
Azure Command Line Interface (https://learn.microsoft.com/it-it/cli/azure/install-azure-cli-windows?tabs=azure-cli)

To connect to the Azure workspace you will need to log in both to Azure Resources from VSCode and to log in from the terminal with the az login command (from VSCode). Once the command is launched you will be asked to choose the account and you will then need to select your Azure subscription. The workspace currently present in the code is in my name, you will need to replace it with your own.

