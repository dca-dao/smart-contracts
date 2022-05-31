# Smart Contracts
## DcaManager
Un contrat pour gérer l'ensemble des comptes des utilisateurs ainsi que la configuration de leur DCA.
### Variables
### Fonctions
#### setupDca
```
function setupDca(uint256 interval, uint256 amount){}
``` 
Permet de modifier l'intervalle de temps pour le déclanchement du swap.

<table>
    <thead>
        <tr>
            <th align="left">Name</th>
            <th align="left">Type</th>
            <th align="left">Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left"><code>interval</code></td>
            <td align="left">uint256</td>
            <td align="left">Intervalle de temps entre deux achats automatique</td>
            </tr>
            <tr>
            <td align="left"><code>amount</code></td>
            <td align="left">uint256</td>
            <td align="left">Montant de DAI utilisé à chaque achat automatique</td>
            </tr>
    </tbody>
</table>

#### fundAccount
```
function fundAccount(uint256 value, address tokenAddress){}
``` 
Permet d'ajouter des tokens sur l'application dca.io
<table>
    <thead>
        <tr>
            <th align="left">Name</th>
            <th align="left">Type</th>
            <th align="left">Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left"><code>value</code></td>
            <td align="left">uint256</td>
            <td align="left">Nombre de tokens à envoyer</td>
            </tr>
            <tr>
            <td align="left"><code>tokenAddress</code></td>
            <td align="left">address</td>
            <td align="left">Adresse du token à envoyer</td>
            </tr>
    </tbody>
</table>

#### withdraw
```
function withdraw(uint256 value, address tokenAddress){}
``` 
Permet de retirer des tokens de l'application dca.io
<table>
    <thead>
        <tr>
            <th align="left">Name</th>
            <th align="left">Type</th>
            <th align="left">Description</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="left"><code>value</code></td>
            <td align="left">uint256</td>
            <td align="left">Nombre de tokens à retirer</td>
            </tr>
            <tr>
            <td align="left"><code>tokenAddress</code></td>
            <td align="left">address</td>
            <td align="left">Adresse du token à retirer</td>
            </tr>
    </tbody>
</table>